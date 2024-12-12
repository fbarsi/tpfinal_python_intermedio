import tkinter as tk
import ttkbootstrap as ttkb
from cliente.reclamos import Reclamos, aplicar_estilos
from cliente.reclamo_tipos import ReclamosTipos
from dao.consultas import crear_tabla, listar_reclamos, agregar_datos
from datetime import datetime

class App():
    def __init__(self):
        self.ventana = ttkb.Window()
        self.ventana.title('Lista de Reclamos')
        crear_tabla()
        # agregar_datos() # En el caso de necesitar agregar los datos de reclamostipos y reclamosestados a la base de datos

        self.style = ttkb.Style() 
        self.style.theme_use('superhero')
        aplicar_estilos()
        
        self.theme_var = tk.BooleanVar() 
        self.theme_var.set(True)

    def main(self):
        notebook = ttkb.Notebook(self.ventana)
        notebook.pack()

        reclamos = Reclamos(root=self.ventana)

        rtipos = ReclamosTipos(root=self.ventana)

        notebook.add(reclamos, text='Reclamos')
        notebook.add(rtipos, text='Tipos de reclamo')

        modoscuro = ttkb.Checkbutton(self.ventana, text='Modo Oscuro', variable=self.theme_var, command=self.cambiar_tema, style='Roundtoggle.Toolbutton')
        modoscuro.pack(side=tk.LEFT, padx=40, pady=8)        

        self.ventana.mainloop()

    def cambiar_tema(self): 
        if self.theme_var.get(): 
            self.style.theme_use("superhero") 
        else: 
            self.style.theme_use("flatly")
        aplicar_estilos()

if __name__ == '__main__':
    app = App()
    app.main()