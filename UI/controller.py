import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre=None
        self._choiceArtist=None

    def fillDDGenre(self):
        allGenre=self._model.getAllGenre()
        for g in allGenre:
            self._view._ddGenre.options.append(ft.dropdown.Option(data=g,key=g.Name,on_click=self._choiceDDGenre))
    
    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        allArtist=self._model.getAllArtist()
        for a, dati in allArtist.items():
            self._view._ddArtist.options.append(ft.dropdown.Option(data=dati, key=dati.Name, on_click=self._choiceDDArtist))

    def handleCreaGrafo(self, e):
        if self._choiceGenre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un genere musicale", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(self._choiceGenre.GenreId)
        
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nNodes}."))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {nEdges}."))
        

        bestArtist,value=self._model.getBestArtist()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {bestArtist}, con influenza: {value}."))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for u,v,w in self._model.getTopEdges():
            self._view.txt_result.controls.append(
            ft.Text(f"{u} ->{v} : {w}."))
        self.fillDDArtist()
        self._view.update_page()

        self.fillDDArtist()
    def handleCammino(self,e):
        pass

    def _choiceDDGenre(self, e):
        self._choiceGenre = e.control.data
        print(f"hai selezionato{self._choiceGenre}")

    def _choiceDDArtist(self, e):
        self._choiceArtist = e.control.data
        print(f"hai selezionato{self._choiceArtist}")

    #menu a tendina di country come si costruisce:
    self._choiceCountry=None
    def fillDDCountry(self):
        allCountries = self._model.getAllCountries()
        for c in allCountries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(
                    key=c,
                    data=c,
                    on_click=self._choiceCountryDD
                )
            )
    def _choiceCountryDD(self,e):
        self._choiceCountry = e.control.data

    #handle percorso della ricorsione
    def handlePercorso(self,e):
        percorso = self._model.cercaPercorso()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(
                f"Lunghezza percorso: {len(percorso)}"
            )
        )
        for c in percorso:
            self._view.txt_result.controls.append(
                ft.Text(
                    f"{c.FirstName} {c.LastName} - {c.spesaTotale}"
                )
            )
        self._view.update_page()

    #menu a tendina mediatype
    #menu a tendina artista del grafo
    self._choiceMediaType = None
    self._choiceArtist = None

    def fillDDMediaType(self):
        allTypes = self._model.getAllMediaTypes()
        for t in allTypes:
            self._view._ddMediaType.options.append(
                ft.dropdown.Option(
                    key=t.Name,
                    data=t,
                    on_click=self._choiceMediaTypeDD
                )
            )
    def _choiceMediaTypeDD(self,e):
        self._choiceMediaType = e.control.data

    #questo da aggiungere dopo buildgraph in handle crea grafo
    self._view._ddArtist.options.clear()

    for a in self._model.getArtists():
        self._view._ddArtist.options.append(
            ft.dropdown.Option(
                key=a.Name,data=a,
                on_click=self._choiceArtistDD
                )
            )
    #handle percorso per la ricorsione 
    def handlePercorso(self,e):
        if self._choiceArtist is None:
            self._view.create_alert(
                "Selezionare un artista"
            )
            return
        percorso = self._model.cercaPercorso(
            self._choiceArtist
        )
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(
                f"Lunghezza: {len(percorso)}"
            )
        )
        for a in percorso:
            self._view.txt_result.controls.append(
                ft.Text(
                    f"{a.Name} ({a.popolarita})"
                )
            )
        self._view.update_page()