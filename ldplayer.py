import emulator

class LDPlayer():
    def __init__(self, ldplayer_dir):
        self.ldplayer_dir = ldplayer_dir

    def list_ldplayer(self):
        ld = emulator.LDPlayer(ldplayer_dir=self.ldplayer_dir)
        return ld.emulators