from tkinter import messagebox
from ftplib import FTP
import os
class Archivos():

    def guardarArchivo(con)->bool:        
        try:
            with open("Conexiones/Conexiones.txt","w") as wm:                
                for i in con:
                    wm.write(f'{i[0]},{i[1]},{i[2]}{os.linesep}')                                 
                wm.close()
            return True
        except Exception as e:
            print(f"Error de escritura:\n{e}")
            return False

    def traerConexiones()->list:
        lista=list()
        try:
            with open("Conexiones/Conexiones.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(','))
                r.close()
            return lista
            
        except FileNotFoundError as fnf:
            print(fnf)     
            return []
    
    def traerDefM()->list:
        lista=list()
        try:
            with open("Tablas/DefinicionM.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(';'))
                r.close()
            return lista
        except FileNotFoundError as fnf:
            print(fnf)
            return []

    def traerDefMST()->list:
        lista=list()
        try:
            with open("Tablas/DefinicionMST.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(';'))
                r.close()
            return lista
        except FileNotFoundError as fnf:
            print(fnf)
            return []

    def traerConcepJerar()->list:
        lista=list()
        try:
            with open("Tablas/ConcJerar.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(';'))
                r.close()
                return lista
        except FileNotFoundError as fnf:
            print(f'No se encuentra archivo: {fnf}')
            return []

    def traerConcepJerarDev()->list:
        lista=list()
        try:
            with open("Tablas/ConcJerarDev.txt","r") as r:
                datos=r.readlines()
                for i in range(len(datos)):
                    lista.append(datos[i].replace('\n','').split(';'))
                r.close()
                return lista
        except FileNotFoundError as fnf:
            print(f'No se encuentra archivo: {fnf}')
            return []

    def traerConsultaDiaria(propiedad,ofi)->list:
        ruta=f'Consultas/Diaria/{propiedad}-{ofi}'
        lista=[]
        try:
            for nomArchivo in os.listdir(ruta):
                f=os.path.join(ruta,nomArchivo)
                aux=[]
                with open(f,'r') as r:
                    datos=r.readlines()
                    for i in range(len(datos)):
                        aux.append(datos[i].replace('\n','').split(';'))
                    r.close()
                    lista+=aux
            return lista
        except Exception as e:
            print(f'Error al traer consulta filtrada ({e})')

    def traerNombreReportes(propiedad,ofi)->list:
            ruta=f'Reportes/{propiedad}-{ofi}'
            lista=[]
            try:
                for nomArchivo in os.listdir(ruta):
                    lista.append(nomArchivo)
                return lista
            except Exception as e:
                print(f'Error al traer reportes ({e})')

    def escribirConsulta(datos,propiedad,ofi,my,tipo)->str:
        def diario():
            with open(f'Consultas/{tipo}/{propiedad}-{ofi}/{my}.txt','w') as wm:
                    for i in datos:                                               
                        wm.write(f'{i[0]};{i[1]};{i[2]};{i[3]};{i[4]};{i[5]};{i[6]};{i[7]};{i[8]};{i[9]};{i[10]}\n')
                    wm.close()
            return f'Consulta {tipo} Guardada'
        try:
            os.mkdir(f'Consultas/{tipo}/{propiedad}-{ofi}')
            return diario()
        except FileExistsError as fee:
            try:
                return diario()
            except Exception as e:
                return f'Error al escribir archivo: {e}'
        except FileNotFoundError as fne:
            return f'Error: {fne}'

    def reportes(self,datos,propiedad,ofi,fecha,ip,user,password)->str:
        def crear():
            with open(f'Reportes/{propiedad}-{ofi}/VTAS{ofi}{fecha}.txt','w') as wm:
                for i in datos:
                    wm.write(f'{i[0]};{i[1]};{i[2]};{i[3]};{i[4]};{i[5]};{i[6]};{i[7]};{i[8]};{i[9]}\n')
                wm.close()
                return f'Estado: Reporte {fecha} Creado | Ftp: {self.enviar_a_Ftp(propiedad,ofi,fecha,ip,user,password)}' 
        try:
            os.mkdir(f'Reportes/{propiedad}-{ofi}')
            return crear()
        except FileExistsError as fee:
            try:
                return crear()
            except Exception as e:
                return f'Error al escribir archivo reporte {str(e)}'
        except FileNotFoundError as fne:
            return f'Error: {fne}'
    
    def enviar_a_Ftp(self,propiedad,ofi,fecha,ip,user,password)->str:
        try:
            with FTP(ip,user,password) as ftp:
                with open(f'Reportes/{propiedad}-{ofi}/VTAS{ofi}{fecha}.txt','rb') as reporte:
                    ftp.storlines(f'STOR VTAS{ofi}{fecha}.txt',reporte)
                    return 'Reporte enviado a ftp correctamente'
        except FileNotFoundError as fnf:
            return 'Reporte no se pudo enviar porque no se ha encontrado'
        except FileExistsError as fee:
            return 'Reporte ya existe en servidor ftp'
        except Exception as e:
            return f'Posiblemente no se pudo establecer conexion con el servidor ftp\nDescripcion: {e}'

    def configuraciones(self)->list:
        conf=[]
        try:
            with open('Config.txt','r') as r:
                datos=r.readlines()
                for i in datos:
                    conf.append(i.replace('\n','').split(':'))
                r.close()
                return conf
        except FileNotFoundError as fnf:
            messagebox.showerror(message="Archivo de configuraciones no encontrado se creara en la raiz del programa",title="Error Grave")
            return self.configuraciones()
