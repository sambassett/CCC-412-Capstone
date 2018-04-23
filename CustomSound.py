from pyo import *
from datetime import datetime
import random
import math
import copy

class CustomSound:

    def generate(self): raise NotImplementedError
    def mutate(self): raise NotImplementedError
    def __deepcopy__(self): raise NotImplementedError

class CustomBlit(CustomSound):
    def __init__(self):
        self.sine = generateSine()
        self.adsr = generateAdsr()
        self.blit = Blit(freq = generatePitch(), harms = self.sine, mul = self.adsr)

    def __deepcopy__(self, memodict={}):
        customBlit = CustomBlit()
        customBlit.sine.freq = copy.copy(self.sine.freq)
        customBlit.sine.mul = copy.copy(self.sine.mul)
        customBlit.sine.add = copy.copy(self.sine.add)
        customBlit.adsr.attack = copy.copy(self.adsr.attack)
        customBlit.adsr.decay = copy.copy(self.adsr.decay)
        customBlit.adsr.sustain = copy.copy(self.adsr.sustain)
        customBlit.adsr.release = copy.copy(self.adsr.release)
        customBlit.blit = Blit(freq = copy.copy(self.blit.freq), harms = customBlit.sine, mul = customBlit.adsr)
        return customBlit

    def generate(self):
        #print("Blit generated.")
        self.sine = generateSine()
        self.adsr = generateAdsr()
        self.blit = Blit(freq = generatePitch(), harms = self.sine, mul = self.adsr)
        #self.printData()
        return self

    def mutateSelf(self):
        newSine = generateSine()
        self.sine.freq = checkMutate(self.sine.freq, newSine.freq, 50, "Sine freq")
        self.sine.mul = checkMutate(self.sine.mul, newSine.mul, 50, "Sine mul")
        self.sine.add = checkMutate(self.sine.add, newSine.add, 50, "Sine add")

        newAdsr = generateAdsr()
        self.adsr.attack = checkMutate(self.adsr.attack, newAdsr.attack, 50, "Attack")
        self.adsr.decay = checkMutate(self.adsr.decay, newAdsr.decay, 50, "Decay")
        self.adsr.sustain = checkMutate(self.adsr.sustain, newAdsr.sustain, 50, "Sustain")
        self.adsr.release = checkMutate(self.adsr.release, newAdsr.release, 50, "Release")
        #self.adsr.dur = checkMutate(self.adsr.dur, newAdsr.dur, 25, "ADSR dur")
        #self.adsr.mul = checkMutate(self.adsr.mul, newAdsr.mul, 25, "ADSR mul")

        #newPitch = generatePitch()
        #newFreq = checkMutate(self.blit.freq, generateFreq(), 25, "Freq")
        self.blit = Blit(freq = self.blit.freq, harms = self.sine, mul = self.adsr)
        #self.blit = Blit(freq = newPitch, harms = self.sine, mul = self.adsr)
        #self.printData()
        return self

    def mutateCopy(self):
        newSound = self
        newSine = generateSine()
        self.sine.freq = checkMutate(self.sine.freq, newSine.freq, 50, "Sine freq")
        self.sine.mul = checkMutate(self.sine.mul, newSine.mul, 50, "Sine mul")
        self.sine.add = checkMutate(self.sine.add, newSine.add, 50, "Sine add")

        newAdsr = generateAdsr()
        self.adsr.attack = checkMutate(self.adsr.attack, newAdsr.attack, 50, "Attack")
        self.adsr.decay = checkMutate(self.adsr.decay, newAdsr.decay, 50, "Decay")
        self.adsr.sustain = checkMutate(self.adsr.sustain, newAdsr.sustain, 50, "Sustain")
        self.adsr.release = checkMutate(self.adsr.release, newAdsr.release, 50, "Release")
        # self.adsr.dur = checkMutate(self.adsr.dur, newAdsr.dur, 25, "ADSR dur")
        # self.adsr.mul = checkMutate(self.adsr.mul, newAdsr.mul, 25, "ADSR mul")

        # newFreq = checkMutate(self.blit.freq, generateFreq(), 25, "Freq")
        self.blit = Blit(freq=self.blit.freq, harms=self.sine, mul=self.adsr)
        #self.printData()
        return self

    def getSound(self):
        return self.blit

    def playADSR(self):
        self.adsr.play()

    def printData(self):
        print("Pitch: freq= %.3f" % self.blit.freq)
        print("Sine: freq= %.3f" % self.sine.freq, ", mul= %.3f" % self.sine.mul, ", add= %.3f" % self.sine.add)
        print("ADSR: att= %.3f" % self.adsr.attack, ", dec= %.3f" % self.adsr.decay, ", sus= %.3f" % self.adsr.sustain,
              ", rel= %.3f" % self.adsr.release, "\n")

def generateSine():
    #random.seed(datetime.now())
    sine = Sine(freq = random.uniform(.1, 4)).range(1, random.randint(5, 50))
    #sine = Sine(freq = random.uniform(.1, 4), mul = random.uniform(.05, 5), add = random.uniform(1, 10)) use this one
    #sine = Sine(freq = 2, mul = random.uniform(.05, 3), add = random.uniform(1, 10))
    #sine = Sine(freq = .4, mul = .3, add = 2)
    return sine

def generateAdsr():
    #random.seed(datetime.now())
    adsr = Adsr(attack = random.uniform(0.1, 2.0), decay = random.uniform(0.1, 2.0),
                sustain = random.uniform(0.2, 0.9), release = random.uniform(0.2, 3.0),
                dur = 4, mul = .1)
    return adsr

def generatePitch():
    #random.seed(datetime.now())
    return random.uniform(50, 550)

def generateMul():
    #random.seed(datetime.now())
    return random.uniform(.3, .6)

def generateTable(tableType):
    #random.seed(datetime.now())
    if tableType == "sawtooth":
        return SawTable(order = random.randint(9, 12)).normalize()
    elif tableType == "sinc":
        return SincTable(freq = math.pi * random.randint(1, 8), windowed = True)
    elif tableType == "square":
        return SquareTable(order = random.randint(9, 12)).normalize()
    elif tableType == "harm":
        return HarmTable([random.uniform(.100, 1), 0, random.uniform(.100, 1), 0, random.uniform(.100, 1), 0,
                          random.uniform(.100, 1), 0, random.uniform(.100, 1), 0, random.uniform(.100, 1)])

def checkMutate(initial, target, chance, name):
    #random.seed(datetime.now())
    rand = random.randint(1, 100)
    #print(rand)
    if rand < chance:
        print("--", name, "mutated.")
        return target
    else:
        return initial