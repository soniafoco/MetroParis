from database.DAO import DAO
import networkx as nx
import geopy

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()

        self._fermate = DAO.getAllFermate()
        self._idMap = {}
        for f in self._fermate:
            self._idMap[f.id_fermata] = f

        self._idMapLinee = {}
        self._linee = DAO.getAllLinee()
        for l in self._linee:
            self._idMapLinee[l.id_linea] = l

    def buildGraph(self):
        self._grafo.add_nodes_from(self._fermate)
        self.addEdge3()

    def buildGraphPesato(self):
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgePesati()

    def addEdge1(self):
    # Soluzione 1: doppio loop sui nodi e query per ogni arco --> da EVITARE per numeri elevati di nodi --> complessità troppo elevata (itera 616*616 volte)
        for u in self._fermate:
            for v in self._fermate:
                result = DAO.getEdge(u, v) #verifica se c'è una connessione (cioè devo inserire un arco) tra i due nodi
                if len(result)>0:
                    self._grafo.add_edge(u,v)
                    print(f"Added edge from {u} to {v}")


    def addEdge2(self):
    # Soluzione 2: singolo loop sui nodi e query su ogni vertice che restituisce una lista di connessioni --> itera 616 volte
        for u in self._fermate:
            vicini = DAO.getEdgeVicini(u)
            for v in vicini:
                v_nodo = self._idMap[v.id_stazA]
                self._grafo.add_edge(u, v_nodo)
                print(f"Added edge from {u} to {v_nodo}")


    # Soluzione 3: nessun loop sui nodi e una query unica che legge tutte le connessioni
    def addEdge3(self):
        allConnessioni = DAO.getAllConnessioni()
        print(f"Numero totale di connessioni (anche duplicate): {len(allConnessioni)}")
        for c in allConnessioni:
            u_nodo = self._idMap[c.id_stazP]  # nodo partenza
            v_nodo = self._idMap[c.id_stazA]  # nodo arrivo
            linea = self._idMapLinee[c.id_linea]
            peso = self.getTraversalTime(u_nodo, v_nodo, linea)

            if self._grafo.has_edge(u_nodo, v_nodo):
                if self._grafo[u_nodo][v_nodo]["weight"] > peso:
                    self._grafo[u_nodo][v_nodo]["weight"] = peso
            else:
                self._grafo.add_edge(u_nodo, v_nodo, weight=peso)
            #self._grafo.add_edge(u_nodo, v_nodo)
            #print(f"Added edge from {u_nodo} to {v_nodo}")


    def addEdgePesati(self):
        print(self._grafo)
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            if self._grafo.has_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA]):
                self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]["weight"] += 1
            else:
                self._grafo.add_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA], weight=1)
        print(self._grafo)

    # Breadth First Search --> (da usare per trovare i cammini minimi)
    def getBFSNodes(self, source):
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    # Depth First Search --> percorsi lunghi (da usare se si cerca la componente connessa)
    def getDFSNodes(self, source):
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    def getBestPath(self, v0, v1):
        cost, path = nx.single_source_dijkstra_path(self._grafo, v0, v1)
        return cost, path


    @property
    def fermate(self):
        return self._fermate

    def getNumNodes(self):
        return len(self._grafo.nodes())

    def getNumEdges(self):
        return len(self._grafo.edges())

    def getArchiPesoMaggioreUno(self):
        if len(self._grafo.edges) == 0:
            print("Il grafo è vuoto")
            return
        edges = self._grafo.edges()
        result = []
        for u,v in edges:
            peso = self._grafo[u][v]['weight']
            if peso > 1:
                result.append((u, v, peso))
        return result

    def getEdgeWeight(self, v1, v2):
        return self._grafo[v1][v2]["weigth"]

    def getTraversalTime(self, v1, v2, linea):
        posizione1 = (v1.coordX, v1.coordY)
        posizione2 = (v2.coordX, v2.coordY)
        distanza = geopy.distance.distance(posizione1, posizione2).km
        velocita = linea.velocita
        tempo = distanza/velocita * 60 #minuti
        return tempo
