# Code from user snippsat at https://python-forum.io/Thread-How-to-change-the-sound-volume-with-python
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class SystemVolume:
    devices = None
    interface = None
    volume = None

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def setSystemVolume(self, volumeLevel):
        self.volume.SetMasterVolumeLevel(c_float(volumeLevel), None)

    def getSystemVolume(self):
        return self.volume.GetMasterVolumeLevel()