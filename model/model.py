from database.DAO import DAO
import networkx as nx
import itertools

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
    
    #Costruisci un grafo non orientato e pesato tra clienti
    self._graph = nx.Graph()
    #per menu a tendina delle country
    def getAllCountries(self):
        return DAO.getAllCountries()
    #I vertici sono i clienti residenti nel paese selezionato.
    def buildGraph(self,country):
        self._graph.clear()
        self._idMapCustomer={}
        self._allNodes=DAO.getAllNodes(country)
        for c in self._allNodes:
            self._idMapCustomer[c.CustomerId]=c
        self._graph.add_nodes_from(
            self._allNodes
        )
        self.addEdges(country)
        #Esiste un arco tra due clienti se hanno acquistato almeno un brano dello stesso artista. Il peso è il numero di artisti in comune.
    def addEdges(self,country):
            acquisti = DAO.getArtistsByCustomer(                self._idMapCustomer,
                country
            )

            clienti = list(
                self._graph.nodes()
            )

            for c1,c2 in itertools.combinations(
                    clienti,
                    2):

                artisti1 = acquisti.get(
                    c1.CustomerId,
                    set()
                )

                artisti2 = acquisti.get(
                    c2.CustomerId,
                    set()
                )

                comuni = artisti1.intersection(
                    artisti2
                )

                peso = len(comuni)

                if peso > 0:

                    self._graph.add_edge(
                        c1,
                        c2,
                        weight=peso
                    )
        #componenti connesse
    def getCompConnesse(self):
            return nx.number_connected_components(
                self._graph
            )
        
    def getCompMaggiore(self):
            return max(nx.connected_components(self._graph), key=len)
        
        #ricorsione: il cammino semplice di lunghezza massima tale che la spesa totale 
        # (Total delle invoice) di ogni cliente successivo sia strettamente crescente.
    def cercaPercorso(self):
            self.bestPath=[]
            for nodo in self._graph.nodes():
                parziale=[nodo]
                self.ricorsione(parziale)
            return self.bestPath
    def ricorsione(self,parziale):
            if len(parziale)>len(self.bestPath):
                self.bestPath=list(parziale)
            ultimo=parziale[-1]
            for vicino in self._graph.neighbors(
                    ultimo):
                if vicino not in parziale:
                    if vicino.spesaTotale > ultimo.spesaTotale:
                        parziale.append(vicino)
                        self.ricorsione(parziale)
                        parziale.pop()
        #Costruisci un grafo orientato e pesato tra artisti
    self._graph = nx.DiGraph()
        #per il menu a tendina mediatype
    def getAllMediaTypes(self):
            return DAO.getAllMediaTypes()
        #I vertici sono gli artisti che hanno almeno un brano del media type selezionato.
    def buildGraph(self,mediaTypeId):
            self._graph.clear()
            self._idMapArtist = {}
            self._allNodes = DAO.getAllNodes(
                mediaTypeId
            )
            for a in self._allNodes:
                self._idMapArtist[a.ArtistId] = a
            self._graph.add_nodes_from(
                self._allNodes
            )
            self.addEdges()
    def addEdges(self):
            for a,b in itertools.combinations(self._graph.nodes(),r=2):
                peso = (a.popolarita +b.popolarita)
                if a.popolarita > b.popolarita:
                    self._graph.add_edge(
                        a,
                        b,
                        weight=peso
                    )
                elif b.popolarita > a.popolarita:
                    self._graph.add_edge(
                        b,
                        a,
                        weight=peso
                    )
                else:
                    self._graph.add_edge(
                        a,
                        b,
                        weight=peso
                    )
                    self._graph.add_edge(
                        b,
                        a,
                        weight=peso
                    )
    #l'artista con maggiore influenza (peso archi uscenti − peso archi entranti).
    def getInfluente(self):
        best = None
        bestValue = -999999999
        for a in self._graph.nodes():
            pesoOut = 0
            pesoIn = 0
            for v in self._graph.successors(a):
                pesoOut += self._graph[a][v]["weight"]
            for v in self._graph.predecessors(a):
                pesoIn += self._graph[v][a]["weight"]
            valore = pesoOut - pesoIn
            if valore > bestValue:
                bestValue = valore
                best = a
        return best,bestValue
    #per il dropdown
    def getArtists(self):
        return sorted(
            self._graph.nodes(),
            key=lambda x:x.Name
        )
    #ricorsione:Selezionato un artista dall'utente (tra quelli del grafo), trovare il cammino semplice di lunghezza massima a partire da quel nodo tale che ogni arco successivo abbia peso strettamente crescente.
    def cercaPercorso(self,artist):
        self.bestPath=[]
        parziale=[artist]
        self.ricorsione(parziale)
        return self.bestPath
    def ricorsione(self,parziale):
        if len(parziale)>len(self.bestPath):
            self.bestPath=list(parziale)
        ultimo=parziale[-1]
        for vicino in self._graph.successors(
                ultimo):
            if vicino not in parziale:
                pesoNuovo = self._graph[
                    ultimo
                ][
                    vicino
                ]["weight"]
                if len(parziale)==1:
                    parziale.append(vicino)
                    self.ricorsione(parziale)
                    parziale.pop()
                else:
                    precedente = parziale[-2]
                    pesoVecchio = self._graph[
                        precedente
                    ][
                        ultimo
                    ]["weight"]
                    if pesoNuovo > pesoVecchio:
                        parziale.append(vicino)
                        self.ricorsione(parziale)
                        parziale.pop()