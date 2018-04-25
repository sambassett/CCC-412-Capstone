from pyo import *
from datetime import datetime as dt
import random
import math
import copy

class CustomSound:
    timeStarted = 0
    def generate(self): raise NotImplementedError
    def mutate(self): raise NotImplementedError
    def __deepcopy__(self): raise NotImplementedError

class CustomBlit(CustomSound):
    def __init__(self):
        self.sine = generateSine()
        self.adsr = generateAdsr()
        self.blit = Blit(freq = generatePitch(), harms = self.sine, mul = self.adsr)

    def initWithValues(self, blitFreq, sineFreq, sineMul, sineAdd, attack, decay, sustain, release):
        self.sine = Sine(freq = sineFreq, mul = sineMul, add = sineAdd)
        self.adsr = Adsr(attack = attack, decay = decay, sustain = sustain, release = release, dur = 4, mul = 0.1)
        self.blit = Blit(freq = blitFreq, harms = self.sine, mul = self.adsr)

    def initWithArray(self, array):
        self.sine = Sine(freq = array[1], mul = array[2], add = array[3])
        self.adsr = Adsr(attack = array[4], decay = array[5], sustain = array[6], release = array[7], dur=4, mul=0.1)
        self.blit = Blit(freq = array[0], harms=self.sine, mul=self.adsr)

    def __deepcopy__(self, memodict={}):
        customBlit = CustomBlit()
        customBlit.sine.freq = copy.copy(self.sine.freq)
        customBlit.sine.phase = copy.copy(self.sine.phase)
        customBlit.sine.mul = copy.copy(self.sine.mul)
        customBlit.sine.add = copy.copy(self.sine.add)
        customBlit.adsr.attack = copy.copy(self.adsr.attack)
        customBlit.adsr.decay = copy.copy(self.adsr.decay)
        customBlit.adsr.sustain = copy.copy(self.adsr.sustain)
        customBlit.adsr.release = copy.copy(self.adsr.release)
        customBlit.adsr.mul = copy.copy(self.adsr.mul)
        customBlit.adsr.add = copy.copy(self.adsr.add)
        customBlit.adsr.exp = copy.copy(self.adsr.exp)
        customBlit.blit = Blit(freq = copy.copy(self.blit.freq), harms = customBlit.sine, mul = customBlit.adsr)
        return customBlit

    def __str__(self):
        strToReturn = ("Blit freq: " + str(self.blit.freq) + "\nSine freq: " + str(self.sine.freq) + "\nSine mul: " + str(self.sine.mul) +
                        "\nSine add: " + str(self.sine.add) + "\nAttack: " + str(self.adsr.attack) + "\nDecay: " + str(self.adsr.decay) +
                        "\nSustain: " + str(self.adsr.sustain) + "\nRelease: " + str(self.adsr.release))
        return strToReturn

    def toArray(self):
        return [self.blit.freq, self.sine.freq, self.sine.mul, self.sine.add, self.adsr.attack, self.adsr.decay,
                self.adsr.sustain, self.adsr.release]

    def generate(self):
        #print("Blit generated.")
        self.sine = generateSine()
        self.adsr = generateAdsr()
        self.blit = Blit(freq = generatePitch(), harms = self.sine, mul = self.adsr)
        #self.printData()
        return self

    # Change to mutateReplace
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

    def mutate(self):
        self.blit.freq = checkMutate(self.blit.freq, mutatePitch(self.blit.freq), 25, "Pitch")

        newFreq = checkMutate(self.sine.freq, mutateFreq(self.sine.freq), 25, "Sine Freq")
        newRange = checkMutate((self.sine.add - self.sine.mul, self.sine.add + self.sine.mul), mutateRange(self.sine.mul, self.sine.add), 25, "Sine Range")
        self.sine = Sine(freq = newFreq).range(newRange[0], newRange[1])
        self.blit.harms = self.sine

        self.adsr.attack = checkMutate(self.adsr.attack, mutateAttackOrDecay(self.adsr.attack), 25, "Attack")
        self.adsr.decay = checkMutate(self.adsr.decay, mutateAttackOrDecay(self.adsr.decay), 25, "Decay")
        self.adsr.sustain = checkMutate(self.adsr.sustain, mutateSustain(self.adsr.sustain), 25, "Sustain")
        self.adsr.release = checkMutate(self.adsr.release, mutateRelease(self.adsr.release), 25, "Release")
        self.blit.mul = self.adsr

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
        self.timeStarted = dt.now()
        self.adsr.play()

    def isPlaying(self):
        return (dt.now() - self.timeStarted).total_seconds() < self.adsr.dur

    def printData(self):
        print("Pitch: freq= %.3f" % self.blit.freq)
        print("Sine: freq= %.3f" % self.sine.freq, "range= %d - %d" % (self.sine.add - self.sine.mul, self.sine.add + self.sine.mul))
        print("ADSR: att= %.3f" % self.adsr.attack, ", dec= %.3f" % self.adsr.decay, ", sus= %.3f" % self.adsr.sustain,
              ", rel= %.3f" % self.adsr.release, "\n")

def generateSine():
    #random.seed(datetime.now())
    #rangeType = random.randint(1, 10)
   # rangeMin = 0
    #rangeMax = 0
   # if rangeType > 4:
    rangeMin = random.randint(2, 40)
    rangeMax = rangeMin + random.randint(2, 40)
   # elif rangeType > 1:
   #     rangeMin = random.randint(-25, -5)
   #     rangeMax = random.randint(5, 25)
   # else:
   #     rangeMin = random.randint(-25, 10)
   #     rangeMax = rangeMin * -1

    if random.randint(1, 10) < 3:
        sine = Sine(freq = 0).range(rangeMin, rangeMax)
    else:
        sine = Sine(freq = random.uniform(.1, 4)).range(rangeMin, rangeMax)
    #sine = Sine(freq = random.uniform(.1, 4), mul = random.uniform(.05, 5), add = random.uniform(1, 10)) use this one
    #sine = Sine(freq = 2, mul = random.uniform(.05, 3), add = random.uniform(1, 10))
    #sine = Sine(freq = .4, mul = .3, add = 2)
    return sine

def generateAdsr():
    #random.seed(datetime.now())
    adsr = Adsr(attack = random.uniform(0.3, 1.5), decay = random.uniform(0.3, 1.5),
                sustain = random.uniform(0.4, 0.9), release = random.uniform(0.3, 1),
                dur = 4, mul = .1)
    return adsr

def generatePitch():
    #random.seed(datetime.now())
    return random.uniform(70, 400)

def mutateFreq(freq):
    if freq == 0:
        return 0
    else:
        mutateBy = random.uniform(-.5, .5)

        if freq + mutateBy <= .3:
            return .3
        elif freq + mutateBy >= 4:
            return 4
        else:
            return freq + mutateBy

def mutateAttackOrDecay(value):
    mutateBy = random.uniform(-.5, .5)

    if value + mutateBy <= .1:
        return .1
    elif value + mutateBy >= 1.5:
        return 1.5
    else:
        return value + mutateBy


def mutateSustain(sustain):
    mutateBy = random.uniform(-.1, .1)

    if sustain + mutateBy <= .4:
        return .4
    elif sustain + mutateBy >= .9:
        return .9
    else:
        return sustain + mutateBy


def mutateRelease(release):
    mutateBy = random.uniform(-.2, .2)

    if release + mutateBy <= .3:
        return .3
    elif release + mutateBy >= 1:
        return 1
    else:
        return release + mutateBy

def mutatePitch(pitch):
    mutateBy = random.randint(-100, 100)

    if pitch + mutateBy <= 70:
        return 70
    elif pitch + mutateBy >= 400:
        return 400
    else:
        return pitch + mutateBy

def mutateRange(mul, add):
    rangeMin = add - mul
    rangeMax = add + mul

    mutateMin = random.randint(-10, 10)
    mutateMax = random.randint(-10, 10)

    if rangeMin + mutateMin <= 2:
        rangeMin = 2
    elif rangeMin + mutateMin <= rangeMax:
        rangeMin = rangeMin + mutateMin

    if rangeMax + mutateMax >= 80:
        rangeMax = 80
    elif rangeMax + mutateMax >= rangeMin:
        rangeMax = rangeMax + mutateMax

    return rangeMin, rangeMax

def oldmutateRange(mul, add):
    rangeMin = add - mul
    rangeMax = add + mul

    if rangeMin == rangeMax * -1:
        mutateBy = random.randint(-10, 10)
        rangeMin = rangeMin + mutateBy
        rangeMax = rangeMax - mutateBy
    elif rangeMin < 0:
        mutateMin = random.randint(-10, 10)
        mutateMax = random.randint(-10, 10)

        if rangeMin + mutateMin <= -25:
            rangeMin = -25
        elif rangeMin + mutateMin >= -5:
            rangeMin = -5
        else:
            rangeMin = rangeMin + mutateMin

        if rangeMax + mutateMax >= 25:
            rangeMax = 25
        elif rangeMax + mutateMax <= 5:
            rangeMax = 5
        else:
            rangeMax = rangeMax + mutateMax
    else:
        mutateMin = random.randint(-10, 10)
        mutateMax = random.randint(-10, 10)

        if rangeMin + mutateMin <= 2:
            rangeMin = 2
        elif rangeMin + mutateMin >= 10:
            rangeMin = 10
        else:
            rangeMin = rangeMin + mutateMin

        if rangeMax + mutateMax >= 25:
            rangeMax = 25
        elif rangeMax + mutateMax <= 15:
            rangeMax = 15
        else:
            rangeMax = rangeMax + mutateMax

    return rangeMin, rangeMax

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