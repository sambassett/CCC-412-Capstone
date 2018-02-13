from CustomSound import *

s = Server().boot()

blit = CustomBlit().generate()
sound = blit.getSound()
sound = sound.mix(2)
sound.out()

s.start()

pat2 = Pattern(blit.mutate, time=6).play()
pat1 = Pattern(blit.playAdsr, time=6).play()

# Displays waveform and spectrum
sc = Scope(sound)
sp = Spectrum(sound)

s.gui(locals())