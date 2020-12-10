import numpy as np
import wave
import struct

import staticParams

# 音声履歴を保存しておき、Samplerの要求でファイル出力する
class Recorder():
    def __init__(self, sp:staticParams.StaticParams):
        self.fs = sp.fs
        self.sample_size = sp.sample_size
        self.record_second = sp.record_second
        self.channel_num = sp.channel_num
        self.sample_num = sp.fs * self.record_second // sp.sample_size
        self.samples = []
        self.current = 0

    # サンプルを記録する
    def record_sample(self, sample):
        if(len(self.samples) < self.sample_num):
            self.samples.append(sample)
        # print(f"samples:{len(self.samples)}, sample_num:{self.sample_num}")
        self.samples[self.current] = sample
        self.current += 1
        if(self.current >= self.sample_num):
            self.current = 0

    # 録音した波形を返す
    def get_recorded_wave(self):
        return np.roll(np.hstack(self.samples), -self.current * self.sample_size)

    # 記録したサンプルを出力する
    def save_file(self, filename="record.wav"):
        data = self.get_recorded_wave()
        binaryData = struct.pack("h" * len(data), *data)
        out = wave.Wave_write(filename)
        param = (self.channel_num, 2, self.fs, len(binaryData), 'NONE', 'not compressed') 
        out.setparams(param)
        out.writeframes(binaryData)
        out.close()
        