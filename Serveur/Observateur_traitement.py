import threading

from code.utilities.clientBdd.ClientSql import ClientMysql
from code.utilities.observable.ObservableInterface import ClientObservable
from code.utilities.observateur.Observateur import Observer


class Traitement(Observer, threading.Thread):

    def __init__(self):
        super(Traitement, self).__init__()
        self.bdd = ClientMysql()

    def update(self, subject: ClientObservable) -> None:
        val = []
        try:
            val = eval(subject.valeurs.payload.decode())
        except:
            print("Problème de décodage")
            pass

        if len(val) == 2:
            dev = val[0]
            rssi = val[1]
            gate = subject.event
            self.bdd.ajout_rssi(gate, dev, rssi)

    def run(self):
        while 1:
            pass
