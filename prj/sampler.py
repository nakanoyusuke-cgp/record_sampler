import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.lang.builder import Builder

import pyaudio
import numpy as np
from threading import Thread

import staticParams
import sound
import pad
import recorder

class Sampler(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialized = False

    # kvファイルのロード後に呼び出す初期化用メソッド
    def init_sampler(self, sp:staticParams.StaticParams):
        # 静的パラメータ
        self.sample_size = sp.sample_size
        self.channel_num = sp.channel_num
        self.fs = sp.fs

        # プロット用変数初期化
        self.plot_count = 0
        self.plot_interval = 30
        
        # GUI要素の取得
        self.file_picker = self.ids["file_picker"]
        self.graph = self.ids["graph_view"]

        # 各パッドのインスタンス化
        self.sound_num = 10
        self.pads = []
        for i in range(self.sound_num):
            pad_wid = pad.Pad()
            self.pads.append(pad_wid)
            self.ids.pad_grid.add_widget(pad_wid)

        # ストリーム初期化
        audio = pyaudio.PyAudio()
        self.stream = audio.open(
            format=pyaudio.paInt16, 
            channels=self.channel_num, 
            rate=int(self.fs), 
            output=True)

        # レコーダ初期化
        self.recorder = recorder.Recorder(sp)

        self.initialized = True
        print("sampler inited")
    
    # ミックス・出力をスレッディングする
    def run(self):
        while self.isRunning:
            buf = self.mix()
            self.recorder.record_sample(buf)
            self.stream.write(buf)
            self.plot()

    # サンプラーをスタートする
    def start(self):
        if(not self.initialized):
            print("sampler is not initialized!!")
            return

        self.isRunning = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    # サンプラーを停止する
    def stop(self):
        self.isRunning = False
        self.thread.join()
        exit()

    # パッドに音声を設定する。
    def set_sound(self, idx, path):
        if(not self.initialized):
            print("sampler is not initialized!!")
            return
        
        if(idx < 0 or idx > len(self.pads)):
            print("illegal pad index!!")
            return

        self.pads[idx].set_sound(path)

    # 各パッドの音をミックスする
    def mix(self):
        buf = np.zeros(self.sample_size).astype(np.int16)
        for pad in self.pads:
            if pad.sound.isPlaying:
                ps = pad.sound.get_next_sample()
                buf += np.pad(ps,(0,self.sample_size-len(ps)),"wrap")

        return buf

    # レコードした音をファイル出力する
    def record(self):
        self.recorder.save_file(self.ids["record_file_name"].text + ".wav")

    # 現在まで録音した波形をプロットする
    def plot(self):
        if(self.plot_count > self.plot_interval):
            data = self.recorder.get_recorded_wave()
            self.graph.plot(data)
            self.plot_count = 0
        self.plot_count += 1
