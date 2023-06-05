import copy
import time
import decimal
from DBFTPManager import *
from Persistencia import *
from calendar import monthrange as mr
from Persistencia import *
from datetime import datetime
from datetime import timedelta


class ReportsManager():
    #Metodo constructor, este codigo se ejecutara apenas se genere una instancia de la clase
    def __init__(self)->None:
        self.cargar_Config()

    def rutina_Reloj(self,seg:int)->None:
        while True:
            if self.cargar_Config():
                list(map(self.analisis_DB,self.__estaciones))
                time.sleep(seg)
            else:
                print(f"Archivos de configuracion incompletos en {seg/4/60} minutos se intentara de nuevo")
                time.sleep(seg/4)        

    #Traemos toda la condifuracion necesaria desde los archivos JSON y definimos las variables que utilizaremos, en este cso vtas como una lista vacia donde dejaremos los datos finales y hoy con la fecha actual
    def cargar_Config(self)->bool:
        self.__vtas=[]
        self.__hoy=datetime.now()
        self.__config=Archivos.configuraciones()
        self.__estaciones=Archivos.traerEstaciones()
        self.__concepJer=Archivos.traerConcepJerar()
        self.__conepJerDev=Archivos.traerConcepJerarDev()
        self.__defM=Archivos.traerDefM()
        self.__defST=Archivos.traerDefST()
        if self.__config and self.__concepJer and self.__conepJerDev and self.__defM and self.__defST and self.__estaciones:return True
        return False

    def analisis_DB(self,estacion:dict)->None:
        conn=ConexionDB()
        if conn.conectar(estacion['ip']):
            data=conn.consulta(self.__config['consulta'])
            self.orden_Vtas(data,estacion)
        print(f"No se pudo conectar a la DB de {estacion['punto']}")

    def orden_Vtas(self,data:list,estacion:dict)->None:
        pass

    def fechaValida(self,fecha:datetime,dias:int)->bool:
        auxfecha=deepcopy(self.__hoy)
        if dias==1:
            ini_intervalo=auxfecha-timedelta(days=dias)
            ini_intervalo.replace(hour=3,minute=0,second=0, microsecond=0)
            fin_intervalo=auxfecha.replace(hour=2,minute=59,second=59,microsecond=0)
            return ini_intervalo<=fecha<=fin_intervalo
        elif 1<dias<5:
            ini_intervalo=auxfecha-timedelta(days=dias)
            ini_intervalo.replace(hour=3,minute=0,second=0, microsecond=0)
            fin_intervalo=auxfecha.replace(hour=2,minute=59,second=59,microsecond=0)
            fin_intervalo=fin_intervalo-timedelta(days=(dias-1))
            return ini_intervalo<=fecha.hour<=fin_intervalo

'''def buscar_conceptoJer(self,concepdb:int,daportare:bool)->dict:
    if self.__concepJer:
        filter(lambda)
    return {}'''

if __name__=='__main__':
    prueba=ReportsManager()