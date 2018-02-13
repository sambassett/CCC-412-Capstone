from pyo import *
import random
import math

class CustomSound:

    def generate(self): raise NotImplementedError
    def mutate(self): raise NotImplementedError

class CustomBlit(CustomSound):
    def __init__(self, sine = 0, adsr = 0, blit = 0):
        self.sine = sine
        self.adsr = adsr
        self.blit = blit

    def generate(self):
        print("Blit generated.")
        self.sine = generateSine()
        self.adsr = generateAdsr()
        self.blit = Blit(freq = generatePitch(), harms = self.sine, mul = self.adsr)
        self.printData()
        return self

    def mutate(self):
        newSine = generateSine()
        self.sine.freq = checkMutate(self.sine.freq, newSine.freq, 25, "Sine freq")
        self.sine.mul = checkMutate(self.sine.mul, newSine.mul, 25, "Sine mul")
        self.sine.add = checkMutate(self.sine.add, newSine.add, 25, "Sine add")

        newAdsr = generateAdsr()
        self.adsr.attack = checkMutate(self.adsr.attack, newAdsr.attack, 25, "Attack")
        self.adsr.decay = checkMutate(self.adsr.decay, newAdsr.decay, 25, "Decay")
        self.adsr.sustain = checkMutate(self.adsr.sustain, newAdsr.sustain, 25, "Sustain")
        self.adsr.release = checkMutate(self.adsr.release, newAdsr.release, 25, "Release")
        #self.adsr.dur = checkMutate(self.adsr.dur, newAdsr.dur, 25, "ADSR dur")
        #self.adsr.mul = checkMutate(self.adsr.mul, newAdsr.mul, 25, "ADSR mul")

        #newFreq = checkMutate(self.blit.freq, generateFreq(), 25, "Freq")
        self.blit = Blit(freq = self.blit.freq, harms = self.sine, mul = self.adsr)
        self.printData()
        return self

    def getSound(self):
        return self.blit

    def playAdsr(self):
        return self.adsr.play()

    def printData(self):
        print("Pitch: freq= %.3f" % self.blit.freq)
        print("Sine: freq= %.3f" % self.sine.freq, ", mul= %.3f" % self.sine.mul, ", add= %.3f" % self.sine.add)
        print("ADSR: att= %.3f" % self.adsr.attack, ", dec= %.3f" % self.adsr.decay, ", sus= %.3f" % self.adsr.sustain,
              ", rel= %.3f" % self.adsr.release, "\n")

def generateSine():
    sine = Sine(freq = random.uniform(.1, 4)).range(1, random.randint(5, 50))
    #sine = Sine(freq = random.uniform(.1, 4), mul = random.uniform(.05, 5), add = random.uniform(1, 10)) use this one
    #sine = Sine(freq = 2, mul = random.uniform(.05, 3), add = random.uniform(1, 10))
    #sine = Sine(freq = .4, mul = .3, add = 2)
    return sine

def generateAdsr():
    adsr = Adsr(attack = random.uniform(0.1, 2.0), decay = random.uniform(0.1, 2.0),
                sustain = random.uniform(0.2, 0.9), release = random.uniform(0.2, 3.0),
                dur = 4, mul = .1)
    return adsr

def generatePitch():
    return random.uniform(50, 600)

def generateMul():
    return random.uniform(.3, .6)

def generateTable(tableType):
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
    if random.randint(1, 100) < chance:
        print("--", name, "mutated.")
        return target
    else:
        return initial