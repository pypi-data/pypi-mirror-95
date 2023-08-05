#!/usr/bin/python3
# coding=utf-8
""" PyMusicLooper
    Copyright (C) 2020  Hazem Nabil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

import json
import os
import sys
import time
from multiprocessing import Manager, Process

import librosa
import numpy as np
import soundfile


class MusicLooper:
    def __init__(self, filename, min_duration_multiplier=0.35):
        # Load the file if it exists
        if os.path.exists(filename) and os.path.isfile(filename):
            try:
                audio, sr = librosa.load(filename, sr=None, mono=False)
            except Exception:
                raise TypeError("Unsupported file type.")
        else:
            raise FileNotFoundError("Specified file not found.")

        self.filename = filename
        mono_signal = librosa.core.to_mono(audio)
        self.audio, self.trim_offset = librosa.effects.trim(mono_signal)
        self.rate = sr
        self.playback_audio = audio
        self.min_duration_multiplier = min_duration_multiplier

        # Initialize parameters for playback
        self.channels = self.playback_audio.shape[0]

    def _loop_finding_routine(
        self,
        beats,
        i_start,
        i_stop,
        chroma,
        power_db,
        min_duration,
    ):
        for i in range(i_start, i_stop):
            deviation = np.linalg.norm(chroma[..., beats[i]] * 0.1)
            for j in range(i):
                # Since the beats array is sorted
                # any j >= current_j will only decrease in duration
                if beats[i] - beats[j] < min_duration:
                    break
                dist = np.linalg.norm(chroma[..., beats[i]] -
                                      chroma[..., beats[j]])
                if dist <= deviation:
                    avg_db_diff = self.db_diff(power_db[..., beats[i]],
                                               power_db[..., beats[j]])
                    if avg_db_diff <= 10:
                        self._candidate_pairs_q.put({
                            "loop_start": beats[j],
                            "loop_end": beats[i],
                            "dB_diff": avg_db_diff
                        })

    def db_diff(self, power_db_f1, power_db_f2):
        average_diff = np.average(np.abs(power_db_f1 - power_db_f2))
        return average_diff

    def find_loop_pairs(self,
                        combine_beat_plp=False,
                        concurrency=False):
        runtime_start = time.time()

        S = librosa.core.stft(y=self.audio)
        S_power = np.abs(S)**2
        S_weighed = librosa.core.perceptual_weighting(
            S=S_power, frequencies=librosa.fft_frequencies(sr=self.rate))
        mel_spectrogram = librosa.feature.melspectrogram(S=S_weighed)
        onset_env = librosa.onset.onset_strength(S=mel_spectrogram)
        bpm, beats = librosa.beat.beat_track(onset_envelope=onset_env)

        beats = np.sort(beats)
        print("Detected {} beats at {:.0f} bpm".format(beats.size, bpm))

        chroma = librosa.feature.chroma_stft(S=S_power)

        power_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
        min_duration = int(chroma.shape[-1] * self.min_duration_multiplier)

        self._candidate_pairs_q = Manager().Queue()

        runtime_end = time.time()
        prep_time = runtime_end - runtime_start
        print("Finished initial prep in {:.3}s".format(prep_time))

        def loop_subroutine(combine_beat_plp=combine_beat_plp,
                            beats=beats,
                            avg_dB_diff_threshold=10):
            if combine_beat_plp:
                onset_env = librosa.onset.onset_strength(S=mel_spectrogram)
                pulse = librosa.beat.plp(onset_envelope=onset_env)
                beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
                beats = np.union1d(beats, beats_plp)
                print(
                    "Detected {} total points by combining PLP with existing beats"
                    .format(beats.size))

            if concurrency:
                processes = []
                affinity = 16
                first_half = int(beats.size / 2)
                step_size = int(beats.size / affinity)
                i_step = np.concatenate([
                    [1, first_half],
                    np.arange(
                        start=first_half + step_size,
                        stop=beats.size,
                        step=step_size,
                        dtype=np.intp,
                    ),
                ])
                i_step[-1] = int(beats.size)
                for i in range(i_step.size - 1):
                    p = Process(
                        target=self._loop_finding_routine,
                        args=(
                            beats,
                            i_step[i],
                            i_step[i + 1],
                            chroma,
                            power_db,
                            min_duration,
                        ),
                    )
                    processes.append(p)
                    p.daemon = True
                    p.start()
            else:
                self._loop_finding_routine(beats, 1, beats.size, chroma,
                                           power_db, min_duration)

            if concurrency:
                for process in processes:
                    process.join()

            candidate_pairs = []

            while not self._candidate_pairs_q.empty():
                candidate_pairs.append(self._candidate_pairs_q.get())

            candidate_pairs = sorted(candidate_pairs,
                                     reverse=False,
                                     key=lambda x: x["dB_diff"])

            db_diff_array = np.array([
                candidate_pairs[i]["dB_diff"]
                for i in range(len(candidate_pairs))
            ])
            db_diff_avg = np.average(db_diff_array)
            db_diff_std = np.std(db_diff_array)

            i = 0
            one_stddev = db_diff_avg - db_diff_std
            while i < len(candidate_pairs):
                if candidate_pairs[i]["dB_diff"] > one_stddev:
                    break
                i += 1

            pruned_list = candidate_pairs[:i if i >= 10 else 10]

            test_offset = librosa.samples_to_frames(
                np.amax([int((bpm / 60) * 0.1 * self.rate), self.rate * 1.5]))

            subseq_beat_sim = [
                self._subseq_beat_similarity(
                    pruned_list[i]["loop_start"],
                    pruned_list[i]["loop_end"],
                    chroma,
                    test_duration=test_offset,
                ) for i in range(len(pruned_list))
            ]

            # Add cosine similarity as score
            for i in range(len(pruned_list)):
                pruned_list[i]["score"] = subseq_beat_sim[i]

            # re-sort based on new score
            pruned_list = sorted(pruned_list,
                                 reverse=True,
                                 key=lambda x: x["score"])
            return pruned_list

        pruned_list = loop_subroutine()

        # Retry will trigger when:
        # (a) there is no beat sequence with <5dB difference and >90% similarity
        # (b) list is empty
        retry = True
        for i in range(len(pruned_list)):
            if pruned_list[i]["dB_diff"] <= 5.0 and pruned_list[i][
                    "score"] >= 0.90:
                retry = False
                break

        if retry and not combine_beat_plp:
            print(
                "No suitable loop points found with current parameters. Retrying with additional beat points from PLP method."
            )
            pruned_list = loop_subroutine(combine_beat_plp=True)

        if self.trim_offset[0] > 0:
            for i in range(len(pruned_list)):
                pruned_list[i]["loop_start"] = self.apply_trim_offset(
                    pruned_list[i]["loop_start"])
                pruned_list[i]["loop_end"] = self.apply_trim_offset(
                    pruned_list[i]["loop_end"])

        return pruned_list

    def apply_trim_offset(self, frame):
        return librosa.samples_to_frames(
            librosa.frames_to_samples(frame) + self.trim_offset[0])

    def _subseq_beat_similarity(self, b1, b2, chroma, test_duration=None):
        if test_duration is None:
            test_duration = librosa.samples_to_frames(self.rate * 3)

        testable_offset = np.amin([
            test_duration,
            chroma[..., b1:b1 + test_duration].shape[1],
            chroma[..., b2:b2 + test_duration].shape[1],
        ])

        cosim = np.zeros(test_duration)

        for i in range(testable_offset):
            dot_prod = np.dot(chroma[..., b1 + i], chroma[..., b2 + i])
            b1_norm = np.linalg.norm(chroma[..., b1 + i])
            b2_norm = np.linalg.norm(chroma[..., b2 + i])
            cosim[i] = dot_prod / (b1_norm * b2_norm)

        return np.average(cosim)

    def samples_to_frames(self, samples):
        return librosa.core.samples_to_frames(samples)

    def frames_to_samples(self, frame):
        return librosa.core.frames_to_samples(frame)

    def frames_to_ftime(self, frame):
        time_sec = librosa.core.frames_to_time(frame, sr=self.rate)
        return "{:02.0f}:{:06.3f}".format(time_sec // 60, time_sec % 60)

    def play_looping(self, loop_start, loop_end):
        from mpg123 import ENC_FLOAT_32
        from mpg123 import Out123

        out = Out123()
        encoding = ENC_FLOAT_32

        out.start(self.rate, self.channels, encoding)

        playback_frames = librosa.util.frame(
            self.playback_audio.flatten(order="F"))
        adjusted_loop_start = loop_start * self.channels
        adjusted_loop_end = loop_end * self.channels

        i = adjusted_loop_end - 1000
        loop_count = 0
        try:
            while True:
                out.play(playback_frames[..., i])
                i += 1
                if i == adjusted_loop_end:
                    i = adjusted_loop_start
                    loop_count += 1
                    print("Currently on loop #{}".format(loop_count), end="\r")

        except KeyboardInterrupt:
            print()  # so that the program ends on a newline

    def export(self, loop_start, loop_end, filename=None, format="WAV"):
        if filename is None:
            filename = os.path.splitext(self.filename)[0]

        filename = os.path.abspath(filename)

        loop_start = self.frames_to_samples(loop_start)
        loop_end = self.frames_to_samples(loop_end)

        soundfile.write(
            filename + "-intro." + format.lower(),
            self.playback_audio[..., :loop_start].T,
            self.rate,
            format=format,
        )
        soundfile.write(
            filename + "-loop." + format.lower(),
            self.playback_audio[..., loop_start:loop_end].T,
            self.rate,
            format=format,
        )
        soundfile.write(
            filename + "-outro." + format.lower(),
            self.playback_audio[..., loop_end:].T,
            self.rate,
            format=format,
        )

    def export_json(self, loop_start, loop_end, score):
        loop_start = self.frames_to_samples(loop_start)
        loop_end = self.frames_to_samples(loop_end)

        out = {
            "loop_start": int(loop_start),
            "loop_end": int(loop_end),
            "score": float(f"{score:.4}"),
        }

        with open(self.filename + "-lps.json", "w") as file:
            json.dump(out, fp=file)

    def cache_loop_points(self, loop_start, loop_end, score):
        filename = os.path.abspath(self.filename)

        out = {
            "loop_start": int(loop_start),
            "loop_end": int(loop_end),
            "score": float(f"{score:.4}"),
        }

        dirpath = os.path.dirname(os.path.realpath(__file__))
        cache_path = os.path.join(dirpath, "cache.json")
        try:
            with open(cache_path, "r") as file:
                cache = json.load(file)
        except Exception:
            cache = {}
        try:
            with open(cache_path, "w") as file:
                cache[filename] = out
                json.dump(cache, fp=file)
        except Exception as e:
            sys.stderr(f"Couldn't write to cache. Error: {e}")
