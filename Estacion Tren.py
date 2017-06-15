5# Tercer proyecto programado
# Estacion de Tren
# Jasson Rodriguez
# Marco Herrera

import sys
import os
from tkinter import *
import pygame
import random
from threading import Thread
import time
import datetime
from PIL import Image, ImageTk

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen
#Restricciones: el archivo debe estar contenido en la carpeta Imagenes

def cargarImagen(nombre,tamaño):
    ruta = os.path.join("Imagenes", nombre)
    imagen = Image.open(ruta)
    imagen.thumbnail((tamaño * windowWidth,tamaño * windowHeight))
    imagen = ImageTk.PhotoImage(image = imagen)
    return imagen

#Funcion: cargarSonido
#Entrada: nombre
#Salida: sonido
#Restricciones: el archivo debe estar contenido en la carpeta Audio
def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

#Funcion: scale_img
#Entradas: imagen, ancho y altura
#Salida: imagen reescalada
#Restricciones: imagen de tipo pygame, ancho y altura son enteros
def scale_img(image,width,height):    
    image = pygame.transform.smoothscale(image,(width,height))
    return PhotoImage(image)


class Tren:
    def __init__(self, id, ruta, hora):
        self.id = id
        self.ruta = ruta
        self.hora = hora
        self.demanda = random.randrange(5, 75)
        self.maquina = None
        self.head = None
        self.tail = None
        self.carga = 0
        self.capacidad = 0
        if ruta.find("TEC") == 0:
            self.enEstacion = True
        else:
            self.enEstacion = False

    def get_hora(self):
        return self.hora

    #Metodo: optimizar
    #Entrada: demanda
    #Salida: asigna los vagones y la maquina de acuerdo a la demanda existente
    #Restricciones: demanda es un entero positivo
    def optimizar(self, demanda):
        if self.enEstacion:
            listaVagones = vagonesLibres
            listaMaquinas = maquinasLibres
        else:
            listaVagones = vagonesFuera
            listaMaquinas = maquinasFuera

        vagones = []
        while demanda > 0:
            mejorVagon = None
            for vagon in listaVagones:
                if vagon.capacidad >= demanda and (mejorVagon == None or vagon.capacidad < mejorVagon.capacidad):
                    mejorVagon = vagon
                    if vagon.capacidad == demanda:
                        break
            if mejorVagon == None:
                for vagon in listaVagones:
                    if mejorVagon == None or demanda - vagon.capacidad < demanda - mejorVagon.capacidad:
                        mejorVagon = vagon
            vagones.append(mejorVagon)
            listaVagones.remove(mejorVagon)
            demanda -= mejorVagon.capacidad
        mejorMaquina = None
        for maquina in listaMaquinas:
            if maquina.capacidad >= len(vagones) and (mejorMaquina == None or maquina.capacidad < mejorMaquina.capacidad):
                mejorMaquina = maquina
                if mejorMaquina.capacidad == len(vagones):
                    break
        self.asignarMaquina(mejorMaquina.id)
        for vagon in vagones:
            self.engancharInicio(vagon.id)

    #Metodo: asignarMaquina
    #Entrada: id de la maquina
    #Salida: asigna esa maquina al atributo maquina del tren
    #Restricciones: id es un entero positivo
    def asignarMaquina(self, id): #Acepta trenes en la estacion y afuera
        if self.enEstacion:
            listaMaquinas = maquinasLibres
        else:
            listaMaquinas = maquinasFuera
        for maquina in listaMaquinas:
            if maquina.id == id:
                if self.maquina != None:
                    listaMaquinas.append(self.maquina)
                self.maquina = maquina
                listaMaquinas.remove(maquina)
            elif maquina == maquinasLibres[-1]:
                print("Máquina no encontrada")

    #Metodo: engancharInicio
    #Entrada: id del vagon
    #Salida: asigna ese vagon al inicio del tren
    #Restricciones: id es un entero positivo
    def engancharInicio(self, id): #Acepta trenes en la estacion y afuera
        if self.enEstacion:
            listaVagones = vagonesLibres
        else:
            listaVagones = vagonesFuera
        if self.maquina != None and self.carga != self.maquina.capacidad:
            for vagon in listaVagones:
                if vagon.id == id:
                    temp = self.head
                    self.head = vagon
                    self.head.next = temp
                    if temp != None:
                        temp.prev = vagon
                    else:
                        self.tail = self.head
                    self.carga += 1
                    self.capacidad += vagon.capacidad
                    listaVagones.remove(vagon)
                    break
                elif vagon == vagonesLibres[-1]:
                    print("Vagón no encontrado")
        elif self.maquina == None:
            print("No hay máquina asignada")
        else:
            print("Capacidad de la máquina alcanzada")

    #Metodo: engancharMedio
    #Entrada: id del vagon y la posicion en que se desea añadir
    #Salida: asigna ese vagon en la posicion dada
    #Restricciones: id y pos enteros positivo y pos menor o igual que la carga del tren
    def engancharMedio(self, id, pos): #Solo trenes en la estacion
        if self.maquina != None and self.carga != self.maquina.capacidad:
            for vagon in vagonesLibres:
                if vagon.id == id:
                    if pos == self.carga:
                        self.engancharFinal(id)
                    elif pos == 0:
                        self.engancharInicio(id)
                    elif pos < self.carga:
                        temp = self.head
                        cont = 0
                        while cont != pos:
                            temp = temp.next
                            cont += 1
                        temp.prev.next = vagon
                        temp.prev = vagon
                        vagon.prev = temp.prev
                        vagon.next = temp
                        self.carga += 1
                        self.capacidad += vagon.capacidad
                        vagonesLibres.remove(vagon)
                    else:
                        print("Índice fuera de rango")
                    break
                elif vagon == vagonesLibres[-1]:
                    print("Vagón no encontrado")
        elif self.maquina == None:
            print("No hay máquina asignada")
        else:
            print("Capacidad de la máquina alcanzada")

    #Metodo: engancharFinal
    #Entrada: id del vagon
    #Salida: asigna ese vagon en la ultima posicion
    #Restricciones: id es un entero positivo
    def engancharFinal(self, id):
        if self.maquina != None and self.carga != self.maquina.capacidad:
            for vagon in vagonesLibres:
                if vagon.id == id:
                    if self.carga > 0:
                        temp = self.tail
                        self.tail.next = vagon
                        self.tail = vagon
                        vagon.prev = temp
                    else:
                        self.head = vagon
                        self.tail = vagon
                    self.carga += 1
                    self.capacidad += vagon.capacidad
                    vagonesLibres.remove(vagon)
                    break
        elif self.maquina == None:
            print("No hay máquina asignada") 
        else:
            print("Capacidad de la máquina alcanzada")

    #Metodo: quitarVagon
    #Entrada: pos del vagon
    #Salida: elimina el vagon existente en la posicion pos
    #Restricciones: posicion valida
    def quitarVagon(self, pos):
        global vagonesLibres
        if pos < 0 or pos > self.carga -1:
            print("Índice fuera de rango")
                
        elif self.maquina != None and self.carga != self.maquina.capacidad and self.carga > 0 :
            if pos == 0:
                temp = self.head
                if self.carga > 1:
                    self.head = temp.next
                    self.head.prev = None
                    temp.next = None
                else:
                    self.tail = None
                    self.head = None

            elif pos == self.carga:
                temp = self.tail
                self.tail = temp.prev
                temp.prev = None
                self.tail.next = None
                
            else:
                temp = self.head
                cont = 0
                while temp != self.tail:
                    if cont == pos:
                        temp.prev.next = temp.next
                        temp.next.prev = temp.prev
                        temp.next = None
                        temp.prev = None
                        break
                    else:
                        temp = temp.next
                        connt += 1
            vagonesLibres += [temp]
            self.carga -= 1
                    
        elif self.maquina == None:
            print("No hay máquina asignada")
        elif self.carga == 0:
            print("No hay vagones asignados")
        else:
            print("Capacidad de la máquina alcanzada")

    #Metodo: salir
    #Entrada: ninguna
    #Salida: el tren sale de la estacion, enEstacion pasa a False
    #Restricciones: maquina asignada y que cumpla con la demanda
    def salir(self):
        self.enEstacion = False
        print("salir")

    #Metodo: llegar
    #Entrada: ninguna
    #Salida: el tren llega a la estacion, enEstacion pasa a True, la maquina y vagones quedan libres
    #Restricciones: ninguna
    def llegar(self):
        global maquinasLibres
        global vagonesLibres
        self.optimizar(self.demanda)
        self.enEstacion = True
        maquinasLibres += [self.maquina]
        temp = self.head
        while temp != None:
            vagonesLibres += [temp]
            temp = temp.next
        self.maquina = None
        self.head = None
        self.tail = None
        print("Llegar")

    #Metodo: mostrar
    #Entrada: ninguna
    #Salida: muestra los atributos y vagones del tren
    #Restricciones: ninguna
    def mostrar(self):
        print("ID : ", self.id)
        print("Ruta: ", self.ruta)
        print("Hora: ", self.hora)
        print("Estacion: ", self.enEstacion)
        if self.maquina != None and self.head != None:
            print("Maquina: ")
            self.maquina.mostrar()
            temp = self.head
            print("Vagones")
            while temp != None:
                temp.mostrar()
                temp = temp.next

class Maquina:
    def __init__(self, id, capacidad):
        self.id = id
        self.capacidad = capacidad

    def mostrar(self):
        print("ID: ", self.id, " Capacidad: ", self.capacidad)

class Vagon:
    def __init__(self, id, capacidad):
        self.id = id
        self.capacidad = capacidad
        self.prev = None
        self.next = None

    def mostrar(self):
        print("ID: ", self.id, " Capacidad: ", self.capacidad)


trains = []
newTrainID = 0
enEjecucion = True

#Lectura de archivo de configuracion
with open("estacion.txt") as config:
    vagonesLibres = eval(config.readline())
    maquinasLibres = eval(config.readline())
    vagonesFuera = eval(config.readline())
    maquinasFuera = eval(config.readline())
    for line in config:
        if line.find("Ruta") != -1:
            ruta = line.replace("Ruta ", "").replace("\n", "")
        else:
            hora = int(line[0:2]), int(line[3:])
            trains.append(Tren(id=newTrainID, ruta=ruta, hora = hora))
            newTrainID += 1

trenesDia = trains[:]

#Funcion: mostrar
#Entrada: lista
#Salida: el metodo mostrar para cada elemento de la lista
#Restricciones: todos los objetos de la lista tienen el metodo mostrar
def mostrar(lista):
    for i in lista:
        i.mostrar()
        print("----------------------------")

#Funcion: ruta_hora
#Entrada: lista y hora
#Salida: rutas por hora
#Restricciones: hora es un numero entero
def ruta_hora(lista, hora):
    salidas = []
    llegadas = []
    for tren in trains:
        if tren.hora[0] == hora:
            if tren.hora[1] < 10:
                minutos = "0" + str(tren.hora[1])
            else:
                minutos = str(tren.hora[1])
            ruta = tren.ruta + " " + str(tren.hora[0]) + ":" + minutos
            if tren.enEstacion:
                salidas.append(ruta)
            else:
                llegadas.append(ruta)
    print("Salidas")
    for hora in salidas:
        print(hora)
    print("Llegadas")
    for hora in llegadas:
        print(hora)


#Funcion: rutas_loop
#Entrada: ninguna
#Salida: crea una ventana con las rutas del dia
#Restricciones: ninguna
def rutas_loop():
    ventana.withdraw()
    #Crea la ventana
    rutas = Toplevel()
    rutas.minsize(windowWidth, windowHeight)
    c_rutas = Canvas(rutas)
    c_rutas.pack(fill=BOTH, expand=True)

    #Carga el fondo
    fondo = cargarImagen("fondo claro.png",1)
    c_rutas.create_image(0,0,image = fondo,anchor = NW)

    #Funcion de volver
    def salirRutas():
        rutas.destroy()
        ventana.deiconify()

    # Boton volver
    backButton = cargarImagen("back button.png", 0.1)
    botonVolver = Button(c_rutas, image=backButton, command=salirRutas, bg="#000000")
    botonVolver.place(relx=0.05, rely=0.05)


    #Titulo
#    c_rutas.create_text(windowWidth//2,windowHeight//10,text = "Rutas de hoy", font = (font, 40),anchor = CENTER, fill="#FFFFFF")

    #Horarios
    textos = []
    ultimaRuta = trenesDia[0].ruta.replace("\n", "")
    textos.append(ultimaRuta)
    horas = ""
    for tren in trenesDia:
        if tren.ruta.replace("\n", "") != ultimaRuta:
            ultimaRuta = tren.ruta.replace("\n", "")
            textos.append(horas)
            textos.append(ultimaRuta)
            horas = ""
        if tren.hora[1] < 10:
            minutos = "0" + str(tren.hora[1])
        else:
            minutos = str(tren.hora[1])
        horas += str(tren.hora[0]) + ":" + minutos + " "
    textos.append(horas)
    
    posicionTextos = 140
    aumento = (windowHeight - 140) // len(textos)

    c_rutas.create_text(windowWidth // 2, posicionTextos/2 , text="RUTAS DE HOY", font=(font, int(aumento/2), "bold"), fill="#000000")
    
    for texto in textos:
        c_rutas.create_text(windowWidth // 2, posicionTextos, text=texto, font=(font, int(aumento/3)), anchor=N, fill="#000000")
        posicionTextos += aumento


    rutas.mainloop()



def animacion(): #Da error al cerrar la ventana
    while True:
        hora = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
        reloj.config(text=hora)
        time.sleep(1)

def formar_tren(tren):
    temp = tren.head
    imagenMaquina = cargarImagen("maquina.png", 0.5)
    c_ventana.create_image(100, 600, image = imagenMaquina)
    pos = 235
    largoTren = 135
    c_ventana.vagon = cargarImagen("vagon.png",0.5)
    while temp != None:
        c_ventana.create_image(pos,600,image = c_ventana.vagon)
        c_ventana.update()
        temp = temp.next
        pos += largoTren


def diccionario_trenes (trains):
    dicc = {}
    for train in trains:
        clave = train.ruta + " - " + str(train.hora[0]) + ":" + str(train.hora[1])
        if train.hora[1] == 0:
            clave += "0"
        dicc[clave] = train
    return dicc

trains2 = diccionario_trenes(trains)
    
def refresh ():
    global menu
    menu["menu"].delete(0,'end')
    tren_menu.set("RUTAS")
    for train in trains2:
        if trains2[train].get_hora()[0] == datetime.datetime.now().hour:
            menu["menu"].add_command(label=train, command = lambda frase = train : tren_menu.set(frase))
  
    
"""__________________________________________________________________________"""

trains2["TEC-Cartago - 15:00"].optimizar(75)

#Funcion: timer
#Entrada: ninguna
#Salida: ejecuta las acciones de los trenes de acuerdo a la hora
#Restricciones: ninguna
def timer():
    while True:
        hora = datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
        trains_copy = trains[:]
        for tren in trains_copy:
            if tren.enEstacion == True and (hora[0] > tren.hora[0] or (hora[0] == tren.hora[0] and hora[1] > tren.hora[1])): #Elimina los trenes que ya pasaron
                trains.remove(tren)

            elif tren.enEstacion == False and hora[:2] == tren.hora and hora[2] == 0: #Llega los trenes
                tren.llegar()
        time.sleep(1)
"""__________________________________________________________________________"""


#Crear ventana 
ventana = Tk()
windowWidth = ventana.winfo_screenwidth()
windowHeight = windowWidth * 9 // 16
ventana.minsize(windowWidth, windowHeight)
ventana.resizable(False,False)
ventana.title("Estación TEC")

#Crear canvas
c_ventana = Canvas(ventana)
c_ventana.pack(fill=BOTH, expand=True)

#Imagenes botones
botonSettings = cargarImagen("boton settings.png",0.15)
botonInfo = cargarImagen("boton info.png", 0.15)
font = "Courier New"
bfSize = 16

#Carga fondo
fondo = cargarImagen("estacion.png", 1)
c_ventana.create_image(0, 0, image=fondo, anchor=NW)

#Boton para ir a rutas
boton_rutas = Button(ventana, image=botonInfo, borderwidth=0, command=rutas_loop, relief=FLAT)
boton_rutas.place(relx=0.005, rely=0.01)

boton_vagon = Button(ventana, image=botonSettings, borderwidth=0, command=lambda:formar_tren(trains2[tren_menu.get()]), relief=FLAT)
boton_vagon.place(relx=0.005, rely=0.125)

tren_menu = StringVar(c_ventana)
tren_menu.set("RUTAS")
menu = OptionMenu(c_ventana,tren_menu,None)
refresh()
menu.config(bg = "#6fc5cb", relief = FLAT,highlightbackground = "#6fc5cb", font = (font, bfSize))
menu["menu"].config(bg = "WHITE",relief = FLAT,font = (font, bfSize))
menu.place(relx=0.18, rely=0.04)


#Hora
hora = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
#c_ventana.create_text(windowWidth // 2, windowHeight // 10, text=hora, font=(font, 30), anchor=CENTER)
reloj = Label(c_ventana, text=hora, bg="#6fc5cb", font=(font, 30))
reloj.place(relx=0.5, rely= 0.075, anchor=CENTER)

tiempo = Thread(target=animacion, args=())
tiempo.start()

hiloTimer = Thread(target=timer, args=())
hiloTimer.start()


#Pruebas
#mostrar(vagonesLibres)
#mostrar(trains)
#ruta_hora(trains, 23)

ventana.mainloop()

