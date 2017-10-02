#!/usr/bin/python

import subprocess ##Llamar al programa del buzzer
import time ## Delays
import requests, gspread ## Conexion a Google Sheets
from apiclient.discovery import build ## Conexion a Google Sheets
import os ## Utilizar la terminal
from os import system ## Utilizar la terminal
from oauth2client.service_account import ServiceAccountCredentials ## Conexion a Google Sheets
import ast
import numpy as np
import matplotlib.pyplot as plt

from pydrive.auth import GoogleAuth


import RPi.GPIO as GPIO ## Leds
from gspread.exceptions import CellNotFound
from threading import Thread
from sys import argv
import zbar
import picamera

import mmap

## Declaracion de Leds
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)

## Configuracion de hora en terminal
os.system("sudo service ntp stop")
os.system("sudo ntpd -gq")
os.system("sudo service ntp start")

## Enfocar la camara
os.system("uvcdynctrl -s Focus 180")
time.sleep(5)

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)

class UploadData:  
    def __init__(self):
        self._running = True
            
    def terminate(self):  
        self._running = False  

    def run(self):
        global flujo
        global flag

        mes = time.strftime('%m-%Y')
        folder_metadata = {'title' : str(mes),"parents":  [{"id": "0B1zkhucfn1WKTUtlTEJwci0wSmM"}], 'mimeType' : 'application/vnd.google-apps.folder'}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        
        while self._running:

            mes = time.strftime('%m-%Y')
            
            dia = time.strftime('%m-%d-%Y')

            time.sleep(10)

            ##print('test')

            mesnuevo = time.strftime('%m-%Y')

            dianuevo = time.strftime('%m-%d-%Y')
            if dianuevo != dia:
                print('dia cambio')
                f = open( 'Data/'+str(dia)+'.txt', 'a' )
                f.write( '0 0 23:59:59 0')
                f.close()

                
                OX = []
                OY = []

                fecha = time.strftime('%m-%d-%Y')

                with open ('Data/'+str(dia)+'.txt', 'rt') as in_file:
                    for line in in_file:
                        tab = line.split()
                        var1=tab[2].split(":")
                        seg=int(var1[0])*3600+int(var1[1])*60+int(var1[2])-28800
                        OY.append(int(tab[3]))
                        OX.append(seg)
                                          
                ##fig, ax = plt.subplots()

                plt.figure(figsize=( 16,9), dpi=100)

                plt.scatter(OX,OY)

                #plt.figure(figsize=(7.195,3.841), dpi=100)

                plt.xlabel('Hora')
                plt.ylabel('Cantidad de alumnos')
                plt.title('Cantidad de alumnos ' + dia)

                plt.xticks([w*3600 for w in range(17)], 
                  ["8:00 am","9:00 am","10:00 am","11:00 am","12:00 mm","1:00 pm","2:00 pm","3:00 pm","4:00 pm","5:00 pm","6:00 pm","7:00 pm","8:00 pm","9:00 pm","10:00 pm","11:00 pm"], rotation=90)
                plt.axis([0, 55000, 0, 40])
                plt.tight_layout()


                plt.savefig('Data/'+str(dia)+".svg", dpi=1000)

                
                file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder['id']    }]})
                file1.SetContentFile('Data/'+str(dia)+'.txt')
                file1.Upload()
                
                file2 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder['id']    }]})
                file2.SetContentFile('Data/'+str(dia)+'.svg')
                file2.Upload()

                flujo=0
                flag=0
                dia=dianuevo
                
            if mesnuevo != mes:
                print('mes cambio')
                folder_metadata = {'title' : str(mesnuevo),"parents":  [{"id": "0B1zkhucfn1WKTUtlTEJwci0wSmM"}], 'mimeType' : 'application/vnd.google-apps.folder'}
                folder = drive.CreateFile(folder_metadata)
                folder.Upload()
                mes = mesnuevo
     ##############           
           
                
###########################################
            





#Create Class
UploadDataC = UploadData()
#Create Thread

UploadThread = Thread(target=UploadDataC.run) 
#Start Thread 
UploadThread.start()

system('python buzzer.py')
system('python buzzer.py')
GPIO.output(2,GPIO.HIGH)
GPIO.output(3,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(2,GPIO.OUT)
GPIO.output(3,GPIO.OUT)
time.sleep(0.5)
GPIO.output(2,GPIO.HIGH)
GPIO.output(3,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(2,GPIO.OUT)
GPIO.output(3,GPIO.OUT)
time.sleep(0.5)

flujo=0
flag=0

def Subir(codigo, fecha, hora, flag):
    #print(fecha)
    
    lines=[]
    
    with open ('Data/'+str(fecha)+'.txt', 'rt') as in_file:
        for line in in_file:
            if codigo in line:
                lines.append(line)
                
    if (len(lines)%2 == 0):
#        print("Entrada")
        flag=flag+1
        GPIO.output(2,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(2,GPIO.OUT)
    else:
 #       print("Salida")
        flag=flag-1
        GPIO.output(3,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(3,GPIO.OUT)

    return flag

def validar(codigo):
    print("Entre a la funcion validar")
    with open ('file2.csv', 'rt') as in_file:
        if codigo == "":
                print("PRENDER ROJO")
        else:
            for line in in_file:
                if codigo in line:
                    if "desaprobado" in line:
                        system('python buzzer.py')
                        #print("PRENDER ROJO")
                        GPIO.output(3,GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(3,GPIO.OUT)
                    else:
                        system('python buzzer.py')
                        #print("PRENDER AZUL")
                        GPIO.output(2,GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(2,GPIO.OUT)


# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# initialize the Processor
device = '/dev/video0'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

# setup a callback
def my_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:
        # do something useful with results
        print symbol.data
        
        global flag
        global flujo
        codigo = symbol.data
        system('python buzzer.py')
        fecha = time.strftime('%m-%d-%Y')
        hora = time.strftime('%m/%d/%Y %H:%M:%S')

        f = open( 'Data/'+str(fecha)+'.txt', 'a' )

        flag2=Subir(codigo,fecha,hora,flag)
        flujo=flujo+flag2

        
        f.write(codigo + " " + hora  + " "  +str(flujo) + '\n')
        f.close
       # print(flujo)
        
        #validar(codigo)
     

proc.set_data_handler(my_handler)

# enable the preview window
proc.visible = True

# initiate scanning
proc.active = True
try:
    # keep scanning until user provides key/mouse input
    proc.user_wait()
except zbar.WindowClosed, e:
    pass
