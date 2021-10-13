import mysql.connector

from utilities.singleton.singleton import SingletonMeta


class ClientMysql():
    __metaclass__ = SingletonMeta

    def __init__(self):
        self.client = mysql.connector.connect(host="localhost", user="root", password="root", database="dossier")
        self.cursor = self.client.cursor()

    def ajout_rssi(self, gate, dev, rssi):
        sql = f"Insert into rssi (Gateway,device,rssi) values ('{gate}','{dev}','{rssi}')"
        self.cursor.execute(sql)
        self.client.commit()
