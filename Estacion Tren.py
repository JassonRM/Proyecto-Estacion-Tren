# Tercer proyecto programado
# Estacion de Tren
# Jasson Rodriguez
# Marco Herrera

import sys
import os
import pygame
import random

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen
#Restricciones: el archivo debe estar contenido en la carpeta Imagenes
def cargarImagen(nombre):
    ruta = os.path.join("Imagenes", nombre)
    imagen = PhotoImage(file=ruta) #Depende del motor grafico
    return imagen

#Funcion: cargarSonido
#Entrada: nombre
#Salida: sonido
#Restricciones: el archivo debe estar contenido en la carpeta Audio
def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

class Tren:
    def __init__(self, id, ruta, hora):
        self.id = id
        self.ruta = ruta
        self.hora = hora
        self.demanda = random.randrange(5, 75)
        if ruta.find("TEC") == 0:
            self.enEstacion = True
            self.maquina = None
            self.head = None
            self.tail = None
            self.carga = 0
            self.capacidad = 0
        else:
            self.enEstacion = False
            self.optimizar(self.demanda)

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


    def asignarMaquina(self, id): #Acepta trenes en la estacion y afuera
        if self.enEstacion:
            listaMaquinas = maquinasLibres
        else:
            listaMaquinas = maquinasFuera
        for maquina in listaMaquinas:
            if maquina.id == id:
                if self.maquina != None:
                    maquinasLibres.append(self.maquina)
                self.maquina = maquina
                maquinasLibres.remove(maquina)
            elif maquina == maquinasLibres[-1]:
                print("Máquina no encontrada")

    def engancharInicio(self, id): #Acepta trenes en la estacion y afuera
        if self.enEstacion:
            listaVagones = vagonesLibres
        else:
            listaVagones = vagonesFuera

        if self.carga != self.maquina.capacidad and self.maquina != None:
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
                    vagonesLibres.remove(vagon)
                    break
                elif vagon == vagonesLibres[-1]:
                    print("Vagón no encontrado")
        elif self.maquina == None:
            print("No hay máquina asignada")
        else:
            print("Capacidad de la máquina alcanzada")

    def engancharMedio(self, id, pos): #Solo trenes en la estacion
        if self.carga != self.maquina.capacidad and self.maquina != None:
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

    def engancharFinal(self, id):
        print("Nuevo final")
    def quitarVagon(self, pos):
        print("Quitar vagonl")
    def salir(self):
        print("salir")
    def llegar(self):
        print("Llegar")

    def mostrar(self):
        print("ID : ", self.id)
        print("Ruta: ", self.ruta)
        print("Hora: ", self.hora)
        if self.maquina != None and self.head != None:
            temp = self.head
            while temp != None:
                temp.mostrar()
                print("\n")
                temp = temp.next

class Maquina:
    def __init__(self, id, capacidad):
        self.id = id
        self.capacidad = capacidad

    def mostrar(self):
        print("ID: ", id, " Capacidad: ", capacidad)

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


with open("estacion.txt") as config:
    vagonesLibres = eval(config.readline())
    maquinasLibres = eval(config.readline())
    vagonesFuera = eval(config.readline())
    maquinasFuera = eval(config.readline())
    for line in config:
        if line.find("Ruta") != -1:
            ruta = line.replace("Ruta ", "")
        else:
            trains.append(Tren(id=newTrainID, ruta=ruta, hora = line))
            newTrainID += 1

def mostrar(lista):
    for i in lista:
        i.mostrar()
        print("----------------------------")

pygame.init()
windowWidth = pygame.display.Info().current_w
windowHeight = pygame.display.Info().current_h



