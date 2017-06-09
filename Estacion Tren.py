# Tercer proyecto programado
# Estacion de Tren
# Jasson Rodriguez
# Marco Herrera

import sys
import os
import pygame
import random
from threading import Thread
import time

#Definir colores
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

pygame.init()


windowWidth = pygame.display.Info().current_w 
windowHeight = pygame.display.Info().current_h
fontSize = int(windowWidth/32) # tamaño de letra

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen
#Restricciones: el archivo debe estar contenido en la carpeta Imagenes
def cargarImagen(nombre):
    ruta = os.path.join("Imagenes", nombre)
    imagen = pygame.image.load(ruta)
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
    return image

class Text:
    def __init__(self,font = 'microsoftyaheimicrosoftyaheiui',bold = False,italic = False,size = fontSize,underline = False):
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.size = size
        self.space = (0,0)
        self.color = white

    #Metodo: render
    #Entrada: texto a mostrar, posición de la superficie donde se desea centrar,
    #posición de la superficie donde se desea colocar
    #Salida: texto listo para mostrar y tupla con posicion del texto
    #Restricciones: posiciones deben ser tuplas
    def render(self,texto,bSize,bDimensions):
        font = pygame.font.SysFont(self.font,self.size)
        self.space = font.size(texto)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        font.set_underline(self.underline)
        text = font.render(texto,True,self.color)
        placex = bDimensions[0] + bSize[0]//2 - self.space[0]//2
        placey = bDimensions[1] + bSize[1]//2 - self.space[1]//2
        return text,(placex,placey)

    #Metodo: set_color
    #Entrada: color
    #Salida: Cambia el color de un texto
    #Restricciones: color debe ser RGB
    def set_color(self,color):
        self.color = color

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
                    maquinasLibres.append(self.maquina)
                self.maquina = maquina
                maquinasLibres.remove(maquina)
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
                    vagonesLibres.remove(vagon)
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
        print("Quitar vagonl")

    #Metodo: salir
    #Entrada: ninguna
    #Salida: el tren sale de la estacion, enEstacion pasa a False
    #Restricciones: maquina asignada y que cumpla con la demanda
    def salir(self):
        print("salir")

    #Metodo: llegar
    #Entrada: ninguna
    #Salida: el tren llega a la estacion, enEstacion pasa a True, la maquina y vagones quedan libres
    #Restricciones: ninguna
    def llegar(self):
        print("Llegar")

    #Metodo: mostrar
    #Entrada: ninguna
    #Salida: muestra los atributos y vagones del tren
    #Restricciones: ninguna
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

#Lectura de archivo de configuracion
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

#Funcion: mostrar
#Entrada: lista
#Salida: el metodo mostrar para cada elemento de la lista
#Restricciones: todos los objetos de la lista tienen el metodo mostrar
def mostrar(lista):
    for i in lista:
        i.mostrar()
        print("----------------------------")


"""__________________________________________________________________________"""

#inicializar Clock
clock = pygame.time.Clock()

#Crear ventana 
ventana = pygame.display.set_mode((windowWidth,windowHeight), pygame.FULLSCREEN)
pygame.display.set_caption("Estación TEC")

bSize = (windowWidth*0.225,windowHeight*0.225) # tamaño botones


#Funcion: buttonPressed
#Entrada: posicion del cursor y cordenadas rectangulares para revisar
#Salidas: Verifica si el cursor se encuentra entre las cordenadas
#restricciones: cordenadas son rectangulares
def buttonPressed(rect,mouse):
    left = rect[0]
    top = rect[1]
    width = rect[2]
    height = rect[3]
    if mouse[0] > left and mouse[0] < left + width and mouse[1] > top and mouse[1] < top + height:
        return True
    else:
        return False

#ciclo de Menu
def Menu_loop():
    in_menu = True
    
    #cargar imagen de fondo
    fondoMenu = scale_img(cargarImagen("fondo.png"),windowWidth,windowHeight)

    #Definir posición de botones 
    boton_top = int(windowHeight*5/24)
    boton_left = int(windowWidth*15/256)
    boton_bottom = int(windowHeight*16/29)
    boton_right = int(windowWidth*131/183)

    #Asignar posicion a cada boton
    ListaRutas = (boton_left,boton_top ) # posición del boton ListasRutas
    Demanda = (boton_right,boton_top) # posición del boton Demanda
    Llegada = (boton_right,boton_bottom - fontSize//2) # posición del texto Llegada
    Salida = (boton_right,boton_bottom + fontSize//1.5) # posición del texto Salida
    Llegada_salida = (boton_right,boton_bottom) # posición del boton LLegada-Salida
    Administrar = (boton_left,boton_bottom- fontSize//2)# posición del texto administrar
    Vagones = (boton_left,boton_bottom + fontSize//1.5)# posición del texto vagones
    Administrar_v = (boton_left,boton_bottom)# posición del boton administrar-vagones
    Time = (int(windowWidth*0.5),int(windowHeight*0.1))# posición del texto time

    #Crear instancias para los textos que se van a mostrar
    text_ListasRutas = Text()
    text_demanda = Text()
    text_llegada = Text()
    text_salida = Text()
    text_administrar = Text()
    text_vagones = Text()
    text_time = Text()

    #Crear rectangulos para los botones 
    botones = [[pygame.Rect(ListaRutas[0],ListaRutas[1],bSize[0],bSize[1]),text_ListasRutas,Lista_Rutas_loop],
               [pygame.Rect(Demanda[0],Demanda[1],bSize[0],bSize[1]),text_demanda,Demanda_loop],
               [pygame.Rect(Llegada_salida[0],Llegada_salida[1],bSize[0],bSize[1]),text_llegada,Llegadas_loop],
               [pygame.Rect(Llegada_salida[0],Llegada_salida[1],bSize[0],bSize[1]),text_salida,Llegadas_loop],
               [pygame.Rect(Administrar_v[0],Administrar_v[1],bSize[0],bSize[1]),text_administrar,Administrar_loop],
               [pygame.Rect(Administrar_v[0],Administrar_v[1],bSize[0],bSize[1]),text_vagones,Administrar_loop]]

    #ciclo principal de ventana
    while in_menu:
            #cerrar ventana
            for event in pygame.event.get():
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()    
    
            #revisa estado de todos los botones 
            for boton in botones:
                if buttonPressed(boton[0],pygame.mouse.get_pos()):
                #ejecuta la funcion respectiva para cada boton
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        boton[2]()
                        in_menu = False
                        break
                    #cambia color de texto
                    boton[1].set_color(white)
                else:
                    boton[1].set_color(black)

            #actualiza los textos de los botones 
            rutas = text_ListasRutas.render("Lista Rutas",bSize, ListaRutas)
            demanda = text_demanda.render("Demanda",bSize, Demanda)
            llegada = text_llegada.render("Llegadas/",bSize,Llegada)
            salida = text_salida.render("Salidas",bSize,Salida)
            administrar = text_administrar.render( "Administrar",bSize, Administrar)
            clock = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
            vagones = text_vagones.render( "Vagones",bSize, Vagones)
            time1 = text_time.render(clock,(0,0),Time)
            
            #muestra todo en ventana
            ventana.blit(fondoMenu,(0,0))
            ventana.blit(rutas[0],rutas[1])
            ventana.blit(demanda[0],demanda[1])
            ventana.blit(llegada[0],llegada[1])
            ventana.blit(salida[0],salida[1])
            ventana.blit(administrar[0],administrar[1])
            ventana.blit(vagones[0],vagones[1])
            ventana.blit(time1[0],time1[1])

            #actualiza ventana
            pygame.display.update()

    
#ciclo de Listas de Rutas
def Lista_Rutas_loop():
    in_rutas = True
    fondo = cargarImagen("metallic2.jpg")
    while in_rutas:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

#ciclo de Demandas
def Demanda_loop():
    in_demanda = True
    fondo = cargarImagen("metallic2.jpg")
    while in_demanda:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

#ciclo de Llegadas
def Llegadas_loop():
    in_llegadas = True
    fondo = cargarImagen("metallic2.jpg")
    while in_llegadas:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

def Administrar_loop():
    in_administrar = True
    fondo = cargarImagen("metallic2.jpg")
    while in_administrar:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()


Menu_loop()

