import math
import os
import threading
from fxpmath import Fxp


class Beacon(threading.Thread):

    def __init__(self):
        super(Beacon, self).__init__()
        self.__stop_event = False
        self.passage = True
        self.temp = [0,0]
        self.tension = [0,0]
        self.pdu = [0,0,0,0]
        self.time = [0,0,0,0]
        self.trame = "sudo hcitool -i hci0 cmd 0x08 0x0008 1c 02 01 06 03 03 aa fe 14 16 aa fe 20"


    def set_temp(self,temp):
        x = Fxp(25, signed=True, n_word=16, n_frac=8)
        val = x.hex()
        for i in range(len(val)):
            if val[i] == '':
                val[i] = '00'

        self.temp = [val[2:4],val[4:]]
        self.stop()
        self.unstop()

    def set_tension(self,tension):
        x = Fxp(25, signed=True, n_word=16, n_frac=8)
        val = x.hex()
        for i in range(len(val)):
            if val[i] == '':
                val[i] = '00'

        self.tension = [val[2:4], val[4:]]

    def unstop(self):
        self.__stop_event = True
        self.passage = True

    def stop(self):
        self.__stop_event = False

    def run(self) -> None:
        while 1:
            if self.__stop_event:
                if self.passage:
                    os.system("sudo hciconfig hci0 up")
                    os.system("sudo hciconfig hci0 noleadv")
                    os.system("sudo hciconfig hci0 leadv 3")
                    os.system(f'{self.trame} 00 {self.tension[0]} {self.tension[1]} {self.temp[0]} {self.temp[1]} {self.pdu[0]} {self.pdu[1]} {self.pdu[2]} {self.pdu[3]} {self.time[0]} {self.time[1]} {self.time[2]} {self.time[3]}  ')

                self.passage = False


if __name__ == "__main__":
    B = Beacon()
    B.start()
    B.unstop()
    B.set_temp(25)
    B.join()
