import threading

import paho.mqtt.client as paho
from getmac import get_mac_address as gma

from utilities.observable.ObservableInterface import ClientObservable
from utilities.observateur.Observateur import Observer
from utilities.singleton.singleton import SingletonMeta


class ClientMqtt(Observer, ClientObservable, threading.Thread):
    __metaclass__ = SingletonMeta

    def __init__(self, parent=None):
        super(ClientMqtt, self).__init__()
        threading.Thread.__init__(self)
        self.nom = "DefaultClientMqtt"
        self.mac = gma()
        self.serveur = "127.0.0.1"
        self.port = 8080
        self.client = paho.Client(self.nom)

        self.Debug = True
        self.__go = False

    def update(self, subject: ClientObservable) -> None:
        if False:
            print(
                f"update de : {subject.nom} \n Evènement recu :{subject.event} \n message : {subject.message} \nvaleurs : {subject.valeurs}")
        self.publish(f"{self.mac}", str(subject.message))

    def onpublish(self, client, userdata, result) -> None:
        if self.Debug:
            # print(f"Message publié de : {client} avec les données : {userdata}, renvoyant le resultat : {result}")
            pass
        else:
            pass

    def set_nom(self, nom):
        self.client._client_id = nom
        self.nom = nom

    def connection(self) -> None:

        self.client.connect(self.serveur, self.port, keepalive=3600)
        self.client.on_publish = self.onpublish
        self.client.on_message = self.onmessage
        self.client.subscribe(f"{self.mac}/param/#")

    def publish(self, topic=None, payload):
        if self.Debug:
            print(f"Topic : {topic}, charge utile = {payload}")
        if topic:
            self.client.publish(topic=f'{self.mac}/{topic}', payload=payload)
        else:
            self.client.publish(topic=self.mac, payload=payload)

    def onmessage(self, client, userdata, message):
        # print("Message recu")
        self.valeurs = message.payload
        self.event = message.topic
        if f"{self.mac}/param/" in message.topic:
            print("message de param : ", message.payload)
        self.notify_observer(message.topic)

    def unstop(self):
        self.__go = True

    def stop(self):
        self.__go = False

    def run(self):
        while 1:
            if self.__go:
                self.client.loop_read()
