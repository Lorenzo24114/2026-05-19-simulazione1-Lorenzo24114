from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.allGenre=[]
        self._graph = nx.Graph()
        self._allNodes=[]
        self._idMapArtist={}

    def getAllGenre(self):
        self.allGenre=DAO.getAllGenre()
        return self.allGenre


    def buildGraph(self,genreId):
        self._allNodes=DAO.getAllNodes(genreId)
        for a in self._allNodes:
            self._idMapArtist[a.ArtistId] = a
        self._graph.add_nodes_from(self._allNodes)
        self.addEdges()

    def addEdges(self):
        risultato=DAO.getAllEdges(self._idMapArtist)
        for id1,dati1 in risultato.items():
            for id2,dati2 in risultato.items():
                if id1<id2:
                    customers1=set(dati1["customer"])
                    customers2 = set(dati2["customer"])
                    comuni=customers1.intersection(customers2)

                    if len(comuni)>0:
                        pop1=dati1["popolarita"]
                        pop2=dati2["popolarita"]

                        peso=pop1+pop2
                        if pop1>pop2:
                            self._graph.add_edge(dati1["artist"],dati2["artist"],weight=peso)
                        elif pop1==pop2:
                            self._graph.add_edge(dati1["artist"], dati2["artist"], weight=peso)
                            self._graph.add_edge(dati2["artist"], dati1["artist"], weight=peso)
                        else:
                            self._graph.add_edge(dati2["artist"], dati1["artist"], weight=peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)