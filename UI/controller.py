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