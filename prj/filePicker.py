from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser, FileChooserListView

# wavファイルをブラウザする
class FilePicker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_selected_sound(self):
        if(not len(self.ids["list_view"].selection) is 0):
            idx = int(self.ids["pad_idx"].text)
            path = self.ids["list_view"].selection[0]
            self.parent.set_sound(idx, path)
