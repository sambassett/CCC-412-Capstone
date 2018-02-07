from pyo import *
import random

s = Server().boot()
freq = 263.74 # Middle C
#amp = Fader(fadein = 2, fadeout = 2, dur = 0).play()
adsr = Adsr(attack = random.uniform(.1, .3), decay = random.uniform(.1, .3), sustain = random.uniform(.6, .8), release = random.uniform(.5, 1.5), dur = 3, mul = 0.2)
#adsr = Adsr(attack = 0.5, decay = 0.5, sustain = 1, release = 1, dur = 3, mul = 0.5)
#adsr.setExp(1.25)
#print(str(adsr.attack) + ", " + str(adsr.decay) + ", " + str(adsr.sustain) + ", " + str(adsr.release) + ", " + str(adsr.dur + adsr.release))

opt = int(input("0 for random, or 1-8 for sound"))

if (random.randint(1, 100) > 25 and opt == 0) or 0 < opt < 6: # Generate tone
    rand = random.randint(1, 100)

    if (rand > 80 and opt == 0) or opt == 1: # Generate impulse train (1)
        osc = Sine(.1).range(1, 50)
        sound = Blit(freq = freq, harms = osc, mul = adsr).mix(2).out()

    elif (rand > 60 and opt == 0) or opt == 2: # Generate frequency modulation (2)
        table = LinTable([(0, 3), (20, 40), (300, 10), (1000, 5), (8191, 3)])
        sound = FM(carrier = [freq, freq - 1, freq - 2], ratio = [.2498, .2503], index = TrigEnv(Metro(.5).play(), table, dur = .5), mul = adsr).mix(2).out() # Randomize parameters?

    elif (rand > 40 and opt == 0) or opt == 3: # Generate Supersaw (3)
        osc = Sine([.4, .3]).range(1, 10)
        sound = SuperSaw(freq = [freq, freq + 50], detune = osc, mul = adsr).mix(2).out()

    elif (rand > 20 and opt == 0) or opt == 4: # Generate sine loop (4)
        osc = Sine(.25, 0, .1, .1)
        sound = SineLoop(freq = [freq, freq + 50], feedback = osc, mul = adsr).mix(2).out()

    else: # Generate phase incrementor (5)
        osc = Phasor(freq = [1.2, 1.2], mul = 1000, add = 500)
        sound = Sine(freq = osc, mul = adsr).out()

else: # Generate noise
    rand = random.randint(1, 100)

    if (rand > 66 and opt == 0) or opt == 6: # Generate white noise (6)
        sound = Noise(adsr).mix(2).out()

    elif (rand > 33 and opt == 0) or opt == 7: # Generate pink noise (7)
        sound = PinkNoise(adsr).mix(2).out()

    else: # Generate brown noise (8)
        sound = BrownNoise(adsr).mix(2).out()

# Displays waveform and spectrum
sc = Scope(sound)
sp = Spectrum(sound)

pat = Pattern(adsr.play, time=4.5).play()

s.gui(locals())