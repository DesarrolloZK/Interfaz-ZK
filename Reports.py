from copy import deepcopy
import time
import decimal
from DBFTPManager import *
from Persistencia import *
from Persistencia import *
from datetime import datetime
from datetime import timedelta
from functools import reduce


class ReportsManager():
    #Metodo constructor, este codigo se ejecutara apenas se genere una instancia de la clase
    def __init__(self)->None:
        self.cargar_Config()

    def iniRutina(self,tiempo:int)->None:
        while True:
            if self.cargar_Config():
                list(map(self.analisis_DB,self.__estaciones.values()))
                time.sleep(tiempo)
            else:
                print(f"Archivos de configuracion incompletos en {tiempo/4/60} minutos se intentara de nuevo")
                time.sleep(tiempo/4)        

    #Traemos toda la condifuracion necesaria desde los archivos JSON y definimos las variables que utilizaremos, en este caso vtas como una lista vacia donde dejaremos los datos finales y hoy con la fecha actual
    def cargar_Config(self)->bool:
        self.__vtas=[]
        self.__db=ConexionDB()
        self.__hoy=datetime.now()
        self.__config=Archivos.configuraciones()
        self.__db.cagarConf(self.__config)
        self.__estaciones=Archivos.traerEstaciones()
        self.__concepJer=Archivos.traerConcepJerar()
        self.__concepJerDev=Archivos.traerConcepJerarDev()
        self.__defM=Archivos.traerDefM()
        self.__defST=Archivos.traerDefST()
        if self.__config and self.__concepJer and self.__concepJerDev and self.__defM and self.__defST and self.__estaciones:return True
        return False

    #Traemos la consulta desde la DB de la estacion y verificamos si es correcta la conexion
    def analisis_DB(self,estacion:dict)->None:
        if self.__db.conectar(estacion['ip']):
            data=self.__db.consulta(self.__config['consulta'])
            self.orden_Vtas(data,estacion,1)
        else:print(f"No se pudo conectar a la DB de {estacion['punto']}")

    #Realizamos todas las operaciones para constuir el archivos y dejarlo con su orden final
    def orden_Vtas(self,data:list,estacion:dict,dias:int)->None:
        print(f'------------------>{estacion["punto"]}<--------------------------')
        self.__descuentos,vtas=[],[]
        vtas=list(filter(lambda x:self.fecha_Valida(x[1],x[11],dias),data))
        vtas=list(filter(self.datovalido_descuentos,deepcopy(vtas)))
        vtas=list(map(self.fix_None,deepcopy(vtas)))
        print(len(vtas))
        propinas=self.calcular_Propinas(deepcopy(vtas),estacion)
        vtas=self.aplicar_Descuentos(deepcopy(vtas))
        print(len(vtas))
        '''vtas=self.suma_Productos(deepcopy(vtas))
        for x in vtas:
            print(x[3])'''
        
        

    #Filtramos la informacion que necesitamos segun la fecha
    def fecha_Valida(self,checkpost:datetime,checkclose:datetime,dias:int)->bool:
        if checkclose!=None:
            auxfecha=deepcopy(self.__hoy)
            ini_intervalo=auxfecha.replace(hour=3,minute=0,second=0, microsecond=0)
            ini_intervalo-=timedelta(days=dias)
            fin_intervalo=auxfecha.replace(hour=3,minute=0,second=0,microsecond=0)
            if dias==1:return ini_intervalo<=checkpost<fin_intervalo
            elif 1<dias<5:
                fin_intervalo=fin_intervalo-timedelta(days=(dias-1))
                return ini_intervalo<=checkpost<fin_intervalo
            return False
        return False

    #Filtramos los datos que necesitamos (verifica si el campo 5 es mayor a 0 y diferete de Nulo, verifica si los campos 10 y 11 son distintos de None), el campo 7 indica si es un dato normal o es un descuento (2: descuento, 1: dato normal), y aqui mismo separamos los descuentos del resto de datos
    def datovalido_descuentos(self,datos:list)->bool:
        flag=datos[5]!=0 and datos[5]!=None and datos[10]!=None
        if datos[7]==2 and flag:
            self.__descuentos.append(datos)
            return False
        elif datos[7]==1 and datos[3]>99999 and flag:
            return True
        return False

    #Si el dato del capo 6 es None se reemplazara su valor con 0
    def fix_None(self,datos:list)->list:
        if datos[6]==None:datos[6]=0
        return datos
    
    #Busca los conceptos y jerarquias y pregunta si es una devolucion o no
    def buscar_conceptoJer(self,concepto,daportare:bool,devolucion:bool)->dict:
        if not devolucion:
            r=next(filter(lambda x: concepto in x['conceptodb'] and daportare==x['daportare'],self.__concepJer.values()),{})
            return r
        else:
            r=next(filter(lambda x: concepto in x['conceptodb'] and daportare==x['daportare'],self.__concepJerDev.values()),{})
            return r

    #Se caculan las propinas, por chk y se le agrega  concepto y jerarquia.
    def calcular_Propinas(self,datos:list,estacion:dict)->list:
        conJer=self.buscar_conceptoJer('prop',False,False)
        chks,propSugerida,propVoluntaria=[],0,0
        def verificar(dat)->None:
            nonlocal chks,propSugerida,propVoluntaria
            if dat[0] not in chks:
                chks.append(dat[0])
                if dat[8]!=None:propSugerida+=dat[8]
                if dat[9]!=None:propVoluntaria+=dat[9]
        if conJer:
            list(map(verificar,datos))
            suma=propSugerida+propVoluntaria
            if suma>0: return[conJer['concepto'],self.__config['canal'],self.__config['sector'],'',conJer['jerarquia'],estacion['oficina'],'','','',round(suma)]
            return []
        return []

    #Aplicamos los descuentos por chk
    def aplicar_Descuentos(self,datos:list,valores=[],suma=0)->list:
        aplicado=[]
        def sumando_chk(dato:list,desc:list,suma:list):
            nonlocal aplicado
            if dato not in aplicado:
                if dato[0]==desc[0] and dato[2]!=9:
                    dato[6]=dato[6]-(dato[6]*abs(desc[6]/suma))
                aplicado.append(dato)

        def separar_chks(descuento:list)->list:
            nonlocal aplicado
            values=list(filter(None,map(lambda x: x[6] if descuento[0]==x[0] and x[2]!=0 else None,datos)))
            suma=sum(values)
            pass
        return datos

    #Sumamos por producto (PPD)
    def suma_Productos(self,datos:list)->list:
        salida,ppds,values=[],[],
        def sumando_ppds():
            nonlocal salida
            pass

        def agrupar_ppds(dato:list)->None:
            nonlocal ppds,values
            if not ppds or dato[3] not in ppds:
                ppds.append(dato[3])
                values.append(dato)

        list(map(agrupar_ppds,datos))
        return list(map(sumando_ppds,values))
        


if __name__=='__main__':
    prueba=ReportsManager()
    prueba.iniRutina(3600)
