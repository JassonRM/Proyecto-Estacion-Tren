# Tercer proyecto programado
# Estacion de Tren
# Jasson Rodriguez
# Marco Herrera

import sys
import os
from tkinter import *
from tkinter import messagebox
import pygame
import random
from threading import Thread
import time
import datetime
from PIL import Image, ImageTk

pygame.mixer.init()

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen
#Restricciones: el archivo debe estar contenido en la carpeta Imagenes
def cargarImagen(nombre,tamaño,right = False):
    ruta = os.path.join("Imagenes", nombre)
    imagen = Image.open(ruta)
    imagen.thumbnail((tamaño * windowWidth,tamaño * windowHeight))
    if right:
        imagen = imagen.transpose(Image.FLIP_LEFT_RIGHT)
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

    def __str__(self):
        if self.hora[1] < 10:
            minutos = "0" + str(self.hora[1])
        else:
            minutos = str(self.hora[1])
        return str(self.ruta) + " - " + str(self.hora[0]) + ":" + minutos

    def get_hora(self):
        return self.hora

    #Metodo: optimizar
    #Entrada: demanda
    #Salida: asigna los vagones y la maquina de acuerdo a la demanda existente
    #Restricciones: demanda es un entero positivo
    def optimizar(self, demanda):
        if self.enEstacion:
            listaVagones = vagonesLibres[:]
            listaMaquinas = maquinasLibres[:]
        else:
            listaVagones = vagonesFuera[:]
            listaMaquinas = maquinasFuera[:]

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

            elif pos == self.carga - 1:
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
                        cont += 1
            vagonesLibres.append(temp)
            self.carga -= 1

        elif self.maquina == None:
            print("No hay máquina asignada")
        elif self.carga == 0:
            print("No hay vagones asignados")
        else:
            print("Capacidad de la máquina alcanzada")
    #Metodo: quitarTodos
    #Entrada: ninguna
    #Salida: elimina todos los vagones y maquinas del tren
    #Restricciones: ninguna
    def quitarTodos(self):
        for vagon in range(self.carga):
            self.quitarVagon(0)

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
        if self.maquina != None:
            print("Maquina: ")
            self.maquina.mostrar()
        if self.maquina != None and self.head != None:
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
with open("estacion.txt",encoding='utf-8-sig') as config:
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
    rutas.focus_force()
    rutas.overrideredirect(True)
    rutas.geometry("%dx%d+0+0" %(windowWidth,windowHeight))
    c_rutas = Canvas(rutas)
    c_rutas.pack(fill=BOTH, expand=True)

    #Carga el fondo
    fondo = cargarImagen("fondo.png",1)
    c_rutas.create_image(0,0,image = fondo,anchor = NW)

    #Funcion de volver
    def salirRutas():
        rutas.destroy()
        ventana.deiconify()
        ventana.focus_force()

    # Boton volver
    backButton = cargarImagen("back button.png", 0.1)
    botonVolver = Button(c_rutas, image=backButton, command=salirRutas, bg="#313139", relief=FLAT)
    botonVolver.place(relx=0.05, rely=0.05)

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

    #Posiciones de los textos
    posicionTextos = 140
    aumento = (windowHeight - 140) // len(textos)

    #Titulo de la pantalla
    c_rutas.create_text(windowWidth // 2, posicionTextos/2 , text="RUTAS DE HOY", font=(font, int(aumento/2), "bold"), fill="#000000")

    for texto in textos:
        c_rutas.create_text(windowWidth // 2, posicionTextos, text=texto, font=(font, int(aumento/3)), anchor=N, fill="#000000")
        posicionTextos += aumento

    rutas.bind("<Escape>", cerrar)
    rutas.mainloop()

#Funcion: armar_loop
#Entrada: ninguna
#Salida: crea una ventana para modificar el tren
#Restricciones: ninguna
def armar_loop():
    if tren == None:
        messagebox.showerror("Tren no seleccionado", "No se ha seleccionado un tren para modificar")
    else:
        ventana.withdraw()

        # Crea la ventana
        armar = Toplevel()
        armar.overrideredirect(True)
        armar.geometry("%dx%d+0+0" %(windowWidth,windowHeight))
        armar.focus_force()
        def armar1():
            c_armar = Canvas(armar)
            c_armar.pack(fill=BOTH, expand=True)

            #Carga el fondo
            fondo = cargarImagen("fondo.png",1)
            c_armar.create_image(0,0,image = fondo,anchor = NW)

            #Funcion de volver
            def salirArmar():
                armar.destroy()
                ventana.deiconify()
                salir_tren(tren.carga)
                ventana.focus_force()

            # Boton volver
            backButton = cargarImagen("back button.png", 0.1)
            botonVolver = Button(c_armar, image=backButton, command=salirArmar, bg="#313139", relief=FLAT)
            botonVolver.place(relx=0.05, rely=0.05)

            #Botones asignar
            def asignar(id):
                tren.asignarMaquina(id)
                c_armar.destroy()
                armar2()

            #Titulo de la pantalla
            c_armar.create_text(windowWidth * 0.5, 70 , text="Asignación de máquina", font=(font, int((windowHeight - 140)/20), "bold"), fill="#000000")
            demanda = "Demanda: " + str(tren.demanda)
            c_armar.create_text(windowWidth * 0.85, 70 , text=demanda, font=(font, int(windowHeight // 30)), fill="#000000")

            #Cargar boton
            botonAsignar = cargarImagen("boton asignar.png", 0.1)

            #Posiciones
            pos = 170
            aumento = 140

            for maquina in maquinasLibres:
                datos = "ID: " + str(maquina.id) + "   Capacidad: " + str(maquina.capacidad) + " vagones"
                c_armar.create_text(windowWidth * 42 // 100, pos, text=datos, font=(font, windowHeight // 30), fill="#000000", anchor=CENTER)
                boton = (Button(c_armar, image = botonAsignar, command=lambda maquina=maquina: asignar(maquina.id), bg="#313139", relief=FLAT)) #El comando debe llevar maquina=maquina para evitar que maquina se asigne luego de que haya terminado el ciclo
                boton.place(x=windowWidth * 67 // 96, y=pos, anchor=W)
                pos += aumento #(windowHeight - 140) // len(maquinasLibres)
                if pos > windowHeight:
                    break

            armar.bind("<Escape>", cerrar)
            armar.mainloop()

        def armar2():
            c_armar = Canvas(armar)
            c_armar.pack(fill=BOTH, expand=True)
            
            # Carga el fondo
            fondo = cargarImagen("fondo.png", 1)
            c_armar.create_image(0, 0, image=fondo, anchor=NW)

            # Funcion de volver
            def salirArmar():
                tren.quitarTodos()
                c_armar.destroy()
                armar1()

            # Boton volver
            backButton = cargarImagen("back button.png", 0.1)
            botonVolver = Button(c_armar, image=backButton, command=salirArmar, bg="#313139", relief=FLAT)
            botonVolver.place(relx=0.05, rely=0.05)

            #Cargar botones
            botonInicio = cargarImagen("boton asignar inicio.png", 0.1)
            botonMedio = cargarImagen("boton asignar pos.png", 0.118)
            botonFinal = cargarImagen("boton asignar final.png", 0.1)
            botonQuitar = cargarImagen("boton quitar.png", 0.08)
            botonSalir = cargarImagen("boton salir.png", 0.13)

            # Botones asignar
            def engancharInicio(id):
                tren.engancharInicio(id)
                c_armar.destroy()
                armar2()
            def engancharMedio(id, pos):
                tren.engancharMedio(id, int(pos))
                c_armar.destroy()
                armar2()
            def engancharFinal(id):
                tren.engancharFinal(id)
                c_armar.destroy()
                armar2()
            def quitarVagon(pos):
                tren.quitarVagon(pos)
                c_armar.destroy()
                armar2()
            def asignar():
                if tren.demanda <= tren.capacidad:
                    print("Vagones asignados, deberia mostrar el tren")
                    c_armar.destroy()
                    ventana.deiconify()
                else:
                    restante = tren.demanda - tren.capacidad
                    messagebox.showwarning("Capacidad insuficiente", "Faltan " + str(restante) + " asientos para suplir la demanda")


            # Titulo de la pantalla
            c_armar.create_text(windowWidth // 2, 70, text="Asignación de vagones", font=(font, int((windowHeight - 140) / 20), "bold"), fill="#000000")
            demanda = "Demanda: " + str(tren.demanda)
            c_armar.create_text(windowWidth * 0.85, 70 , text=demanda, font=(font, int(windowHeight // 30)), fill="#000000")

            #Posiciones
            pos = 205
            aumento = (windowHeight - 400) // (tren.carga + len(vagonesLibres))
            if aumento > 100:
                aumento = 100
            elif aumento < 60:
                aumento = 60

            #Boton asignar
            boton_salir = Button(c_armar, image=botonSalir, command=asignar, bg="#313139", relief=FLAT)
            boton_salir.place(relx=0.9, y= windowHeight - 100, anchor=CENTER)

            #Quitar vagones
            if tren.head != None:
                temp = tren.head
                cont = 0
                while temp != None:
                    datos = "ID: " + str(temp.id) + "  Capacidad: " + str(temp.capacidad) + " personas Posición: " + str(cont)
                    c_armar.create_text(windowWidth * 0.07, pos, text=datos, font=(font, windowHeight // 30), fill="#000000", anchor=W)
                    boton = Button(c_armar, image=botonQuitar, command=lambda posicion = cont: quitarVagon(posicion), bg="#313139", relief=FLAT) #Arreglar comando
                    boton.place(relx= 0.775, y=pos, anchor=W)
                    pos += aumento
                    cont += 1
                    temp = temp.next

            #Seleccionar vagones nuevos
            for vagon in vagonesLibres:
                datos = "ID: " + str(vagon.id) + "  Capacidad: " + str(vagon.capacidad) + " personas"

                #Menu
                varPos = StringVar()
                varPos.set("-")
                posList = range(tren.carga + 1)
                menuPos = OptionMenu(c_armar, varPos, *posList, command=lambda pos, varPos=varPos: varPos.set(pos)) #Necesito una varPos para cada vagon
                menuPos.place(relx= 0.805, y=pos, anchor=CENTER)

                #Botones
                c_armar.create_text(windowWidth * 0.07, pos, text=datos, font=(font, windowHeight // 30), fill="#000000", anchor=W)
                boton = Button(c_armar, image=botonInicio, command=lambda vagon=vagon: engancharInicio(vagon.id), bg="#313139", relief=FLAT)#Arreglar comando
                boton.place(relx= 0.55, y=pos, anchor=W)
                boton2 = Button(c_armar, image=botonMedio, command=lambda vagon=vagon, varPos=varPos: engancharMedio(vagon.id, varPos.get()), bg="#313139", relief=FLAT)#Arreglar comando
                boton2.place(relx= 0.66, y=pos, anchor=W)
                boton3 = Button(c_armar, image=botonFinal, command=lambda vagon=vagon: engancharInicio(vagon.id), bg="#313139", relief=FLAT)#Arreglar comando
                boton3.place(relx= 0.83, y=pos, anchor=W)


                pos += 140  # (windowHeight - 140) // len(maquinasLibres)
                pos += aumento
                if pos > windowHeight - 200:
                    break
            armar.bind("<Escape>", cerrar)
            armar.mainloop()

        armar1()
    
#Funcion: actualizar_hora
#Entradas: ninguna
#Salidas: actualiza la hora en pantalla
#Restricciones ninguna
def actualizar_hora():
    while enEjecucion:
        hora = str(time.asctime())[10:-4] + "/" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
        reloj.config(text=hora)
        time.sleep(1)

#Funcion: animacion_llegada
#Entradas: cantidad de vagones
#salidas: lleva a cabbo la animacion de llegada de los trenes
#Restricciones: cantidad entera
def animacion_tren(cantidad,enEstacion):
    if cantidad == 0:
        return None

    tren = cargarSonido("tren.wav")
    tren.play()    

    if enEstacion:
        c_ventana.maquina = cargarImagen("maquina.png",0.5,True) 
        c_ventana.vagon = cargarImagen("vagon.png",0.5,True)
        velocidad = 5
        pos = -windowWidth*0.5
        altura = windowHeight*0.84
        v = [[c_ventana.create_image(0,altura,image = c_ventana.maquina, tags = "p",anchor = E),0]]
        condicion = windowWidth
    else:
        c_ventana.maquina = cargarImagen("maquina.png",0.5)
        c_ventana.vagon = cargarImagen("vagon.png",0.5)
        velocidad = -5
        pos = windowWidth*1.5
        altura = windowHeight*0.56
        v = [[c_ventana.create_image(windowWidth,altura,image = c_ventana.maquina, tags = "p",anchor = W),windowWidth]]
        condicion2 = 0
        
    for ele in range(cantidad):
        if enEstacion:
            v += [[c_ventana.create_image(pos,altura,image = c_ventana.vagon, tags = "p",anchor = E),pos]]
            pos -= windowWidth*0.5
            condicion2 = pos
            aumento = 1
        else: 
            v += [[c_ventana.create_image(pos,altura,image = c_ventana.vagon, tags = "p",anchor = W),pos]]
            pos += windowWidth*0.5
            condicion = pos
            aumento = -1
    
    tren.fadeout(2000)
    while condicion > condicion2:
        c_ventana.move("p",velocidad,0)
        condicion -= abs(velocidad)
        time.sleep(0.001)
        velocidad -= aumento*(1/100)
        if int(velocidad)  == 0:
            time.sleep(1)
            tren.play()
            tren.fadeout((cantidad+1)*1800)
            aumento = -aumento
        elif abs(velocidad) > 5:
            aumento = 0
    
    for ele in v:
        c_ventana.delete(ele[0])
        
    return None

#Declara el tren en uso
tren = None
        
#Funcion: Refresh
#Entradas: ninguna
#Salidas: Actualiza el menu de trenes segun la hora
#Restricciones: ninguna
def refresh ():
    global menu
    menu["menu"].delete(0,'end')
    tren_menu.set("RUTAS")

    def seleccion(objeto):
        global tren
        tren = objeto
        tren_menu.set(objeto)

    for train in trains:
        if train.get_hora()[0] == datetime.datetime.now().hour and train.enEstacion:
            menu["menu"].add_command(label=train, command=lambda tren = train: seleccion(tren))

"""__________________________________________________________________________"""

#Funcion: timer
#Entrada: ninguna
#Salida: ejecuta las acciones de los trenes de acuerdo a la hora
#Restricciones: ninguna
def timer():
    while enEjecucion:
        hora = datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
        trains_copy = trains[:]
        for tren in trains_copy:
            if tren.enEstacion == True and (hora[0] > tren.hora[0] or (hora[0] == tren.hora[0] and hora[1] > tren.hora[1])): #Elimina los trenes que ya pasaron
                trains.remove(tren)

            elif tren.enEstacion == False and hora[:2] == tren.hora and hora[2] == 0: #Llega los trenes
                tren.llegar()
                animacion_tren(tren.carga,False)
                
        time.sleep(1)
"""__________________________________________________________________________"""

def salir_tren(cant):
    animacion_salir = Thread(target= animacion_tren,args = (cant,True))
    animacion_salir.start()


#Funcion: cerrar
#Entrada: ninguna
#Salida: termina todos los procesos
#Restricciones: ninguna
def cerrar(event):
    global enEjecucion
    enEjecucion = False
    ventana.destroy()

#Crear ventana
ventana = Tk()
windowWidth = ventana.winfo_screenwidth()
windowHeight = windowWidth * 9 // 16
ventana.overrideredirect(True)
ventana.geometry("%dx%d+0+0" %(windowWidth,windowHeight))
ventana.title("Estación TEC")

#Crear canvas
c_ventana = Canvas(ventana)
c_ventana.pack(expand = True, fill = BOTH)

#Imagenes botones
tamano = 0.13
botonSettings = cargarImagen("boton settings.png",tamano)
botonInfo = cargarImagen("boton info.png", tamano)
botonOptimizar = cargarImagen("boton optimizar.png", tamano)
font = "Courier New"
bfSize = 16

#Carga fondo
fondo = cargarImagen("estacion.png", 1)
c_ventana.create_image(0, 0, image=fondo, anchor=NW)

#Boton para ir a rutas
boton_rutas = Button(ventana, image=botonInfo, borderwidth=0, command=rutas_loop, relief=FLAT)
boton_rutas.place(relx=0.005, rely=0.01)

#Boton para asignacion manual
boton_vagon = Button(ventana, image=botonSettings, borderwidth=0, command=armar_loop)#lambda:formar_tren(trains2[tren_menu.get()]), relief=FLAT)
boton_vagon.place(relx=0.850, rely=0.01, anchor=NE)

#Boton para optimizar
boton_vagon = Button(ventana, image=botonOptimizar, borderwidth=0, command=armar_loop)#lambda:formar_tren(trains2[tren_menu.get()]), relief=FLAT)
boton_vagon.place(relx=0.860, rely=0.01, anchor=NW)


#Crea el menu
tren_menu = StringVar(c_ventana)
tren_menu.set("RUTAS")
menu = OptionMenu(c_ventana,tren_menu,None)
refresh()
menu.config(bg = "#6fc5cb", relief = FLAT,highlightbackground = "#6fc5cb", font = (font, bfSize))
menu["menu"].config(bg = "WHITE",relief = FLAT,font = (font, bfSize))
menu.place(relx=0.8555, rely=0.14, anchor=S)

#Hora
hora = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
#c_ventana.create_text(windowWidth // 2, windowHeight // 10, text=hora, font=(font, 30), anchor=CENTER)
reloj = Label(c_ventana, text=hora, bg="#6fc5cb", font=(font, 30))
reloj.place(relx=0.5, rely= 0.075, anchor=CENTER)

#Inicia el hilo del reloj
tiempo = Thread(target=actualizar_hora, args=())
tiempo.start()

#Inicia el hilo de llegadas
hiloTimer = Thread(target=timer, args=())
hiloTimer.start()

ventana.focus_force()
ventana.bind("<Escape>", cerrar)
ventana.mainloop()

