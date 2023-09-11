#Libreria pyodbc: Contiene todo el codigo necesario para manejar la base de datos
#Libreria ftplib: Contiene todo el codigo necesario para manejar la conexion al servidor FTP
import pyodbc
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from ftplib import FTP 
from ftplib import error_perm

#Clase para establecer la conexion con la base de datos
class ManagerDB():
    
    #Traemos las configuraciones
    def cagarConf(self,configuraciones:dict)->None:self.__configuraciones=configuraciones

    #Realizamos la conexion a la base de datos de la interfaz
    def conectar_DBInterfaz(self)->bool:
        try:
            if self.__configuraciones:
                self.__conectInterfaz=pyodbc.connect(f'DRIVER={self.__configuraciones["DriverDB"]};'+
                                             f'SERVER={self.__configuraciones["SistemasInstanciaDB"]};'+
                                             f'UID={self.__configuraciones["SistemasUID"]};'+
                                             f'PWD={self.__configuraciones["SistemasPWD"]};'+
                                             f'ENCRYPT={self.__configuraciones["SistemasENCRYPT"]}',
                                             autocommit=True)
                return True
            else:return False
        except Exception:return False

    #Verificamos si esta creada la base de datos de la interfaz, si no es asi la creamos
    def comprobar_DBInterfaz(self)->bool:
        try:
            cursor=self.__conectInterfaz.cursor()
            db=self.__configuraciones["InterfazDB"]
            cursor.execute(f"SELECT COUNT(*) FROM sys.databases WHERE name='{db}';")
            r=cursor.fetchone()
            if r[0]>0:return True
            else:
                cursor.execute(f'CREATE DATABASE {self.__configuraciones["InterfazDB"]};')
                return True
        except Exception: return False

    #Verificamos si existe las tablas de la interfaz, si no las creamos
    def comprobar_TablaInterfaz(self,punto:str)->bool:
        try:
            cursor=self.__conectInterfaz.cursor()
            db=self.__configuraciones['InterfazDB']
            tabla=punto.replace(' ','')
            cursor.execute(f'use {db};')
            cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME ='{tabla}'")
            r1=cursor.fetchone()
            cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME ='{tabla}Fechas'")
            r2=cursor.fetchone()
            if not r1[0]>0:cursor.execute(self.__configuraciones['crearTabla'].replace("nombre",tabla))
            if not r2[0]>0:cursor.execute(f'CREATE TABLE {tabla}Fechas(fecha date not null);')
            return True
        except Exception:return False

    #Guardamos la consulta tal cual la traemos de las estaciones y guardamos las fechas
    def guardar_ConsultaDia(self,datos,punto:str,hoy:datetime)->None:
        def preparar_Dato(dato:list)->tuple:
            nonlocal fechasDB,fechas
            if self.aux_consultaDia(dato[1],hoy,fechasDB,fechas):return tuple(dato)
        try:
            fechas=[]
            tabla=punto.replace(" ","")
            query=f'insert into {tabla}(numcheque,fechaPosteo,tipoProducto,codProducto,ofiProduce,cantidad,total,tipoDato,propinaObligatoria,propinaVoluntaria,subTotal,fechaPago) values(?,?,?,?,?,?,?,?,?,?,?,?);'
            cursor=self.__conectInterfaz.cursor()
            db=self.__configuraciones['InterfazDB']
            cursor.execute(f'use {db};')
            fechasDB=list(cursor.execute(f'select * from {tabla}Fechas;').fetchall())
            fechasDB=list(map(lambda x:tuple(x),fechasDB))
            aux=list(map(preparar_Dato,datos))
            aux=list(filter(lambda x: x is not None,aux))
            if aux and fechas:
                cursor.executemany(query,aux)
                cursor.executemany(f'insert into {tabla}Fechas(fecha) values(?);',fechas)
                cursor.commit()
                list(map(lambda x:print(f'Informacion guardada de: {x[0]}'),fechas))
        except Exception as exc:print(f"Error al guardar informacion: {exc}")

    #Es una funcion auxiliar que verifica si un dato esta en el rango de fecha correcto, para guardarlos en la base de datos
    def aux_consultaDia(self,dato:datetime,hoy:datetime,fechasDb:list,fechas:list)->bool:
        auxHoy=hoy.replace(hour=3,minute=0,second=0,microsecond=0)
        ini=dato.replace(hour=3,minute=0,second=0,microsecond=0)
        fin=ini+timedelta(days=1)
        if tuple([dato.date()]) not in fechasDb:
            if tuple([dato.date()]) not in fechas and dato.date()!=hoy.date():fechas.append(tuple([dato.date()]))
            if dato.date()==hoy.date() and dato>auxHoy:return False
            if dato<ini or dato>=fin:return False
            return True
        return False

    #Traemos la informacion de la base de datos de la interfaz.
    def consulta_InterfazDB(self,punto:str)->list:
        try:
            with self.__conectInterfaz.cursor() as cursor:
                db=self.__configuraciones['InterfazDB']
                tabla=punto.replace(' ','')
                cursor.execute(f'use {db};')
                cursor.execute(f'SELECT * FROM {tabla};')
                aux=cursor.fetchall()
            consulta=deepcopy(aux)
            return consulta
        except Exception as exc:
            print(exc)
            return []

    #Funcion encargada de realizar la conexion a cada estacion y retornar true si se establece la conexion o retornar false si no se establece dicha conexion
    def conectar_Estacion(self,ipcaps)->bool:
        try:
            if self.__configuraciones:
                self.__conect=pyodbc.connect(f'DRIVER={self.__configuraciones["DriverDB"]};'+
                                             f'SERVER={ipcaps}{self.__configuraciones["InstanciaDB"]};'+
                                             f'DATABASE={self.__configuraciones["DATABASE"]};'+
                                             f'UID={self.__configuraciones["UID"]};'+
                                             f'PWD={self.__configuraciones["PWD"]};'+
                                             f'ENCRYPT={self.__configuraciones["ENCRYPT"]}')
                return True
            else:return False
        except Exception:return False

    #Funcion para realizar consultas en la base de datos
    def consulta_Estacion(self,query:str)->list:
        try:
            with self.__conect.cursor() as cursor:
                cursor.execute(query+';')
                aux=cursor.fetchall()
            consulta=deepcopy(aux)
            return consulta
        except Exception: return []

    def cerrarConexion(self):
        self.__conect.close()
        self.__conectInterfaz.close()

#Clase para establecer la conexion con el servidor FTP
class ConexionFTP():
    #Instanciamos la clase FTP (Este es el metodo constructor)
    def __init__(self) -> None:
        self.__ftp=FTP()

    #Establecemos la conexion y manejamos los posibles errores cuando se realice dicha conexion
    def conn(self,ip,user,password,carpeta)->int:
        try:
            self.__ftp.connect(ip)
            self.__ftp.login(user=user,passwd=password)
            self.__ftp.cwd(carpeta)
            if carpeta not in self.__ftp.nlst():self.__ftp.mkd(carpeta)
            return 0
        except TimeoutError:return 1
        except error_perm as e:
            if str(e).split()[0]=='530':return 2
            elif str(e).split()[0]=='550':return 3
            else:return 4
    
    #Devolvemos el objeto que contiene la conexion con el FTP para manejarlo en otra clase
    def getconn(self)->FTP:return self.__ftp

    #Cerramos la conexion con el FTP
    def closeconn(self)->None:self.__ftp.quit()
