import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre=None

    def fillDDGenre(self):
        allGenre=self._model.getAllGenre()
        for g in allGenre:
            self._view._ddGenre.options.append(ft.dropdown.Option(data=g,key=g.Name,on_click=self._choiceDDGenre))


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
        self._view.update_page()


    def handleCammino(self,e):
        pass

    def _choiceDDGenre(self, e):
        self._choiceGenre = e.control.data
        print(f"hai selezionato{self._choiceGenre}")