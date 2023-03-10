from asyncio.windows_events import NULL
from tkinter import messagebox
import pyodbc
#Clase para controlar la conexion con la base de datos
class Conexion():
    #Metodo constructor
    def __init__(self) -> None:
        self.__serverName=None
        self.__propiedad=None
        self.__ofiVentas=None
        self.__conect=None
        
        
    #Funcion en cargada de realizar la conexion y retornar true si se establece la conexion
    #y retornar flase si no se establece dicha conexion
    def conectar(self,sName,prop,ofVen)->bool:
        self.__serverName=sName
        self.__propiedad=prop
        self.__ofiVentas=ofVen
        try:            
            self.__conect=pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
            'SERVER='+self.__serverName+
            ';DATABASE=CheckPostingDB;UID=ivkdb;PWD=Grup0IVK1*;ENCRYPT=No')            
            return True
        except Exception as e:           
            return False

    #Funcion para realizar consultas en la base de datos
    #Esta funcion  es de prueba.
    def consulta(self,sentencia)->list:
        try:
            with self.__conect.cursor() as cursor:               
                return cursor.execute(sentencia+';').fetchall()
        except Exception as e:
            messagebox.showerror(message=f'Error al consultar en la Db:\n{e}',title='Error')
            return []
            
    
    def cerrarConexion(self):
        self.__conect.close()
    
    def getServerName(self)->str:
        return self.__serverName
    
    def getPropiedad(self)->str:
        return self.__propiedad
    
    def getOfiVentas(self)->str:
        return self.__ofiVentas

if __name__=='__main__':
    prueba=Conexion()
    if prueba.conectar('181.57.147.142\\sqlexpress','1805','ppp'):
        print('Conectado')
    else:
        print('Fallo')