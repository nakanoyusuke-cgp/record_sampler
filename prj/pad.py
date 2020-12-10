import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

import staticParams
import sound

# パッドのウィジェット
class Pad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sp = staticParams.StaticParams()
        self.sound = sound.Sound(self.sp)

    # パッドをたたく処理
    def play_pad(self, num):
        self.sound.play()

    # 音声をパッドに設定する
    def set_sound(self, path):
        self.sound.set_wave(path)
        self.ids["pad_text"].text = self.sound.name

    # 音声の名前を取得する。
    def get_name(self):
        return self.sound.name
