import emulator

class LDPlayer():
    def __init__(self, ldplayer_dir):
        self.ldplayer_dir = ldplayer_dir
        self.ld = emulator.LDPlayer(ldplayer_dir=self.ldplayer_dir)

    def list_ldplayer(self):
        result = {}
        data = dict (zip (self.ld.list_index(), self.ld.list_name()))
        for key, value in data.items():
            status = self.ld.emulators[key].is_running()
            if status:
                status = "Running"
            else:
                status = "Not running"
            serial = self.get_adb_port(key)
            result[key] = {"name": f"{value}", "status": f"{status}", "serial": f"{serial}"}
        return result

    def get_adb_port(self,idx):
        return f"emulator-{int(idx) * 2 + 5554}"
    
    def start(self, idx):
        em = self.ld.emulators[idx]
        em.start(wait=False)
        em.wait_to_started()
    def quit(self, idx):
        em = self.ld.emulators[idx]
        em.quit()

    def list_packages(self, idx):
        em = self.ld.emulators[idx]
        packages = em.list_packages()
        print(packages)

