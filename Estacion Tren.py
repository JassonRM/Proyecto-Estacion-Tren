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
import datetime

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
    def __init__(self,font = 'microsoftyaheimicrosoftyaheiui',bold = False,italic = False,size = fontSize,underline = False, texto = ""):
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.size = size
        self.space = (0,0)
        self.color = white
        self.texto = texto

    #Metodo: render
    #Entrada: texto a mostrar, posición de la superficie donde se desea centrar,
    #posición de la superficie donde se desea colocar
    #Salida: texto listo para mostrar y tupla con posicion del texto
    #Restricciones: posiciones deben ser tuplas
    def render(self,texto = None,bSize=(0,0),bDimensions=(0,0)):
        if texto == None:
            texto = self.texto
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

    def mostrar(self):
        print(self.texto)

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
enEjecucion = True

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
            hora = int(line[0:2]), int(line[3:])
            trains.append(Tren(id=newTrainID, ruta=ruta, hora = hora))
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
    global enEjecucion
    in_menu = True
    
    #cargar imagen de fondo
    fondoMenu = scale_img(cargarImagen("fondo.jpg"),windowWidth,windowHeight)

    #Definir posición de botones 
    boton_top = int(windowHeight*5/24)
    boton_left = int(windowWidth*15/256)
    boton_bottom = int(windowHeight*16/29)
    boton_right = int(windowWidth*131/183)

    # posición del texto time
    Time = (int(windowWidth*0.5),int(windowHeight*0.1))

    #crear Texto de Hora
    text_time = Text()
    
    #textos = [(posicionx,posiciony,texto,comando)]
    textos = [(boton_left,boton_top,Text(texto = "Lista Rutas"),Lista_Rutas_loop),(boton_right,boton_top,Text(texto = "Estación"),Demanda_loop),
              (boton_right,boton_bottom,Text(texto = "Llegadas/"),Llegadas_loop),(boton_right,boton_bottom,Text(texto = "Salidas"),Llegadas_loop),
              (boton_left,boton_bottom,Text(texto = "Administrar"),Administrar_loop),(boton_left,boton_bottom,Text(texto = "Vagones"),Administrar_loop)]


    #boton = (cordenada rectangular,texto,comando)
    botones = []
    for texto in textos:
        botones.append((pygame.Rect(texto[0],texto[1],bSize[0],bSize[1]),texto[2],texto[3]))

    #ciclo principal de ventana
    while in_menu:
            #cerrar ventana
            for event in pygame.event.get():
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        enEjecucion = False
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
            
            #actualiza la hora
            clock = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
            clock = text_time.render(texto = clock,bDimensions = Time)

            #Muestra el fondo y la hora
            ventana.blit(fondoMenu,(0,0))
            ventana.blit(clock[0],clock[1])

            #actualiza y muestra textos
            for boton in botones:
                if boton[1].texto == "Administrar" or boton[1].texto == "Llegadas/":
                    mensaje = boton[1].render(bSize = bSize,bDimensions = (boton[0][0],boton[0][1]-fontSize//2))
                elif boton[1].texto == "Vagones" or  boton[1].texto == "Salidas":
                    mensaje = boton[1].render(bSize = bSize,bDimensions = (boton[0][0],boton[0][1]+fontSize//2))
                else:
                    mensaje = boton[1].render(bSize = bSize,bDimensions = (boton[0][0],boton[0][1]))
                ventana.blit(mensaje[0],mensaje[1])

            #Actualiza ventana
            pygame.display.update()

    
#ciclo de Listas de Rutas
def Lista_Rutas_loop():
    global enEjecucion
    in_rutas = True
    fondo = scale_img(cargarImagen("metallic2.jpg"), windowWidth, windowHeight)
    textos = [Text(size=windowWidth // 20, texto="Rutas de hoy" )]
    ultimaRuta = trains[0].ruta.replace("\n", "")
    textos.append(Text(texto=ultimaRuta))
    horas = ""
    for tren in trains:
        if tren.ruta.replace("\n", "") != ultimaRuta:
            ultimaRuta = tren.ruta.replace("\n", "")
            textos.append(Text(texto=horas))
            textos.append(Text(texto=ultimaRuta))
            horas = ""
        if tren.hora[1] < 10:
            minutos = "0" + str(tren.hora[1])
        horas += str(tren.hora[0]) + ":" + minutos + " "
    textos.append(Text(texto=horas.replace("\n","", )))

    while in_rutas:
        posicionTextos = windowHeight // 10
        #cerrar ventana
        iconoAtras = "atras.png"
        botonAtras = pygame.Rect(windowWidth // 10, windowHeight // 10, windowWidth // 10, windowHeight // 5.62)
        if buttonPressed(botonAtras, pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                Menu_loop()
            iconoAtras = "atras1.png"
        else:
            iconoAtras = "atras.png"

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enEjecucion = False
                    pygame.quit()
                    sys.exit()
        ventana.blit(fondo,(0,0))
        ventana.blit(scale_img(cargarImagen(iconoAtras), windowWidth // 10, int(windowHeight // 5.62)), (windowWidth//10, windowHeight // 10))
        for texto in textos:
            rotulo = texto.render(bDimensions=(windowWidth // 2, posicionTextos))
            ventana.blit(rotulo[0], rotulo[1])
            posicionTextos += 80
        pygame.display.update()

#ciclo de Demandas
def Demanda_loop():
    global enEjecucion
    in_demanda = True
    fondo = scale_img(cargarImagen("metallic2.jpg"), windowWidth, windowHeight)
    while in_demanda:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enEjecucion = False
                    pygame.quit()
                    sys.exit()
                    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

#ciclo de Llegadas
def Llegadas_loop():
    global enEjecucion
    in_llegadas = True
    fondo = scale_img(cargarImagen("metallic2.jpg"), windowWidth, windowHeight)
    while in_llegadas:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enEjecucion = False
                    pygame.quit()
                    sys.exit()    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

def Administrar_loop():
    global enEjecucion
    in_administrar = True
    fondo = scale_img(cargarImagen("metallic2.jpg"), windowWidth, windowHeight)
    while in_administrar:

        #cerrar ventana
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enEjecucion = False
                    pygame.quit()
                    sys.exit()    
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

def reloj():
    while enEjecucion:
        hora = datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
        for tren in trains:
            if tren.enEstacion == False and hora[:2] == tren.hora and hora[2] == 0:
                tren.llegar()
        clock.tick(1)



reloj = Thread(target=reloj, args=())
reloj.start()
Menu_loop()

