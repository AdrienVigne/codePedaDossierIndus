from code.Serveur.Observateur_traitement import Traitement
from code.utilities.Mqtt.clientMqtt import ClientMqtt
from code.utilities.clientBdd.ClientSql import ClientMysql


class ServeurTraitement:

    def __init__(self):
        super(ServeurTraitement, self).__init__()
        self.clientMQTT = ClientMqtt()
        self.clientMQTT.set_nom("Serveur")
        self.traitement = Traitement()
        self.bdd = ClientMysql()
        self.clientMQTT.serveur = "192.168.0.2"
        self.clientMQTT.port = 456
        self.clientMQTT.add_observer(self.traitement)
        self.clientMQTT.connection()
        self.clientMQTT.client.subscribe('#')

    def run(self):
        self.clientMQTT.start()


if __name__ == '__main__':
    S = ServeurTraitement()
    S.run()
