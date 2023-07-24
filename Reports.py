import time
from copy import deepcopy
from decimal import Decimal
from DBFTPManager import *
from Persistencia import *
from datetime import datetime
from datetime import timedelta

class ReportsManager():
    #Metodo constructor, este codigo se ejecutara apenas se genere una instancia de la clase
    def __init__(self)->None:self.__señal=self.cargar_Config()

    #Esta metodo es el punto de inicio, aqui comprobmos que el tiempo de comprobacion y el tiempo uxiliar sea minimo de 10 minutos, tambien definimos el intervalo de tiempo en el que el programa esta activo y solo funciona si las configuraciones estan cargadas.
    def iniRutina(self)->None:
        while True:
            if self.__señal:
                if self.__config['tiempoComprobacion']<600 or type(self.__config['tiempoComprobacion'])!=int:self.__config['tiempoComprobacion']=600 
                if self.__config['tiempoAuxiliar']<600 or type(self.__config['tiempoAuxiliar'])!=int:self.__config['tiempoAuxiliar']=600
                if self.__config['hora_inicio']>0 and self.__config['hora_fin']>0 and self.__config['hora_fin']>self.__config['hora_inicio']:
                    if self.__config['hora_inicio']<=self.__hoy.hour<=self.__config['hora_fin']:
                        list(map(self.analisis_DB,self.__estaciones.values()))
                        time.sleep(self.__config['tiempoComprobacion']*60)
                    time.sleep((24-(self.__config['hora_fin']-self.__config['hora_inicio']))*3600)
                else:time.sleep(self.__config['tiempoAuxiliar']*60)
            else:
                print(f"Archivos de configuracion incompletos, en {self.__config['tiempoAuxiliar']} minutos se intentara de nuevo")
                time.sleep(self.__config['tiempoAuxiliar']*60)    

    #Traemos toda la configuracion necesaria desde los archivos JSON y definimos las variables que utilizaremos, en este caso vtas como una lista vacia donde dejaremos los datos finales y hoy con la fecha actual
    def cargar_Config(self)->bool:
        self.__db=ManagerDB()
        self.__hoy=datetime.now()
        self.__auxFecha=(self.__hoy-timedelta(days=1)).strftime('%d%m%Y')
        self.__config=Archivos.traerConfiguraciones()
        self.__db.cagarConf(self.__config)
        self.__estaciones=Archivos.traerEstaciones()
        self.__concepJer=Archivos.traerConcepJerar()
        self.__concepJerDev=Archivos.traerConcepJerarDev()
        self.__concepJerAnulaciones=Archivos.traerAnulaciones()
        self.__defM=Archivos.traerDefM()
        self.__defST=Archivos.traerDefST()
        if self.__config and self.__concepJer and self.__concepJerDev and self.__defM and self.__defST and self.__estaciones and self.__concepJerAnulaciones:return True
        return False

    #Esta funcion comprueba la conexion a la DB de la estacion y la conexion a la DB de sistemas, luego trae la consulta desde la DB de la estacion y guarda la consulta en la DB de la interfaz, comprueba los dias que se necesitan para hacer los reportes
    def analisis_DB(self,estacion:dict)->None:
        print(f'{estacion["punto"]}___________________________________')
        if self.__db.conectar_DBInterfaz() and self.__db.comprobar_DBInterfaz() and self.__db.comprobar_TablaInterfaz(estacion['punto']):
            if self.__db.conectar_Estacion(estacion['ip']):
                data=self.__db.consulta_Estacion(self.__config['consulta'])
                self.__db.guardar_ConsultaDia(data,estacion['punto'],self.__hoy)
                if self.__hoy.day==1 or self.__config['dia_inicio']==None or self.__config['dia_fin']==None:
                    self.organizar_Vtas(data,estacion,False)
                elif self.__config['dia_inicio']<=self.__hoy.day<=self.__config['dia_fin']:pass
                elif self.__hoy.day==self.__config['dia_fin']+1:
                    del data
                    data=self.__db.consulta_InterfazDB(estacion['punto'])
                    self.organizar_Vtas(data,estacion,True)
                else:self.organizar_Vtas(data,estacion,False)
                self.__db.cerrarConexion()
            else:print(f"No se pudo conectar a la DB de {estacion['punto']}")
        else: print("Error en la DB de la interfaz")

    def comprobar_Reportes()->bool:
        def existe(nombre)->bool:
            nombre.f'VTAS{ofi}')[1].split('.txt')[0],'%d%M%Y'
        reportes=Archivos.traerNombreReportes()

    #Primeros filtros para que la informacion quede separada, por fecha valida, dato valido, separar los descuentos, corregir los datos None que vengan de la DB, calcular las propinas, aplicar los descuentos y sumar los valores por codigo de producto (PPD)
    def organizar_Vtas(self,data:list,estacion:dict,bandera:bool)->None:
        self.__descuentos,self.__formasPago,propinas,vtas=[],[],[],[]
        vtas=list(filter(lambda x:self.fecha_Valida(x[1],x[11],bandera),data))
        vtas=list(filter(self.datovalido_descuentos,vtas))
        vtas=list(map(self.fix_None_Convertir,vtas))
        propinas=self.calcular_Propinas(vtas,estacion)
        self.aplicar_Descuentos(vtas)
        self.marcar_NotaCredito(vtas)
        if estacion['oficina2']!=None:
            ofi1,ofi2=[],[]
            self.separar_oficinas(vtas,estacion['defAparte'],ofi1,ofi2)
            ofi1=self.add_ConJer(ofi1,estacion['oficina'],estacion['daportare'])
            ofi1=self.suma_Productos(ofi1)
            ofi2=self.add_ConJer(ofi2,estacion['oficina2'],estacion['daportare'])
            ofi2=self.suma_Productos(ofi2)
            self.mst_impo_completar(ofi1,estacion['daportare'],estacion['oficina'],estacion['punto'],propinas)
            self.mst_impo_completar(ofi2,estacion['daportare'],estacion['oficina2'],estacion['punto'],propinas)
            del vtas
        else:
            vtas=self.add_ConJer(vtas,estacion['oficina'],estacion['daportare'])
            vtas=self.suma_Productos(vtas)
            self.mst_impo_completar(vtas,estacion['daportare'],estacion['oficina'],estacion['punto'],propinas)

    #Aqui añadimos MST, calculamos los impuestos, agregamos conceptos, jerarquias y traslados (MST); tambien creamos los reportes
    def mst_impo_completar(self,datos:list,daportare:bool,oficina:int,punto:str,propinas:list)->None:
        impoTotal=self.calcular_Quitar_Ico(datos,daportare,oficina,self.__config['impoConsumo'])
        list(map(self.adicionar_DefMST,datos))
        if propinas:datos.append(propinas)
        datos.append(impoTotal)
        list(map(lambda x:self.add_Anulaciones(x),datos))
        aux=self.separar_NotasCredito(datos)
        Archivos().escribirReportes(self.__config['carpetaVtas'],aux[0],punto,oficina,self.__auxFecha)
        if aux[1]:Archivos().escribirReportes(self.__config['carpetaNotasCredito'],aux[1],punto,oficina,self.__auxFecha)

    #Filtramos la informacion que necesitamos segun la fecha, definimos un intervalo comprendido entre las 3:00 am del dia anterior hasta las 2:59am del dia actual
    def fecha_Valida(self,checkpost:datetime,checkclose:datetime,bandera:bool)->bool:
        auxfecha=deepcopy(self.__hoy)
        if checkclose!=None:
            if bandera:
                ini_intervalo=auxfecha.replace(day=self.__config['dia_inicio'],hour=3,minute=0,second=0, microsecond=0)
                fin_intervalo=auxfecha.replace(day=self.__config['dia_fin']+1,hour=3,minute=0,second=0, microsecond=0)
            else:
                ini_intervalo=auxfecha.replace(hour=3,minute=0,second=0, microsecond=0)
                ini_intervalo-=timedelta(days=1)
                fin_intervalo=auxfecha.replace(hour=3,minute=0,second=0,microsecond=0)
            return ini_intervalo<=checkpost<fin_intervalo
        return False

    #Filtramos los datos que necesitamos (verifica si el campo 5 es mayor a 0 y diferete de Nulo, verifica si los campos 10 y 11 son distintos de None), el campo 7 indica si es un dato normal o es un descuento (2: descuento, 1: dato normal), y aqui mismo separamos los descuentos del resto de datos
    def datovalido_descuentos(self,datos:list)->bool:
        flag=datos[2]!=7 and datos[5]!=0 and datos[5]!=None and datos[10]!=None
        if datos[7]==1 and datos[3]>99999 and flag:return True
        elif datos[7]==2 and flag:self.__descuentos.append(datos)
        elif datos[7]==4:self.__formasPago.append(datos)
        return False

    #Si el dato del campo 6 es None se reemplazara su valor con 0 y transformamos cada fila proveniente de la base de datos a una lista
    def fix_None_Convertir(self,dat:list)->list:
        if dat[6]==None:dat[6]=0
        aux=list(dat)
        aux.append(False)
        return aux
    
    #Se verifica gracias al detailtype 4, si un cheque es una factura normal o una nota credito y en base a eso marcamos cada producto con True o False para posteriormente asignarle un concepto normal o de devolucion
    def marcar_NotaCredito(self,datos:list)->None:
        def marcar(forma:list,dat:list)-> None:
            if forma[0]==dat[0] and forma[6]<0:dat[12]=True
        aux=lambda x:list(map(lambda y:marcar(x,y),datos))
        list(map(aux,self.__formasPago))

    #Busca los conceptos y jerarquias, segun el codigo que viene de la DB y verificamos si es una devolucion (si la cantidad o el precio es negativo)
    def buscar_conceptoJer(self,concepto,daportare:bool,devolucion:bool)->dict:
        if not devolucion:
            r=next(filter(lambda x: concepto in x['conceptodb'] and daportare==x['daportare'],self.__concepJer.values()),{})
            if not r:next(filter(lambda x: None in x['conceptodb'] and daportare==x['daportare'],self.__concepJer.values()),{})
        elif devolucion:
            r=next(filter(lambda x: concepto in x['conceptodb'] and daportare==x['daportare'],self.__concepJerDev.values()),{})
            if not r:next(filter(lambda x: None in x['conceptodb'] and daportare==x['daportare'],self.__concepJerDev.values()),{})
        return r

    #Busca por concepto (ejemplo: "0010") el valor que se le asocia para calcular los impuestos
    def valor_conceptoJer(self,concepto:str,jerarquia:str)->float or None:
        if self.__concepJer and self.__concepJerDev:
            val=next(filter(lambda x: x['concepto']==concepto and x['jerarquia']==jerarquia,self.__concepJer.values()),None)
            if val==None:val=next(filter(lambda x: x['concepto']==concepto and x['jerarquia']==jerarquia,self.__concepJerDev.values()),None)
            if val!=None:return val['impuesto']
        return None

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
    def aplicar_Descuentos(self,datos:list)->None:
        def aplicar(desc:list,dat:list,suma)->None:
            if desc[0]==dat[0] and dat[2]!=9:dat[6]=dat[6]-(dat[6]*abs(desc[6]/suma))

        def verificar_chks(descuento:list)->list:
            suma=0
            values=list(map(lambda x: x[6] if descuento[0]==x[0] and x[2]!=0 else 0,datos))
            suma=sum(values)
            if suma!=0: list(map(lambda x:aplicar(descuento,x,suma),datos))

        if self.__descuentos:list(map(verificar_chks,self.__descuentos))
    
    #Se buscan los conceptos y jerarquias asociado a cada dato y se de vuelven los datos en el orden requerido para SAP (concepto, sector,canal, MST, jerarquia, voficina de venta, oficina que produce, PPD, cantidad, valor)
    def add_ConJer(self,datos:list,oficina:str,daportare:bool)->list:
        aux,salida,aparte,flag=deepcopy(datos),[],[],False
        def unaLinea(apar:list,conjer:dict,dat:list)->None:
            nonlocal flag
            if apar[0]==conjer['concepto'] and apar[4]==conjer['jerarquia']:
                apar[9]+=dat[6]
                flag+=True
        def recorrer(dat:list)->None:
            nonlocal flag,aparte
            conjer=self.buscar_conceptoJer(dat[2],daportare,dat[12])
            if conjer:
                if conjer['aparte']:
                    if not aparte:
                        aparte.append([conjer['concepto'],self.__config['canal'],self.__config['sector'],'',conjer['jerarquia'],oficina,'','','',dat[6]])
                    else:
                        list(map(lambda x: unaLinea(x,conjer,dat),aparte))
                        if not bool(flag):aparte.append([conjer['concepto'],self.__config['canal'],self.__config['sector'],'',conjer['jerarquia'],oficina,'','','',dat[6]])
                else:
                    salida.append([conjer['concepto'],self.__config['canal'],self.__config['sector'],'MST',conjer['jerarquia'],oficina,dat[4],dat[3],dat[5],dat[6]])
            else:
                salida.append([dat[0],self.__config['canal'],self.__config['sector'],'MST',f'Sin concepto: {dat[2]}',oficina,dat[4],dat[3],dat[5],dat[6]])
        list(map(recorrer,aux))
        return salida+aparte

    #Sumamos cantidades y valores segun el concepto, jerarquia, oficina que produce y PPD
    def suma_Productos(self,datos:list)->list:
        ppds,values=[],[]
        def sumando_ppds(value:list,dat:list)->None:
            bandera=value[0]==dat[0] and value[4]==dat[4] and value[6]==dat[6] and value[7]==dat[7]
            if bandera:
                value[8]+=dat[8]
                value[9]+=dat[9]

        def agrupar_ppds(dat:list)->None:
            nonlocal ppds,values
            aux=[dat[0],dat[4],dat[6],dat[7]]
            if not ppds or aux not in ppds:
                ppds.append(aux)
                values.append(dat)
            else:
                list(map(lambda x:sumando_ppds(x,dat),values))
        list(map(agrupar_ppds,datos))
        return values

    #Verificamos si el punto consta de una segunda oficina de venta y separamos dichos datos en otra lista.
    def separar_oficinas(self,datos:list,definicion:int,ofi1:list,ofi2:list)->None:
        def separar(dat:list)->None:
            if dat[2]==definicion:ofi2.append(dat)
            else:ofi1.append(dat)
        list(map(separar,datos))

    #Calculamos los impuestos y los quitamos de los productos para dejarlos en una linea aparte.
    def calcular_Quitar_Ico(self,datos:list,daportare:bool,oficina:int,impoConsumo:float)->list:
        aux=0
        def calcular(dat:list)->None:
            nonlocal aux
            valor=self.valor_conceptoJer(dat[0],dat[4])
            if valor!=None:
                dat[9]=round(dat[9]/Decimal(1+valor))
                if impoConsumo==valor:aux+=dat[9]*Decimal(valor)
            else:dat[9]=round(dat[9])
        list(map(calcular,datos))
        conjer=self.buscar_conceptoJer('impConsumo',daportare,False)
        impuesto=[conjer['concepto'],self.__config['canal'],self.__config['sector'],'',conjer['jerarquia'],oficina,'','','',round(aux)]
        return impuesto
    
    #En base a ladefiniciones (1,2,3,4,5,18,20.....etc), asignamos las M, S o T y añadimos la oficina de venta que produce el producto
    def adicionar_DefMST(self,dat:list)->None:
        if dat[5] in self.__defM['traslados'] and dat[5] not in self.__defM['noTraslados']:
            if dat[6] in self.__defST['porDefecto']['produce']:
                aux=self.__defST['porDefecto'][str(dat[6])]
                dat[3]=aux[1]
                dat[6]=aux[0]
            elif dat[6] in self.__defST[str(dat[5])]['produce']:
                aux=self.__defST[str(dat[5])][str(dat[6])]
                dat[3]=aux[1]
                dat[6]=aux[0]
            else:dat[6]=f"No_def ->{dat[6]}<- "
        elif dat[5] not in self.__defM['traslados'] and dat[5] in self.__defM['noTraslados']:
            aux=self.__defM['definicion']
            dat[3]=aux[1]
            dat[6]=aux[0]
        else:dat[6]=f"No_def ->{dat[6]}<-"

    #Verifica si alguno de los totales es negativo y verifica si es una anulacion para añadirle el concepto correspondiente
    def add_Anulaciones(self,dato:list)->None:
        if dato[9]<0:
            r=next(filter(lambda x: dato[0] in x['conceptodb'] and dato[4] in x['conceptodb'],self.__concepJerAnulaciones.values()),{})
            if r:dato[0]=r['concepto']
        if type(dato[8])!=str:dato[8]=abs(dato[8])
        if type(dato[9])!=str:dato[9]=abs(dato[9])

    #Separa las notas credito
    def separar_NotasCredito(self,datos:list)->list:
        vtas,notas=[],[]
        def validar(dato:list,aux:dict)->None:
            val=next(filter(lambda x: x['concepto']==dato[0] and x['jerarquia']==dato[4],self.__concepJerDev.values()),None)
            if val!=None:notas.append(dato)
            else:vtas.append(dato)
        list(map(lambda x:validar(x,self.__concepJer),datos))
        return (vtas,notas)

if __name__=='__main__':ReportsManager().iniRutina()
