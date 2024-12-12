import tkinter as tk 
from tkinter import ttk
from tkinter import font
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from dao.consultas import listar_reclamos, crear_reclamo, modificar_reclamo, borrar_reclamo, listar_tipos

# Reclamos
class Reclamos(ttkb.Frame):
    def __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.fuente = ('Century Gothic', 12, 'normal')
        self.option_add("*TCombobox*Listbox*Font", self.fuente)
        self.id_reclamo = None

        self.widget_refs = {}
        self.asunto = ttkb.StringVar()
        self.descripcion = ttkb.StringVar()
        self.reclamo_tipo = ttkb.StringVar()

        self.rt_list = listar_tipos()
        self.option_list = [option[1] for option in self.rt_list] 
        self.reclamo_tipo.trace_add("write", self.actualizar_texto_mb)

        self.titulo()
        self.formulario()
        self.tabla()
        self.botones_tabla()
        
        
        
        self.bloquear_campos()

    def titulo(self):
        titulo = ttkb.Label(self, text='Crear Reclamo')
        titulo.config(font=('Century Gothic', 18, 'normal'))
        titulo.pack(padx=40, pady=20)

    def formulario(self):
        formulario = ttkb.Frame(self)
        formulario.pack(padx=40, pady=(0, 20))
        
        self.entrada_form(formulario, 'Asunto: ', self.asunto)
        self.entrada_form(formulario, 'Descripción: ', self.descripcion)
        self.entrada_combo_box(formulario, 'Tipo de reclamo: ')
        self.botones_form(formulario)

    def tabla(self):
        tabla = ttkb.Frame(self)
        tabla.pack(padx=40)
        self.tb(tabla)
    
    def entrada_form(self, formulario, label, variable):
        frame_entry = ttkb.Frame(formulario)
        frame_entry.pack(fill='x', expand='yes', padx=10, pady=(0, 8))

        label_1 = ttkb.Label(frame_entry, text=label, font=self.fuente, width=16)
        label_1.pack(side='left')

        input_1 = ttkb.Entry(frame_entry, textvariable=variable, font=self.fuente, width=30)
        input_1.pack(side='left', fill='x', expand='yes')

        self.widget_refs[label] = input_1

    def entrada_combo_box(self, formulario, label):
        frame_combobox = ttkb.Frame(formulario)
        frame_combobox.pack(fill='x', expand='yes', padx=10, pady=(0, 8))

        label_1 = ttkb.Label(frame_combobox, text=label, font=self.fuente, width=16)
        label_1.pack(side='left')

        self.mb = ttk.Menubutton(frame_combobox, text='Seleccione un Tipo', style='Outline.TMenubutton', width=30)

        self.menu = tk.Menu(self.mb, tearoff=0, font=self.fuente)
        for option in self.option_list:
            self.menu.add_radiobutton(label=option, value=option, variable=self.reclamo_tipo, font=self.fuente)

        self.mb['menu'] = self.menu
        self.mb.pack(side='left', fill='x', expand='yes')
        self.widget_refs['Menubutton'] = self.mb

        self.menu.config(postcommand=self.ajustar_menu)

    def actualizar_texto_mb(self, *args):
        self.mb.config(text=self.reclamo_tipo.get())

    def asdasd(self):
        self.rt_list = listar_tipos()
        self.option_list = []
        for option in self.rt_list:
            self.option_list.append(option[1])

    def actualizar_opciones(self): 
        self.menu.delete(0, 'end') 
    
        self.rt_list = self.rt_list_n
        self.option_list = [option[1] for option in self.rt_list] 
        
        for option in self.option_list: 
            self.menu.add_radiobutton(label=option, value=option, variable=self.reclamo_tipo, font=self.fuente) 

    def ajustar_menu(self):
        self.rt_list_n = listar_tipos()
        if self.rt_list_n != self.rt_list:
            self.actualizar_opciones()
                
        self.font_obj = font.Font(family=self.fuente[0], size=self.fuente[1])
        self.longest_option = max([self.menu.entrycget(i, "label") for i in range(self.menu.index("end") + 1)], key=len)
        self.text_width = self.font_obj.measure(self.longest_option)
        
        space_width = self.font_obj.measure(' ')
        num_spaces = int((274 - self.text_width) / space_width)

        for i in range(self.menu.index("end") + 1):
            label = self.menu.entrycget(i, "label").strip()
            self.menu.entryconfig(i, label=label + ' ' * num_spaces)

    def botones_form(self, formulario):
        self.frame_botones = ttkb.Frame(formulario)
        self.frame_botones.pack(side=RIGHT, padx=10)

        padding_botones = (14, 5)

        self.boton_nuevo = ttkb.Button(self.frame_botones, text="Nuevo", padding=padding_botones, command=self.habilitar_campos)
        self.boton_nuevo.pack(side=LEFT, padx=(8,0))

        self.boton_guardar = ttkb.Button(self.frame_botones, text="Guardar", padding=padding_botones, command=self.guardar_campos)
        self.boton_guardar.pack(side=LEFT, padx=(8,0))

        self.boton_cancelar = ttkb.Button(self.frame_botones, text="Cancelar", padding=padding_botones, command=self.bloquear_campos)
        self.boton_cancelar.pack(side=LEFT, padx=(8,0))

    def tb(self, tabla):
        columnas = ('asunto', 'descripcion', 'reclamo_tipo', 'reclamo_estado', 'fecha_creacion')
        self.tabla_reclamos = ttkb.Treeview(tabla, columns=columnas, show='headings')

        self.tabla_reclamos.column('asunto', width=100)
        self.tabla_reclamos.column('descripcion', width=145)
        self.tabla_reclamos.column('reclamo_tipo', width=150)
        self.tabla_reclamos.column('reclamo_estado', width=120)
        self.tabla_reclamos.column('fecha_creacion', width=135)

        self.tabla_reclamos.heading('asunto', text='Asunto', anchor='w')
        self.tabla_reclamos.heading('descripcion', text='Descripción', anchor='w')
        self.tabla_reclamos.heading('reclamo_tipo', text='Tipo de reclamo', anchor='w')
        self.tabla_reclamos.heading('reclamo_estado', text='Estado del reclamo', anchor='w')
        self.tabla_reclamos.heading('fecha_creacion', text='Fecha de creación', anchor='w')

        self.llenar_tabla()
            
        self.tabla_reclamos.pack(side=LEFT)
        
        scroll = ttkb.Scrollbar(tabla, orient='vertical', command=self.tabla_reclamos.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.tabla_reclamos.configure(yscrollcommand=scroll.set)

        self.tabla_reclamos.bind('<<TreeviewSelect>>', self.on_treeview_select)

    def botones_tabla(self):
        frame_1 = ttkb.Frame(self)
        frame_1.pack(side=RIGHT, padx=40, pady=(8, 20))

        padding_botones = (14, 5)

        self.boton_modificar = ttkb.Button(frame_1, text='Modificar', padding=padding_botones, command=self.editar_reclamo, state='disabled')
        self.boton_modificar.pack(side=LEFT, padx=(8, 0))
        
        self.boton_eliminar = ttkb.Button(frame_1, text='Eliminar', padding=padding_botones, command=self.eliminar_reclamo, state='disabled')
        self.boton_eliminar.pack(side=LEFT, padx=(8, 0))

    def editar_reclamo(self):
        try:
            self.id_reclamo = self.tabla_reclamos.item(self.tabla_reclamos.selection())['text']

            self.asunto_v = self.tabla_reclamos.item(self.tabla_reclamos.selection())['values'][0]
            self.descripcion_v = self.tabla_reclamos.item(self.tabla_reclamos.selection())['values'][1]
            self.reclamo_tipo_v = self.tabla_reclamos.item(self.tabla_reclamos.selection())['values'][2]

            self.habilitar_campos()
            self.asunto.set(self.asunto_v)
            self.descripcion.set(self.descripcion_v)
            self.reclamo_tipo.set(self.reclamo_tipo_v)
        except Exception as e:
            print(e)

    def eliminar_reclamo(self):
        self.id_reclamo = self.tabla_reclamos.item(self.tabla_reclamos.selection())['text']

        borrar_reclamo(int(self.id_reclamo))

        self.llenar_tabla()

    def llenar_tabla(self): 
        for row in self.tabla_reclamos.get_children(): 
            self.tabla_reclamos.delete(row) 
            
        self.lista_reclamos = listar_reclamos() 
        for r in self.lista_reclamos: 
            self.tabla_reclamos.insert('', END, text=r[0], values=(r[1], r[2], r[3], r[4], r[5]))

    def guardar_campos(self):
        if self.id_reclamo == None:
            crear_reclamo(self.asunto.get(), self.descripcion.get(), self.reclamo_tipo.get())
        else:
            modificar_reclamo(int(self.id_reclamo), self.asunto.get(), self.descripcion.get(), self.reclamo_tipo.get())

        self.id_reclamo = None
        self.bloquear_campos()
        self.llenar_tabla()

    def habilitar_campos(self):      
        for widget in self.widget_refs.values(): 
            widget.config(state='normal')
        self.boton_guardar.config(state='normal')    
        self.boton_cancelar.config(state='normal')    
        self.boton_nuevo.config(state='disabled')

    def bloquear_campos(self):    
        for widget in self.widget_refs.values(): 
            widget.config(state='disabled')
        self.boton_guardar.config(state='disabled')    
        self.boton_cancelar.config(state='disabled')    
        self.boton_nuevo.config(state='normal')
        self.asunto.set('')
        self.descripcion.set('')
        self.reclamo_tipo.set('')
        self.mb.config(text='Seleccione un Tipo')

    def on_treeview_select(self, event): 
        selected_item = self.tabla_reclamos.selection() 
        if selected_item: 
            self.boton_modificar.config(state='normal') 
            self.boton_eliminar.config(state='normal') 
        else: 
            self.boton_modificar.config(state='disabled') 
            self.boton_eliminar.config(state='disabled')


def aplicar_estilos():
    style = ttkb.Style()
    style.configure('Outline.TMenubutton', font=('Century Gothic', 12))
    style.configure("TButton", font=('Century Gothic', 10)) 
    if style.theme_use() == 'flatly':
        style.configure('Outline.TMenubutton', bordercolor='#ced4da') 
    elif style.theme_use() == 'superhero':
        style.configure('Outline.TMenubutton', bordercolor='#526170') 