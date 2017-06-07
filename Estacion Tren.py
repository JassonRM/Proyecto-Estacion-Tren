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
        if ruta.find("TEC") == 0:
            self.enEstacion = True
            self.maquina = None
            self.head = None
            self.tail = None
            self.carga = 0
            self.demanda = None
        else:
            self.enEstacion = False
            self.demanda = random.randrange(5, 75)
            #Codigo para optimizar la maquina y los vagones aplica aqui tambien
            self.maquina = Maquina()


    def asignarMaquina(self, id):
        for maquina in maquinasLibres:
            if maquina.id == id:
                if self.maquina != None:
                    maquinasLibres.append(self.maquina)
                self.maquina = maquina
                maquinasLibres.remove(maquina)
            elif maquina == maquinasLibres[-1]:
                print("Máquina no encontrada")

    def engancharInicio(self, id):
        if self.carga != self.maquina.capacidad and self.maquina != None:
            for vagon in vagonesLibres:
                if vagon.id == id:
                    temp = self.head
                    self.head = vagon
                    self.head.next = temp
                    if temp != None:
                        temp.prev = vagon
                    else:
                        self.tail = self.head
                    self.carga += 1
                    vagonesLibres.remove(vagon)
                    break
                elif vagon == vagonesLibres[-1]:
                    print("Vagón no encontrado")
        elif self.maquina == None:
            print("No hay máquina asignada")
        else:
            print("Capacidad de la máquina alcanzada")

    def engancharMedio(self, id, pos):
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

    def quitarVagon(self, pos):

    def salir(self):

    def llegar(self):

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
    for line in config:
        print(line)
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

trains[0].asignarMaquina(10)
trains[0].engancharInicio(100)

