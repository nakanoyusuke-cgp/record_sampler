from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

# 音声の時間波形を表示する
class GraphView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('X label')
        self.ax.set_ylabel('Y label')
        
        x = np.linspace(-4, 4)
        self.ax.set_title('hello record_sampler!')
        self.ax.plot(x, np.sin(x), label='sin(x)')
        
        self.ax.legend()
        self.graph = FigureCanvasKivyAgg(self.fig)
        self.add_widget(self.graph)

    # 指定した波形をプロットする
    def plot(self, data:np.ndarray):
        plt.clf()
        plt.close(self.fig)

        self.fig, self.ax = plt.subplots()
        self.ax.clear()
        self.ax.set_xlabel('X label')
        self.ax.set_ylabel('Y label')
        
        self.ax.set_xlim(0, len(data))
        self.ax.set_title('recorded wave')
        self.ax.plot(data)
        
        self.remove_widget(self.graph)
        self.graph = FigureCanvasKivyAgg(self.fig)
        self.add_widget(self.graph)
