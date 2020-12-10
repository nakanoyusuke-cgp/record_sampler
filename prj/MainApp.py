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
from kivy.lang.builder import Builder

import staticParams
import pad
import sampler
import filePicker
import graphView

Builder.load_file('pad.kv')
Builder.load_file('filePicker.kv')
Builder.load_file('graphView.kv')
Builder.load_file('sampler.kv')

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sp = staticParams.StaticParams()

        self.smplr = self.ids["sampler"]
        self.smplr.init_sampler(sp)
        self.smplr.start()

class MainApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    MainApp().run()
