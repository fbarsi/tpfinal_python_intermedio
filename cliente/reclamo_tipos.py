import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from dao.consultas import listar_tipos, crear_tipo, modificar_tipo, borrar_tipo

#  Tipos de reclamos
class ReclamosTipos(ttkb.Frame):
    def __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.fuente = ('Century Gothic', 12, 'normal')
        self.id_reclamo_tipo = None

        self.descripcion_tipo = ttkb.StringVar()

        self.titulo()
        self.formulario()
        self.tabla()
        self.botones_tabla()
                
        self.bloquear_campos()

    def titulo(self):
        titulo = ttkb.Label(self, text='Crear Tipo de Reclamo')
        titulo.config(font=('Century Gothic', 18, 'normal'))
        titulo.pack(padx=40, pady=20)

    def formulario(self):
        formulario = ttkb.Frame(self)
        formulario.pack(padx=40, pady=(0, 20))
        
        self.entrada_form(formulario, 'Descripción: ', self.descripcion_tipo)
        self.botones_form(formulario)

    def tabla(self):
        self.frame_tb = ttkb.Frame(self)
        self.frame_tb.pack(padx=40)
        self.tb(self.frame_tb)
    
    def entrada_form(self, formulario, label, variable):
        frame_entry = ttkb.Frame(formulario)
        frame_entry.pack(fill='x', expand='yes', padx=10, pady=(0, 8))

        label_1 = ttkb.Label(frame_entry, text=label, font=self.fuente, width=16)
        label_1.pack(side='left')

        self.input_desc = ttkb.Entry(frame_entry, textvariable=variable, font=self.fuente, width=30)
        self.input_desc.pack(side='left', fill='x', expand='yes')

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
        self.tabla_reclamo_tipos = ttkb.Treeview(tabla, columns=('id', 'descripcion'), show='headings')

        self.tabla_reclamo_tipos.column('id', width=100)
        self.tabla_reclamo_tipos.column('descripcion', width=400)

        self.tabla_reclamo_tipos.heading('id', text='ID', anchor='w')
        self.tabla_reclamo_tipos.heading('descripcion', text='Descripción', anchor='w')

        self.llenar_tabla()
            
        self.tabla_reclamo_tipos.pack(side=LEFT)
        
        scroll = ttkb.Scrollbar(tabla, orient='vertical', command=self.tabla_reclamo_tipos.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.tabla_reclamo_tipos.configure(yscrollcommand=scroll.set)

        self.tabla_reclamo_tipos.bind('<<TreeviewSelect>>', self.on_treeview_select)

    def botones_tabla(self):
        frame_1 = ttkb.Frame(self)
        frame_1.pack(side=RIGHT, padx=115, pady=(8, 0), anchor='n')

        padding_botones = (14, 5)

        self.boton_modificar = ttkb.Button(frame_1, text='Modificar', padding=padding_botones, command=self.editar_reclamo_tipo, state='disabled')
        self.boton_modificar.pack(side=LEFT, padx=(8, 0))
        
        self.boton_eliminar = ttkb.Button(frame_1, text='Eliminar', padding=padding_botones, command=self.eliminar_reclamo_tipo, state='disabled')
        self.boton_eliminar.pack(side=LEFT, padx=(8, 0))

    def editar_reclamo_tipo(self):
        try:
            self.id_reclamo_tipo = self.tabla_reclamo_tipos.item(self.tabla_reclamo_tipos.selection())['values'][0]
            self.descripcion_tipo_v = self.tabla_reclamo_tipos.item(self.tabla_reclamo_tipos.selection())['values'][1]

            self.habilitar_campos()
            self.descripcion_tipo.set(self.descripcion_tipo_v)
        except Exception as e:
            print(e)

    def eliminar_reclamo_tipo(self):
        self.id_reclamo_tipo = self.tabla_reclamo_tipos.item(self.tabla_reclamo_tipos.selection())['values'][0]

        borrar_tipo(int(self.id_reclamo_tipo))

        self.llenar_tabla()

    def llenar_tabla(self): 
        for row in self.tabla_reclamo_tipos.get_children(): 
            self.tabla_reclamo_tipos.delete(row) 
            
        self.lista_reclamo_tipos = listar_tipos() 
        for r in self.lista_reclamo_tipos: 
            self.tabla_reclamo_tipos.insert('', END, values=(r[0], r[1]))

    def guardar_campos(self):
        if self.id_reclamo_tipo == None:
            crear_tipo(self.descripcion_tipo.get())
        else:
            modificar_tipo(int(self.id_reclamo_tipo), self.descripcion_tipo.get())

        self.id_reclamo_tipo = None
        self.bloquear_campos()
        self.llenar_tabla()

    def habilitar_campos(self):      
        self.input_desc.config(state='normal')
        self.boton_guardar.config(state='normal')    
        self.boton_cancelar.config(state='normal')    
        self.boton_nuevo.config(state='disabled')

    def bloquear_campos(self):    
        self.input_desc.config(state='disabled')
        self.boton_guardar.config(state='disabled')    
        self.boton_cancelar.config(state='disabled')    
        self.boton_nuevo.config(state='normal')
        self.descripcion_tipo.set('')

    def on_treeview_select(self, event): 
        selected_item = self.tabla_reclamo_tipos.selection() 
        if selected_item: 
            self.boton_modificar.config(state='normal') 
            self.boton_eliminar.config(state='normal') 
        else: 
            self.boton_modificar.config(state='disabled') 
            self.boton_eliminar.config(state='disabled')