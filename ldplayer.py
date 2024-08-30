import emulator

class LDPlayer():
    def __init__(self, ldplayer_dir):
        self.ldplayer_dir = ldplayer_dir

    def list_ldplayer(self):
        result = {}
        ld = emulator.LDPlayer(ldplayer_dir=self.ldplayer_dir)
        data = dict (zip (ld.list_index(), ld.list_name()))
        for key, value in data.items():
            status = ld.emulators[key].is_running()
            port = self.get_adb_port(key)
            result[key] = {"name": f"{value}", "port": f"{port}", "is_running": f"{status}"}
        return result

    def get_adb_port(self,idx):
        return int(idx) * 2 + 5554
    

