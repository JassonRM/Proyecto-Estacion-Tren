#importar modulos necesarios
import pygame
import os
import sys
from threading import Thread
import time 

#definir colores
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
bg_color = (240, 255, 255)

#inicializar pygame
pygame.init()
clock = pygame.time.Clock()

def cargarImagen(nombre):
    #ruta = os.path.join(nombre)
    imagen = pygame.image.load(nombre)
    return imagen

#Funcion: scale_img
#Entradas: imagen, ancho y altura
#Salida: imagen reescalada
#Restricciones: imagen de tipo pygame, ancho y altura son enteros
def scale_img(image,width,height):    
    image = pygame.transform.smoothscale(image,(width,height))
    return image

def buttonPressed(rect,mouse):
    left = rect[0]
    top = rect[1]
    width = rect[2]
    height = rect[3]
    if mouse[0] > left and mouse[0] < left + width and mouse[1] > top and mouse[1] < top + height:
        return True
    else:
        return False
        

class Text:
    def __init__(self,font = 'microsoftyaheimicrosoftyaheiui',bold = False,italic = False,size = 25,underline = False):
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.size = size
        self.space = (0,0)
        self.color = white
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
    def set_color(self,color):
        self.color = color

        
        
screenWidht = 800
screenHeight = 600
ventana = pygame.display.set_mode([screenWidht,screenHeight])


bSize = (190, 110)
cSize = [80,35]
ListaRutas = [30, 140]
Demanda = [570,140]
Llegada = [570,335]
Salida = [570,365]
Llegada_salida = [570,350]
Administrar = [30,335]
Vagones = [30,365]
Administrar_v = [30,350]
Time = [360,15]




def Menu_loop():
    in_menu = True
    fondoMenu = cargarImagen("fondo1.png")
    text_ListasRutas = Text()
    text_demanda = Text()
    text_llegada = Text()
    text_salida = Text()
    text_administrar = Text()
    text_vagones = Text()
    text_time = Text()
    botones = [[pygame.Rect(ListaRutas[0],ListaRutas[1],bSize[0],bSize[1]),text_ListasRutas,Lista_Rutas_loop],
               [pygame.Rect(Demanda[0],Demanda[1],bSize[0],bSize[1]),text_demanda,Demanda_loop],
               [pygame.Rect(Llegada_salida[0],Llegada_salida[1],bSize[0],bSize[1]),text_llegada,Llegadas_loop],
               [pygame.Rect(Llegada_salida[0],Llegada_salida[1],bSize[0],bSize[1]),text_salida,Llegadas_loop],
               [pygame.Rect(Administrar_v[0],Administrar_v[1],bSize[0],bSize[1]),text_administrar,Administrar_loop],
               [pygame.Rect(Administrar_v[0],Administrar_v[1],bSize[0],bSize[1]),text_vagones,Administrar_loop]]

    while in_menu:    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for boton in botones:
                if buttonPressed(boton[0],pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        boton[2]()
                        in_menu = False
                        break
                    boton[1].set_color(white)
                else:
                    boton[1].set_color(black)

            rutas = text_ListasRutas.render(" Lista Rutas",bSize, ListaRutas)
            demanda = text_demanda.render(" Demanda",bSize, Demanda)
            llegada = text_llegada.render(" Llegadas/",bSize,Llegada)
            salida = text_salida.render(" Salidas",bSize,Salida)
            administrar = text_administrar.render( "Administrar",bSize, Administrar)
            clock = "Hora: " + str(time.asctime())[10:-4] + "/ Fecha:" + str(time.asctime())[3:10] + str(time.asctime())[-5:]
            vagones = text_vagones.render( "Vagones",bSize, Vagones)
            time1 = text_time.render(clock,cSize,Time)
            

            ventana.blit(fondoMenu,(0,0))
            ventana.blit(rutas[0],rutas[1])
            ventana.blit(demanda[0],demanda[1])
            ventana.blit(llegada[0],llegada[1])
            ventana.blit(salida[0],salida[1])
            ventana.blit(administrar[0],administrar[1])
            ventana.blit(vagones[0],vagones[1])
            ventana.blit(time1[0],time1[1])
            pygame.display.update()

    

def Lista_Rutas_loop():
    in_rutas = True
    fondo = cargarImagen("metallic2.jpg")
    while in_rutas:
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()
        
def Demanda_loop():
    in_demanda = True
    fondo = cargarImagen("metallic2.jpg")
    while in_demanda:
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

def Llegadas_loop():
    in_llegadas = True
    fondo = cargarImagen("metallic2.jpg")
    while in_llegadas:
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

def Administrar_loop():
    in_administrar = True
    fondo = cargarImagen("metallic2.jpg")
    while in_administrar:
        
        ventana.blit(fondo,(0,0))
        pygame.display.update()

    


Menu_loop()
