from codePeda.utilities.Mqtt.clientMqtt import ClientMqtt


class Gateway:

    def __init__(self):
        self.clientMqtt = ClientMqtt()
        self.clientScanner = ClientScanner()
        self.clientScanner.add_observateur(self.clientMqtt)
        self.clientMqtt.add_observer(self.clientScanner)
        self.clientMqtt.serveur = "192.168.0.2"
        self.clientMqtt.port = 456
        self.clientMqtt.set_nom("Pi0")
        self.clientMqtt.connection()
        self.clientScanner.start()
        self.clientMqtt.start()

    def run(self):
        self.clientScanner.unstop()
        self.clientMqtt.unstop()


if __name__ == '__main__':
    G = Gateway()

    G.run()
