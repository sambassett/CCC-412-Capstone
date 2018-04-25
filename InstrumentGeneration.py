import pygame.midi
import pygame.key
import pygame.mixer
import pygame.mouse
import pygame.midi
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
import KivyLayout
from SystemVolume import SystemVolume
from CustomSound import *
from GetHWNDs import win32gui, get_hwnds

Builder.load_string(KivyLayout.getLayout())

class RootWidget(FloatLayout):
    notificationLabel = StringProperty()
    selectionLabel = StringProperty()
    generateAndSaveDisabled = BooleanProperty()
    testDisabled = BooleanProperty()

    def changeNotificationLabel(self, text):
        print(str(text))
        self.notificationLabel = text

    def changeSelectionLabel(self, text):
        self.selectionLabel = text

    def toggleGenerateAndSaveDisabled(self, disabled):
        self.generateAndSaveDisabled = disabled

    def toggleTestDisabled(self, disabled):
        self.testDisabled = disabled

class InstrumentGeneration(App):
    title = 'Instrument Generation'
    server = Server(winhost = 'directsound', duplex = 0, midi = 'jack').boot().start()
    systemVolume = SystemVolume()
    pygame = pygame

    documentsPath = os.path.join(os.path.expanduser("~"), "My Documents", "pyosounds")
    desktopPath = os.path.join(os.path.expanduser("~"), "Desktop", "Saved Sounds")

    if not os.path.exists(documentsPath):
        os.makedirs(documentsPath)
    if not os.path.exists(desktopPath):
        os.makedirs(desktopPath)

    baseHz = 16.35
    aConst = 1.059463094359

    pyoSounds = []
    soundsToRecord = []
    soundRecords = []
    playableSounds = []
    savedSounds = 1
    soundsSelected = [False, False, False, False, False, False]

    for i in range(0, 6):
        pyoSounds.append(CustomBlit())

    mainSound = pyoSounds[0]
    playSound = mainSound.getSound()

    def build(self):
        #rootWidget.changeSelectionLabel("No sounds are selected.")
        return RootWidget()

    def updateNotificationLabelWithClear(self, text, timer):
        if self.root is not None:
            self.root.changeNotificationLabel(str(text))
            Clock.schedule_once(self.clearNotificationLabel, timer)
            print("clear in 4")

    def updateNotificationLabelWithoutClear(self, text):
        if self.root is not None:
            self.root.changeNotificationLabel(str(text))

    def clearNotificationLabel(self, elapsedTime):
        if self.root is not None:
            self.root.changeNotificationLabel("")

    def play_sound(self, index):
        self.mainSound = self.pyoSounds[index]
        self.playSound = self.mainSound.getSound().mix(2)
        self.playSound.out()
        print("Sound " + str(index + 1) + ":")
        self.mainSound.printData()
        self.mainSound.playADSR()


    def setPygameHWND(self):
        ownHWND = ""
        for hwnd in get_hwnds():
            if win32gui.GetWindowText(hwnd) == "Instrument Generation":
                ownHWND = hwnd

        os.environ['SDL_WINDOWID'] = str(ownHWND)

    def saveSoundsToDesktop(self):
        self.soundsToRecord = []
        self.soundRecords = []

        for index in range(0, len(self.soundsSelected)):
            if self.soundsSelected[index]:
                self.soundsToRecord.append(copy.deepcopy(self.pyoSounds[index]))

        for i in range(0, len(self.soundsToRecord)):
            print("Rec " + str(i))
            playSound = self.soundsToRecord[i].getSound().out()
            playSound = playSound.mix(2)
            self.soundsToRecord[i].playADSR()
            self.soundRecords.append(Record(playSound, filename = self.desktopPath + "\\generatedSound" + str(self.savedSounds) + ".wav", chnls=2, fileformat=0, sampletype=0))
            self.savedSounds += 1

        saveVolume = self.systemVolume.getSystemVolume()
        self.systemVolume.setSystemVolume(-60.0)

        for i in range(0, len(self.soundRecords)):
            clean = Clean_objects(4, self.soundRecords[i])
            clean.start()

        time.sleep(4)

        self.updateNotificationLabelWithClear("Save complete.", 8)
        self.systemVolume.setSystemVolume(saveVolume)

    # If the same sound as before is being played (no generations between, same position), don't re-record
    def recordSoundsForPlayback(self):
        self.soundsToRecord = [None] * 108
        self.soundRecords = [None] * 108

        for i in range(0, 108):
            self.soundsToRecord[i] = copy.deepcopy(self.mainSound)
            self.soundsToRecord[i].blit.freq = (self.baseHz * (self.aConst**(i)))
            print(str(self.soundsToRecord[i].blit.freq))

        for i in range(0, len(self.soundsToRecord)):
            print("Rec " + str(i))
            playSound = self.soundsToRecord[i].getSound().out()
            playSound = playSound.mix(2)
            self.soundsToRecord[i].playADSR()
            self.soundRecords.append(Record(playSound, filename=self.documentsPath + "\\sound" + str(i) + ".wav", chnls=2, fileformat=0, sampletype=0))

        saveVolume = self.systemVolume.getSystemVolume()
        self.systemVolume.setSystemVolume(-60.0)

        for i in range(0, len(self.soundRecords)):
            clean = Clean_objects(4, self.soundRecords[i])
            clean.start()

        time.sleep(4)

        self.systemVolume.setSystemVolume(saveVolume)
        self.pygame.init()

        print("Reading sound files back in.")
        for i in range(0, len(self.soundsToRecord)):
            soundPath = self.documentsPath + "\\sound" + str(i) + ".wav"
            try:
                self.playableSounds.append(self.pygame.mixer.Sound(soundPath))
            except Exception as e:
                print(e)
        self.pygame.quit()

    def beginKeyboardPlayback(self, unusedTimer):
        self.pygame.init()
        keyboardPlaying = True
        while keyboardPlaying:
            for event in self.pygame.event.get():
                if event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_ESCAPE:
                    self.pygame.quit()
                    keyboardPlaying = False

                elif event.type == self.pygame.MOUSEBUTTONUP:
                    self.pygame.quit()
                    keyboardPlaying = False

                elif event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_a:
                    self.playableSounds[0].play()

                elif event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_s:
                    self.playableSounds[1].play()

                elif event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_d:
                    self.playableSounds[2].play()

                elif event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_f:
                    self.playableSounds[3].play()
        self.clearNotificationLabel(0)
        return

    def beginMidiKeyboardPlayback(self, unusedTimer):
        pygame.init()
        pygame.midi.init()

        midiIn = pygame.midi.Input(1)

        keyboardPlaying = True
        while keyboardPlaying:
            for event in self.pygame.event.get():
                if (event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_ESCAPE) or (event.type == self.pygame.MOUSEBUTTONUP):
                    self.pygame.quit()
                    keyboardPlaying = False

            if midiIn.poll():
                for press in midiIn.read(1000):
                    print("press")
                    noteDown = (press[0][0] == 144)
                    noteVal = press[0][1]
                    print(noteVal)
                    # Sanitize input better!! THe modulation does weird stuff
                    if noteVal >= 0 and noteVal <= 107 and noteDown:
                        self.playableSounds[noteVal].play()
                    elif noteVal >= 0 and noteVal <= 107 and not noteDown:
                        self.playableSounds[noteVal].fadeout(1250)
            pygame.time.wait(20)

        self.clearNotificationLabel(0)
        return

    def testInstrument(self):
        self.setPygameHWND()

        self.recordSoundsForPlayback()

        print("About to start keyboard input.")
        self.updateNotificationLabelWithoutClear("Piano ready! Click anywhere or press ESC to leave piano mode.")
        Clock.schedule_once(self.beginMidiKeyboardPlayback, 1/10)

    def randomizeSounds(self):
        for i in range(0, len(self.pyoSounds)):
            self.pyoSounds[i] = CustomBlit()
        self.updateNotificationLabelWithClear("Sounds have been randomized.", 4)

    def generateFromSounds(self):
        soundsToClone = []

        for index in range(0, len(self.pyoSounds)):
            if self.soundsSelected[index]:
                soundsToClone.append(self.pyoSounds[index])

        print(str(len(soundsToClone)) + " sounds selected to breed.")

        cloneSounds = list(map(copy.deepcopy, soundsToClone))
        offspring = []

        for index in range(0, len(self.pyoSounds)):
            offspring.append(self.soundCrossover(cloneSounds))
            offspring[index].mutate()
            print("Offspring " + str(index) + " bred.")

        self.pyoSounds = offspring
        self.updateNotificationLabelWithClear("Generation complete.", 4)

    def soundCrossover(self, sounds):
        soundArrays = []
        newOffspringArray = []
        for sound in sounds:
            soundArrays.append(sound.toArray())

        for paramInd in range(0, 8):
            sourceSoundInd = random.randint(0, len(sounds) - 1)

            newOffspringArray.append(soundArrays[sourceSoundInd][paramInd])

        soundToReturn = CustomBlit()
        soundToReturn.initWithArray(newOffspringArray)
        return soundToReturn

    def on_checkbox_active(self, value, index):
        self.soundsSelected[index] = value
        #self.updateSelectionLabel()

        print("Checkbox " + str(index) + "  pressed.")

        if self.root is not None:
            if True in self.soundsSelected:
                self.root.toggleGenerateAndSaveDisabled(False)

                if self.soundsSelected.count(True) == 1:
                    self.root.toggleTestDisabled(False)
                else:
                    self.root.toggleTestDisabled(True)
            else:
                self.root.toggleGenerateAndSaveDisabled(True)
                self.root.toggleTestDisabled(True)

    def updateSelectionLabel(self):
        selectedIndices = []

        for index in range(0, len(self.soundsSelected)):
            if self.soundsSelected[index]:
                selectedIndices.append(index)

        size = len(selectedIndices)

        if size > 0:
            buildStr = "Sound"

            if size > 1:
                buildStr += "s"

            for index in range(0, size):
                if index == size - 1 and size > 1:
                    buildStr += " and " + str(index + 1)
                elif size > 2:
                    buildStr += " " + str(index + 1) + ","
                else:
                    buildStr += " " + str(index + 1)
        else:
            buildStr = "No sounds"

        if size != 1:
            buildStr += " are selected."
        else:
            buildStr += " is selected."

        if self.root is not None:
            self.root.changeSelectionLabel(str(buildStr))

if __name__ == '__main__':
    InstrumentGeneration().run()
