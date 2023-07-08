#Libreria pyodbc: Contiene todo el codigo necesario para manejar la base de datos
#Libreria ftplib: Contiene todo el codigo necesario para manejar la conexion al servidor FTP
import pyodbc
from copy import deepcopy
from ftplib import FTP 
from ftplib import error_perm
from Persistencia import Archivos

#Clase para establecer la conexion con la base de datos
class ManagerDB():
            
    def cagarConf(self,configuraciones:Archivos)->None:self.__configuraciones=configuraciones

    def crear_DBlocal()->bool:
        pass

    #Funcion en cargada de realizar la conexion y retornar true si se establece la conexion
    #y retornar flase si no se establece dicha conexion
    def conectar_Estacion(self,ipcaps)->bool:
        try:
            if self.__configuraciones:
                self.__conect=pyodbc.connect(f'DRIVER={self.__configuraciones["DriverDB"]};'+
                                             f'SERVER={ipcaps}{self.__configuraciones["ServerDB"]};'+
                                             f'DATABASE={self.__configuraciones["DATABASE"]};'+
                                             f'UID={self.__configuraciones["UID"]};'+
                                             f'PWD={self.__configuraciones["PWD"]};'+
                                             f'ENCRYPT={self.__configuraciones["ENCRYPT"]}')
                return True
            else:return False
        except Exception:return False
 
    #Funcion para realizar consultas en la base de datos
    #Esta funcion  es de prueba.
    def consulta(self,query:str)->list:
        try:
            with self.__conect.cursor() as cursor:
                cursor.execute(query+';')
                aux=cursor.fetchall()
            consulta=deepcopy(aux)
            self.__conect.close()
            return consulta
        except Exception: return []

    def cerrarConexion(self):self.__conect.close()

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
