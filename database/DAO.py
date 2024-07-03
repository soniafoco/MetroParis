from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connessione
from model.linea import Linea


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(row["id_fermata"], row["nome"], row["coordX"], row["coordY"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    # Metodo per verificare se esiste una connessione tra due nodi (soluzione 1)
    def getEdge(v1, v2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c WHERE c.id_stazP = %s AND c.id_stazA = %s"
        cursor.execute(query, (v1.id_fermata, v2.id_fermata,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    # Metodo per verificare se esiste una connessione tra due nodi (soluzione 2)
    def getEdgeVicini(v):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c WHERE c.id_stazP = %s"
        cursor.execute(query, (v.id_fermata,))

        for row in cursor:
            result.append(Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    # Metodo per leggere tutte le connessioni del database (soluzione 3)
    def getAllConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllLinee():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM linea"
        cursor.execute(query)

        for row in cursor:
            result.append(Linea(**row))
        cursor.close()
        conn.close()
        return result


