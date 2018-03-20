from kivy.app import App
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

#def WidgetScreen():
#    layout = BoxLayout()
#    btn = Button(text='Hello World')
#    btn2 = Button(text='Goodbye World')
#    layout.add_widget(btn)
#    layout.add_widget(ButtonUpload())
#    return layout

class MyApp(App):
    title = 'Instrument Generation'

    def build(self):
        self.root = Builder.load_file('layout.kv')
        return self.root

    def play_sound(self):
        sound = SoundLoader.load('Images/Wilhelm Scream.wav')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()


if __name__ == '__main__':
    MyApp().run()
