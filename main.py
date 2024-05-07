from os import environ
environ['DISPLAY'] = ':0' #set to local display

from kivy.app import App
from kivy.app import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase

kv = Builder.load_file("homescreen.kv")

LabelBase.register(name="Aptos",
                   fn_regular="assets/fonts/aptos/aptos.ttf",
                   fn_bold="assets/fonts/aptos/aptos-bold.ttf",
                   fn_italic="assets/fonts/aptos/aptos-italic.ttf"
                   )                                     

class SolarClock(App):

    def build(self):
        Window.maximize()
        Window.borderless = True
        print(Window.size)
        return kv

if __name__ == '__main__':
    SolarClock().run()