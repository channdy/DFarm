import emulator

class LDPlayer():
    def __init__(self, ldplayer_dir):
        self.ldplayer_dir = ldplayer_dir

    def list_ldplayer(self):
        ld = emulator.LDPlayer(ldplayer_dir=self.ldplayer_dir)
        print(ld.list_name())
        # for em in ld.emulators:
            # print(em.list_name())
        # return ld.emulators