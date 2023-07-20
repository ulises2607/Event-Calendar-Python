import tkinter as tk
import datetime
from functools import partial
from tkinter import ttk
from tkinter import *
import tkinter as tk
from calendar import monthcalendar
import datos


from Funciones.Funciones import Manipulacion


class Principal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.window = parent

        #Atributos de las ventanas
        parent.minsize(width=700, height=600)
        parent.title("Calendario de Eventos")
        parent.fecha_botones = []
        parent.topLevel = None
        parent.header = None


        # Atributos de la clase
        self.año = datetime.date.today().year  #Retorna el año actual <class int>
        self.mes = datetime.date.today().month  ## Retorna el mes actual <class int>
        self.dia = datetime.date.today().day  ## Retorna el dia actual

        
        
        #print(f"Esta es la linea que queres: {self.window.func.mes_int_a_string(3)}")

        # Funciones internas

        self.config_encabezado()
        self.hacer_botones_dias()
        self.dias_config()
        self.botones_cambio_mes()
        

        # DAtos de prueba 
        # datos.insertarDatos()
        

    def config_encabezado(self):
        """
        Creando el header del calendario que contiene el mes, el año y 2 botones para avanzar en estos atributos
        """

        header_texto = f"{Manipulacion.mes_int_a_string(self.mes)} {self.año}"
        self.header = Label(self, text=header_texto, font="Arvo 20", justify=CENTER)
        self.header.grid(row=0, column=1, columnspan=5, sticky=EW, ipady=25)

        lista_dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for i,j in enumerate(lista_dias):
            Label(self, text=lista_dias[i], bd=1, relief=SOLID).grid(row=1, column=i, sticky=NSEW, ipady=20)

    
    
    def botones_cambio_mes(self):
        btn = Button(self, text=">", command=self.mes_up, height=2, width=7 )
        btn.grid(row=0,column=5)

        btn = Button(self, text="<", command=self.mes_down, height=2, width=7 )
        btn.grid(row=0,column=1)


    def hacer_botones_dias(self):
        """ Crear botones de dias """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = Button(
                self,bg="#5d6094",relief=SUNKEN, bd=2, height=4, width=14)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW)
            self.window.fecha_botones.append(btn)

    def hayDatos(self,año,mes,dia):
        fecha = datetime.date(año, mes, dia)
        fecha_str = fecha.strftime("%Y-%m-%d")      
        data = datos.obtenerDatosGral(fecha_str)
        return len(data) > 0
    
    def dias_config(self):
        self.dates = Manipulacion.fecha_lista(self.año, self.mes)  # cargamos una lista 
          

        for i, j in enumerate(self.dates):  # Configure button text to show dates
            if j == 0:
                self.window.fecha_botones[i].configure(text="", state=DISABLED, bg="#024A86")
            else:
                
                self.window.fecha_botones[i].configure(text=j, command = partial(self.select_dia,j) ,bg="white", state=NORMAL,)

             ## Cambia bg btn color al current day 
            if j == datetime.date.today().day\
                    and self.mes == datetime.date.today().month \
                    and self.año == datetime.date.today().year:
                self.window.fecha_botones[i].configure(bg="#D9FFE3")
            if j > 0 :
                if self.hayDatos(self.año, self.mes, j):
                    self.window.fecha_botones[i].configure(bg="#E36B2C")
                
        
    
    def act_encabezado(self):
        self.header.configure(text=f"{Manipulacion.mes_int_a_string(self.mes)} {self.año}")

    

    ##################################################################################################################

    # Funciones botones

    def mes_up(self):
        "Incrementa el mes y actualiza el encabezado"
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.año += 1
        self.act_encabezado()
        self.dias_config()


    def mes_down(self):
        "Decrementa el mes y actualiza el encabezado"

        self.mes -= 1
        if self.mes ==0:
            self.mes = 12
            self.año -= 1
        self.act_encabezado()
        self.dias_config()

    def select_dia(self,numdia):

        top_level = tk.Toplevel(self.window)

        eventos = Eventos(top_level,numdia,self.mes,self.año).grid()


class Eventos(ttk.Frame):
    def __init__(self,parent,dia,mes,año):
        super().__init__(parent,padding=(10),)

        # Atributos de la ventana
        
        parent.title("Gestor de eventos")
        #parent.geometry("800x500")
        
        self.grid(row=0,column=3)
        # Atributos de la clase
        self.dia = dia
        self.mes = mes
        self.año = año

        
        
        # self.headerEvent()
        # self.tablaEvent()
        
    # def headerEvent(self):
        header_texto = f"{Manipulacion.mes_int_a_string(self.mes) } {self.dia} {self.año}"
        self.header = Label(self, text=header_texto, font="consolas 28 bold", justify=CENTER)
        self.header.grid(row=0, column=0, columnspan=5, sticky=NSEW)

        #FRAME VISUALIZACION DE EVENTOS
        self.frame = Frame(self,width=400, height=250)
        self.frame.grid()
    # def tablaEvent(self):
        self.eventos_registrados = ttk.Treeview(self.frame, columns=("titulo", "fecha_hora", "duracion", "descripcion", "importancia", "etiquetas"))
        self.eventos_registrados.heading("titulo", text="Titulo")
        self.eventos_registrados.heading("fecha_hora", text="Fecha-Hora")
        self.eventos_registrados.heading("duracion", text="Duracion")
        self.eventos_registrados.heading("descripcion", text="Descripcion")
        self.eventos_registrados.heading("importancia", text="Importancia")
        self.eventos_registrados.heading("etiquetas", text="Etiquetas")
        self.eventos_registrados.grid()

        

        #FRAME Y BOTONES ABM
        self.frame2 = Frame(self, width=400, height=250, pady=15)
        self.frame2.grid()

        self.btn_agregar = Button(self.frame2, text="Agregar" ,
                                  width=15 , height=5, command=self.agregarFrame)
        self.btn_agregar.grid(row=1,column=1)
        
        self.btn_eliminar = Button(self.frame2, text="Eliminar",
                                   width=15, height=5)
        self.btn_eliminar.grid(row=1,column=2, padx=15)
        
        self.btn_editar = Button(self.frame2, text= "Modificar",
                                 width=15, height=5)
        self.btn_editar.grid(row=1,column=3)

        self.mostrarDatos(año, mes, dia)
        
    def mostrarDatos(self,año,mes,dia):
        fecha = datetime.date(año, mes, dia)
        fecha_str = fecha.strftime("%Y-%m-%d")      
        data = datos.obtenerDatosGral(fecha_str)

        #Limpieza de tabla
        self.eventos_registrados.delete(*self.eventos_registrados.get_children())

        # Insertando los datos en el Treeview
        for fila in data:
            self.eventos_registrados.insert('', 'end', values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]))
        
    def agregarFrame(self):
        self.frame3 = Frame(self, width=400, height=250, pady=15)
        self.frame3.grid()

        # Crear etiquetas y entradas de texto

        self.labelTitle = Label(self.frame3,text="Titulo", font= "consolas 18 bold",padx=20)
        self.labelTitle.grid(row=0,column=0)

        self.titulo = Entry(self.frame3,width=40)
        self.titulo.grid(row=1,column=0)

        self.labelDesc = Label(self.frame3,text="Descripcion", font= "consolas 18 bold",padx=20)
        self.labelDesc.grid(row=2,column=0)

            #Caja texto descripcion
        self.descripcion = Text(self.frame3, width=40, height = 10)
        self.descripcion.grid(row=3,column=0)

        

        #horarios
            #Selector de hora
        self.tit_hora = Label(self.frame3,text="Seleccione hora",pady=1)
        self.tit_hora.grid(row=0, column=1, pady=(0, 0))

        self.hora = ttk.Combobox(self.frame3,values=[f"{h}" for h in range(0,24)])
        self.hora.grid(row=1, column=1, pady=(0, 0))

            #Selector de minutos
        self.tit_min = Label(self.frame3, text="Seleccione minutos", pady=0)
        self.tit_min.grid(row=2, column=1, pady=(0, 0))

        self.minutos = ttk.Combobox(self.frame3,values=[f"{m}" for m in range(0,61,5) ])
        self.minutos.grid(row=3,column=1, pady=(0, 0))

            #Duracion del evento (Acotado en horas solamente en el dia seleccionado por el momento)
        
        self.tit_dur = Label(self.frame3, text="Duracion del evento en horas",pady=1)
        self.tit_dur.grid(row=4,column=1, pady=(0, 0))

        self.duracion = ttk.Combobox(self.frame3,values=[f"{h}" for h in range(0,24)])
        self.duracion.grid(row=5,column=1, pady=(0, 0))

            # Horarios y etiquetas

        self.rel_label = Label(self.frame3, text="Relevancia",pady=1)
        self.rel_label.grid(row=6,column=1, pady=(0, 0))

        self.relevancia = ttk.Combobox(self.frame3,values=["Normal","Importante"])
        self.relevancia.grid(row=7,column=1, pady=(0, 0))

        self.etiqueta_label = Label(self.frame3, text="Etiqueta",pady=1)
        self.etiqueta_label.grid(row=1,column=2, pady=(0, 0))

        self.etiqueta = ttk.Combobox(self.frame3,values=["Universidad","Trabajo","Pasatiempo"])
        self.etiqueta.grid(row=2,column=2, pady=(0, 0))

            # Botones

        self.guardar = Button(self.frame3,text="Guardar", width=20,height=3 ,command=self.accionGuardar, pady=30)
        self.guardar.grid(row=4,column=0, pady=(0, 5))
       
    def accionGuardar(self):
        #Formateando fecha
        fecha = datetime.date(self.año, self.mes, self.dia)
        fecha_str = fecha.strftime("%Y-%m-%d")    

        #Formateando hora
        hora_evento = self.hora.get().zfill(2)
        minutos_evento = self.minutos.get().zfill(2)
        
        
        titulo = self.titulo.get()
        formato_hora_evento = f"{hora_evento}:{minutos_evento}:00"  
        duracion = self.duracion.get()#Necesito todavia configurar el cambio de horas a minutos
        descripcion = self.descripcion.get('1.0',"end")
        importancia = self.relevancia.get()

        eventos = (titulo,formato_hora_evento,duracion,descripcion,importancia)

        etiqueta = self.etiqueta.get()

        datos.agregarDatos((fecha_str,),(etiqueta,),eventos)
        self.mostrarDatos(self.año,self.mes,self.dia)
        self.frame3.destroy()
        



        # id_etiqueta_label = tk.Label(self.frame3, text="ID Etiqueta:")
        # id_etiqueta_label.pack()
        # id_etiqueta_entry = tk.Entry(self.frame3)
        # id_etiqueta_entry.pack()

        # titulo_evento_label = tk.Label(self.frame3, text="Título del Evento:")
        # titulo_evento_label.pack()
        # titulo_evento_entry = tk.Entry(self.frame3)
        # titulo_evento_entry.pack()

        # hora_evento_label = tk.Label(self.frame3, text="Hora del Evento:")
        # hora_evento_label.pack()
        # hora_evento_entry = tk.Entry(self.frame3)
        # hora_evento_entry.pack()

        # duracion_minutos_label = tk.Label(self.frame3, text="Duración en Minutos:")
        # duracion_minutos_label.pack()
        # duracion_minutos_entry = tk.Entry(self.frame3)
        # duracion_minutos_entry.pack()

        # descripcion_label = tk.Label(self.frame3, text="Descripción:")
        # descripcion_label.pack()
        # descripcion_entry = tk.Entry(self.frame3)
        # descripcion_entry.pack()

        # importancia_label = tk.Label(self.frame3, text="Importancia:")
        # importancia_label.pack()
        # importancia_entry = tk.Entry(self.frame3)
        # importancia_entry.pack()

        # # Crear botón para agregar los datos
        # btn_insertar = tk.Button(self.frame3, text="Insertar Datos")
        # btn_insertar.pack()

        
    
    # def abrir_ventana_datosEventos(self):
    #     top_level2 = tk.Toplevel()
    #     datos_eventos = Datos(top_level2,self.dia,self.mes,self.año).grid()


    

    # def leer_datos_eventos(self):
    #         #Falta estudiar y condicionar la lectura de los datos en sus correspondientes dias
    #         f = open('WriteData.json','r')
    #         data = json.loads(f.read())

    #         count = 0

    #         for record in data[f"{self.dia}"]:
    #             self.eventos_registrados.insert(parent='', index="end", id=count, text="",
    #                                             values=(record['Titulo'],record['Descripcion'],record['Hora de Aviso'], record['Duracion de evento'], record['Modo de recordatorio']))
    #            count += 1