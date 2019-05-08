from ftplib import FTP
from time import time
import threading
import os

ftp = FTP('')
ftp.connect('localhost', 1026)
ftp.login()
ftp.cwd('Escritorio/ftp/ftp')  # Nombre de la carpeta que contendrá los archivos del servidor.
ftp.retrlines('LIST')
rutaArchivo = '/home/rublend/Escritorio/test.txt'  # Ruta del archivo a subir

def subirArchivo():
    nombre = 'test.txt'  # Nombre del archivo a subir.
    ftp.storbinary('STOR ' + nombre, open(rutaArchivo, 'rb'))
    ftp.quit()


def descargarArchivo():
    nombre = 'test.txt'  # Nombre del archivo a descargar.
    localfile = open(rutaArchivo, 'wb')
    ftp.retrbinary('RETR ' + nombre, localfile.write, 1024)
    ftp.quit()
    localfile.close()
def main():
    print("FTP MODULO")
    menu()
def menu():
    while 1:
        print(" MENU")
        print("1. Descargar Archivo")
        print("2. Subir archivo")
        print("3. List Count")
        print("4. Salir")
        opc = int(input())
        if opc == 1:
            t_inicio=time()
            N=10000
            for n in range(N):
                hilo=threading.Thread(name="hilo%s"%n,target=descargarArchivo)
            hilo.start()
            t_trans=time()-t_inicio
            print("El archivo fue descargado en: %.10f seg" % t_trans)
        if opc == 2:
            t_inicio = time()
            subirArchivo()
            t_trans=time()-t_inicio
            print("El archivo fue subido en: %.10f seg" % t_trans)
        if opc == 3:
            print("En la carpeta del servidor tiene ")
            os.system('ls -l /home/rublend'+ftp.pwd()+'|wc -l')
            print("archivos(s)")
        if opc == 4:
            print("FUIMONOS.")
            break
main()


