from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.allGenre=[]
        self._graph = nx.DiGraph()
        self._allNodes=[]
        self._idMapArtist={}
        self._risultato={}

    def getAllGenre(self):
        self.allGenre=DAO.getAllGenre()
        return self.allGenre

    def getAllArtist(self):
        return self._idMapArtist

    def buildGraph(self,genreId):
        self._graph.clear()
        self._idMapArtist.clear()
        self._risultato.clear()
        self._allNodes=DAO.getAllNodes(genreId)
        for a in self._allNodes:
            self._idMapArtist[a.ArtistId] = a
        self._graph.add_nodes_from(self._allNodes)
        self.addEdges(genreId)

    def addEdges(self,genreId):
        self._risultato=DAO.getAllEdges(self._idMapArtist,genreId)
        for id1,dati1 in self._risultato.items():
            for id2,dati2 in self._risultato.items():
                if id1<id2:
                    customers1=dati1["customer"]
                    customers2 = dati2["customer"]
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
    
    def getBestArtist(self):
        bestArtist=None
        bestValue=-1
        for n in self._graph.nodes:
            outgoing=0
            incoming=0
            for u,v,data in self._graph.out_edges(n, data=True):
                outgoing+=data["weight"]
            for u,v,data in self._graph.in_edges(n, data=True):
                incoming+=data["weight"]
            
            influenza= outgoing-incoming

            if influenza>bestValue:
                bestValue=influenza
                bestArtist=n
        
        return bestArtist,bestValue
    
    def getTopEdges(self):
        archi=[]
        for u,v,data in self._graph.edges(data=True):
            archi.append((u,v,data["weight"]))
        archi.sort(key=lambda x:x[2], reverse=True)
        return archi[:5]