#Libreria os: Contiene condigo relacionado a el sistema operativo donde estemos trabajando
#Libreria json: Contiene condigo para manejar los archivos JSON
import os
import json
from ftplib import FTP

#Esta clase nos permite manejar todos los archivos necesarios para el funcionamiento de la aplicacion
class Archivos():

    #Escribimos el archivo JSON que contiene la informacion de las estaciones, devuelve un valor booleano al completar su ejecucion
    def guardarEstaciones(estaciones:dict)->bool:        
        try:
            with open("Conexiones/Estaciones.json","w") as jf:
                json.dump(estaciones,jf,indent=4)                        
                jf.close()
            return True
        except Exception:
            return False

    #Lee el archivo de estaciones y devuelve un diccionario con dicha informacion.
    def traerEstaciones()->dict:
        try:
            with open("Conexiones/Estaciones.json","r") as jf:
                estaciones=json.load(jf)
                jf.close()
                return estaciones
        except FileNotFoundError:return {}
    
    #Lee el archivo de definiciones_m y devuelve un diccionario con dicha informacion.
    def traerDefM()->dict:
        try:
            with open("conceptos_definiciones/definiciones_m.json","r") as jf:
                defm=json.load(jf)
                jf.close()
                return defm
        except FileNotFoundError:
            return {}

    #Lee el archivo de definiciones_st y devuelve un diccionario con dicha informacion.
    def traerDefST()->dict:
        try:
            with open("conceptos_definiciones/definiciones_st.json","r") as jf:
                defst=json.load(jf)
                jf.close()
                return defst
        except FileNotFoundError:
            return {}

    #Lee el archivo de concepto_jerarquia y devuelve un diccionario con dicha informacion.
    def traerConcepJerar()->dict:
        try:
            with open("conceptos_definiciones/concepto_jerarquia.json","r") as jf:
                conjer=json.load(jf)
                jf.close()
                return conjer
        except FileNotFoundError:
            return {}

    #Lee el archivo de concepto_jerarquia_dev y devuelve un diccionario con dicha informacion.
    def traerConcepJerarDev()->dict:
        try:
            with open("conceptos_definiciones/concepto_jerarquia_dev.json","r") as jf:
                conjerdev=json.load(jf)
                jf.close()
                return conjerdev
        except FileNotFoundError:
            return {}

    #lee el archivo de concepto_jerarquia_anulacion.json y devuelve un diciconario con dicha informacion
    def traerAnulaciones()->dict:
        try:
            with open("conceptos_definiciones/concepto_jerarquia_anulacion.json","r") as jf:
                conjerdev=json.load(jf)
                jf.close()
                return conjerdev
        except FileNotFoundError:
            return {}

    #Accede a la carpeta "consultas", luego a la subcarpeta "diaria" y luego accede a la carpeta del restaurante que se le indique para leer todos los txt que se encuentren alli, por ultimo junta toda la informacion en una sola lista y ese es el valor que retorna
    def traerConsultaDiaria(punto,ofi)->list:
        lista=[]
        ruta=f'Consultas/Diaria/{punto}-{ofi}'
        nombresArchivos=os.listdir(ruta)
        def leerArchivo(nombre)-> None:
            nonlocal ruta,lista
            archivo=os.path.join(ruta,nombre)
            with open(archivo,'r') as r:
                aux=list(map(lambda x:x.replace('\n','').split(';'),r.readlines()))
                lista+=aux
                r.close()
        try:
            if nombresArchivos:
                list(map(leerArchivo,nombresArchivos))
                return lista
            return lista
        except Exception:
            return lista

    #Accede a la carpeta "VTAS", luego accede a la carpeta del restaurante que sele indica y extrae todos los nombres de los txt que encuentre
    def traerNombreReportes(punto,ofi)->list:return os.listdir(f'VTAS/{punto}-{ofi}')

    #Escribe las consultas de todos los dias, y son dos tipos una consulta bruta que simplemente es la informacion tal cual se extraer de la DB y una consulta Diaria, que es una consulta filtrada por dia y por los tipos de datos validos
    def escribirConsulta(self,datos:list,punto:str,ofi:str,my,tipo:str)->bool:
        try:
            with open(f'Consultas/{tipo}/{punto}-{ofi}/{my}.txt','w') as wm:
                list(map(lambda x:wm.write(f'{x[0]};{x[1]};{x[2]};{x[3]};{x[4]};{x[5]};{x[6]};{x[7]};{x[8]};{x[9]};{x[10]}\n'),datos))
                wm.close()
            return True
        except FileNotFoundError:
            os.mkdir(f'Consultas/{tipo}/{punto}-{ofi}')
            return self.escribirConsulta(datos,punto,ofi,my,tipo)
        except Exception:return False

    #Escribe los reportes, que son los archivos finales que se enviaran a SAP
    def escribirReportes(self,carpeta:str,datos:list,punto:str,ofi:str,fecha:str)->bool:
        try:
            with open(f'{carpeta}/{punto}-{ofi}/VTAS{ofi}{fecha}.txt','w') as wm:
                list(map(lambda x:wm.write(f'{x[0]};{x[1]};{x[2]};{x[3]};{x[4]};{x[5]};{x[6]};{x[7]};{x[8]};{x[9]}\n'),datos))
                wm.close()
            print(f'Reporte VTAS{ofi}{fecha}.txt creado en {carpeta}')
            return True
        except FileNotFoundError:
            try:
                os.mkdir(f'{carpeta}/{punto}-{ofi}')
                return self.escribirReportes(carpeta,datos,punto,ofi,fecha)
            except FileNotFoundError:
                os.mkdir(f'{carpeta}')
                return self.escribirReportes(carpeta,datos,punto,ofi,fecha)
        except Exception:return False
    
    #Accede a la carpeta de reportes y envia al FTP el reporte que se le indique
    def enviarAFtp(self,ftp:FTP,punto:str,ofi:str,fecha:str)->bool:
        try:
            with open(f'Reportes/{punto}-{ofi}/VTAS{ofi}{fecha}.txt','rb') as reporte:
                ftp.storlines(f'STOR VTAS{ofi}{fecha}.txt',reporte)
                return True
        except FileNotFoundError:return False
        except Exception:return False

    #Lee el archivo "configuracion.json" y retorna un diccionario con dicha informacion
    def traerConfiguraciones()->dict:
        try:
            with open('configuracion.json') as jf:
                configuracion=json.load(jf)
                jf.close()
                return configuracion
        except FileNotFoundError:
            return {}
