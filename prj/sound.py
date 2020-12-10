import os
import numpy as np
import struct
import wave

import staticParams

# パッドに割り当てられる音声
class Sound():
    def __init__(self, sp:staticParams.StaticParams):
        self.name = 'no sound'
        self.wave = None
        self.sample_size = sp.sample_size
        self.isPlaying = False
        self.samples = []
        self.current_sample = 0
        self.max_sample = 0

    # 音声を設定する wavファイルをサンプルごとに区切りすぐに取り出せるようにする
    def set_wave(self, path):
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.samples.clear()

        with wave.open(path , "r" ) as wavef:
            self.wave = wavef
            while True:
                buf = self.wave.readframes(self.sample_size)
                if(len(buf) is 0):
                    break
                sample = np.frombuffer(buf, dtype="int16")
                self.samples.append(np.pad(sample,(0,self.sample_size-len(sample)),"wrap"))

        self.current_sample = 0
        self.max_sample = len(self.samples)
        self.isPlaying = False

    # 次のサンプルを取り出す。
    def get_next_sample(self):
        self.current_sample += 1
        if(self.current_sample >= self.max_sample):
            self.isPlaying = False
        return np.frombuffer(self.samples[self.current_sample - 1], dtype="int16")
    
    # サンプルを取り出すための変数を初期化し、サンプルをSamplerクラスが取り出せるようにする
    def play(self):
        if self.wave is None:
            return
        self.isPlaying = True
        self.current_sample = 0
