import threading

from bluepy.btle import Scanner, DefaultDelegate

from utilities.observable.ObservableInterface import ClientObservable
from utilities.observateur.Observateur import Observer


class ScannerInterface(DefaultDelegate, ClientObservable):

    def __init__(self, Liste=None):
        super(ScannerInterface, self).__init__()
        DefaultDelegate.__init__(self)
        ClientObservable.__init__(self)

        self.deviceToScan = Liste
        self.minRSSI = -60
        self.message_brute = True

    def handleDiscovery(self, scanEntry, isNewDev, isNewData):
        print("SCAN")
        if self.deviceToScan:
            if scanEntry.addr in self.deviceToScan:
                if scanEntry.rssi > self.minRSSI:
                    if self.message_brute:
                        self.message = [scanEntry.addr, scanEntry.rawData]
                    else:
                        self.message = [scanEntry.addr, scanEntry.rssi]
                    self.notify_observer("device_scanned")
        else:
            if self.message_brute:
                self.message = [scanEntry.addr, scanEntry.rawData]
            else:
                self.message = [scanEntry.addr, scanEntry.rssi]
            self.notify_observer("device_scanned")
            print(self.message)


class ClientScanner(threading.Thread, Observer):

    def __init__(self):
        threading.Thread.__init__(self)
        # print("Creation")
        self.ScannerDelegate = ScannerInterface()
        #self.ScannerDelegate = ScannerInterface(['ac:23:3f:a3:33:d8'])
        self.scanner = Scanner().withDelegate(self.ScannerDelegate)
        self.__stop_event = False

    def add_observateur(self, obs: Observer):
        # print(self.__dict__)
        self.ScannerDelegate.add_observer(obs)

    def unstop(self):
        self.__stop_event = True
        print("Lancement")

    def stop(self):
        self.__stop_event = False

    def update(self, subject: ClientObservable) -> None:
        print("update client scanner")
        param = subject.event.split('/')[-1]
        print(param)
        if param == 'add_device':
            new_device = eval(subject.valeurs.decode())
            print(new_device)
            if new_device not in self.ScannerDelegate.deviceToScan:
                self.ScannerDelegate.deviceToScan.append(new_device)
            print(self.ScannerDelegate.deviceToScan)
        if param == 'set_min_rssi':
            rssi = eval(subject.valeurs.decode())
            print('new rssi min :', rssi)
            self.ScannerDelegate.minRSSI = rssi
            print(self.ScannerDelegate.minRSSI)

    def run(self) -> None:
        while 1:
            if self.__stop_event:
                self.scanner.scan()



if __name__ == '__main__':
    S = ClientScanner()
    S.start()
    S.unstop()
