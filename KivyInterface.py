from kivy.app import App
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from CustomSound import *
import copy


class MyApp(App):
    title = 'Instrument Generation'

    server = Server().boot().start()

    soundsList = []
    for i in range(0, 9):
        soundsList.append(CustomBlit().generate())

    mainSound = soundsList[0]
    playSound = mainSound.getSound()

    def build(self):
        self.root = Builder.load_file('layout.kv')
        return self.root

    @staticmethod
    def play_sound_from_file():
        sound = SoundLoader.load('Images/Wilhelm Scream.wav')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()

    def play_sound(self, index):
        self.mainSound = self.soundsList[index]
        self.playSound = self.mainSound.getSound().mix(2)
        self.playSound.out()
        print("Sound " + str(index + 1) + ":")
        self.mainSound.printData()
        self.mainSound.playADSR()

    def newGeneration(self, index):
        saveSound = copy.deepcopy(self.soundsList[index])
        newSoundsList = self.soundsList
        for i in range(0, 9):
            newSoundsList[i] = copy.deepcopy(saveSound)
            print("Sound " + str(i + 1) + ":")
            newSoundsList[i].mutateSelf()
        self.soundsList = newSoundsList

    def on_checkbox_active(self, value, index):
        if value:
            # add index to breeding list
            # remove print when done, used for debugging
            print("The checkbox is active because value={}".format(value))
        else:
            # remove index from breeding list
            # remove print when done, used for debugging
            print("The checkbox is inactive because value={}".format(value))

if __name__ == '__main__':
    MyApp().run()
