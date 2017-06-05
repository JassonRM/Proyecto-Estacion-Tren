# Tercer proyecto programado
# Estacion de Tren
# Jasson Rodriguez
# Marco Herrera

import sys
import os
import pygame
import ast

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

trains = []
newTrainID = 0

with open("estacion.txt") as config:
    vagonesLibres = ast.literal_eval(config.readline())

    for line in config:
        if line.find("Ruta") != -1:
            trains.append(Tren(id = newTrainID, ruta = line.replace("Ruta ", ""), '''maquina'''))
            newTrainID += 1
            
print(vagonesLibres)

pygame.init()
windowWidth = pygame.display.Info().current_w
windowHeight = pygame.display.Info().current_h

