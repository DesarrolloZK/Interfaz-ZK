'''
----------Estaciones---------
"1": {
        "punto": "716",
        "ip": "172.19.25.73",
        "daportare": false,
        "oficina":1820
    },
    "2": {
        "punto": "La Mar",
        "ip": "172.19.85.121",
        "daportare": false,
        "oficina":1855
    },
    "3": {
        "punto": "Pravda",
        "ip": "172.19.101.101",
        "daportare": false,
        "oficina":1354
    },
    "4": {
        "punto": "Watakushi 82",
        "ip": "172.19.111.17",
        "daportare": false,
        "oficina":1331
    },
    "5": {
        "punto": "Diner Unicentro",
        "ip": "172.19.61.17",
        "daportare": false,
        "oficina":1318
    },
    "6": {
        "punto": "Michelle Unicentro",
        "ip": "172.19.76.19",
        "daportare": false,
        "oficina":1335
    },
    "7": {
        "punto": "Amarti Usaquen",
        "ip": "172.19.31.17",
        "daportare": false,
        "oficina":1810
    },
    "8": {
        "punto": "Barra Unicentro",
        "ip": "172.19.120.148",
        "daportare": false,
        "oficina":1891
    },
    "9": {
        "punto": "Barra 109",
        "ip": "172.19.36.17",
        "daportare": false,
        "oficina":1870
    },
    "10": {
        "punto": "Barra 82",
        "ip": "172.19.101.91",
        "daportare": false,
        "oficina":1865
    },
    "11": {
        "punto": "Df 97",
        "ip": "172.19.95.16",
        "daportare": false,
        "oficina":3805
    },
    "12": {
        "punto": "Illy 87",
        "ip": "172.19.71.21",
        "daportare": false,
        "oficina":1325
    },
    "13": {
        "punto": "Illy Unicentro",
        "ip": "172.19.76.50",
        "daportare": false,
        "oficina":1320
    },
    "14": {
        "punto": "Wata Unicentro",
        "ip": "172.19.76.50",
        "daportare": false,
        "oficina":1355
    },
    "15": {
        "punto": "Hamakom Unicentro",
        "ip": "172.19.121.20",
        "daportare": false,
        "oficina":1399
    },
    "16": {
        "punto": "Koi",
        "ip": "172.19.25.92",
        "daportare": false,
        "oficina":1329
    },
    "17": {
        "punto": "Luna",
        "ip": "172.19.101.121",
        "daportare": false,
        "oficina":1330
    },
    "18": {
        "punto": "Michelle 82",
        "ip": "172.19.101.140",
        "daportare": false,
        "oficina":1890
    },
    "19": {
        "punto": "Pomeriggio",
        "ip": "172.19.66.17",
        "daportare": false,
        "oficina":1805
    },
    "20": {
        "punto": "Dapo 82",
        "ip": "172.19.101.139",
        "daportare": true,
        "oficina":1305
    },
    "21": {
        "punto": "Dapo Colina",
        "ip": "172.19.51.14",
        "daportare": true,
        "oficina":1395
    },
    "22": {
        "punto": "Dapo Usaquen",
        "ip": "172.19.25.140",
        "daportare": true,
        "oficina":1885
    },
    "23": {
        "punto": "Michelle Colina",
        "ip": "190.145.201.22",
        "daportare": false,
        "oficina":1398
    },
    "24": {
        "punto": "Watakushi 93",
        "ip": "190.147.30.64",
        "daportare": false,
        "oficina":1385
    },
    "25": {
        "punto": "Diner Santafe",
        "ip": "181.57.147.142",
        "daportare": false,
        "oficina":1332
    }
---------Estaciones----------
datos=Archivos.traerConcepJerar()
conceptodb=8
daportare=True
aux=next(filter(lambda x:conceptodb in x['conceptodb'] and x['daportare']==daportare,datos.values()),None)
print(aux)

    def reloj(self):
        self.__hoy=dt.now()
        h=self.__hoy.hour
        if 3<=h<=17:self.rutina()
        time.sleep(3600)
        self.reloj()

    def comprobar_Reportes(self,prop,ofi)->bool:
        lista=arc.traerNombreReportes(prop,ofi)
        for x in lista:
            if dt.strptime(x.split(f'VTAS{ofi}')[1].split('.txt')[0],'%d%M%Y').day==dt.now().day-1: return False
        return True

    def cargarConfig(self)->None:
        if len(self.__conf)!=0:
            self.__consulta=None
            self.__valIpoC=None
            self.__ipFtp=None
            self.__userFtp=None
            self.__passFtp=None
            self.__valConJer=[]
            self.__valConJerDev=[]
            self.__ctcon=ctcon()
            self.cargar_ConceptoJerarquia()
            self.cargar_ConceptoJerarquiaDev()
            self.cargar_Definiciones()
            for x in self.__conf:
                if x[0].upper()=='QUERY':self.__consulta=x[1]
                elif x[0].upper()=='IPOCONSUMO':self.__valIpoC=decimal.Decimal(x[1])/100
                elif x[0].upper()=='FTP':self.__ipFtp=x[1]
                elif x[0].upper()=='USUARIO':self.__userFtp=x[1]
                elif x[0].upper()=='PASSWORD':self.__passFtp=x[1]
                
            if (self.__consulta or self.__valIpoC or self.__ipFtp or self.__userFtp or self.__passFtp)==None: print('Es posible que el archivo de confifuraciones este incompleto')
        else:
            print('Sin configuraciones')

    def cargar_ConceptoJerarquia(self)->None:
        self.__conJer=arc.traerConcepJerar()
        for x in self.__conJer:
            if x[4]!='0': self.__valConJer.append([x[0],x[4]])
    
    def cargar_ConceptoJerarquiaDev(self)->None:
        self.__conJerDev=arc.traerConcepJerarDev()
        for y in self.__conJerDev:
            if y[4]!='0': self.__valConJerDev.append([y[0],y[4]])
    
    def cargar_Definiciones(self)->None:
        self.__definicionesM=arc.traerDefM()
        self.__definicionesMST=arc.traerDefMST()

    def buscar_ConceptoJerarquia(self,jer,tipo,c)->list:
        self.cargar_ConceptoJerarquia()
        if c==2:return None
        if str(jer)=='None':return self.buscar_ConceptoJerarquia(1,tipo,c)
        for i in self.__conJer:
            if tipo==i[6]:
                if str(jer)==i[1]:return [i[0],i[2],i[5]]
        return self.buscar_ConceptoJerarquia(jer,'',c+1)
    
    def buscar_ConceptoJerquiaDev(self,jer,tipo,c)->list:
        self.cargar_ConceptoJerarquiaDev()
        if c==2:return None
        if str(jer)=='None':return self.buscar_ConceptoJerquiaDev(1,tipo,c)
        for i in self.__conJerDev:
            if tipo==i[6]:
                if str(jer)==i[1]: return [i[0],i[2],i[5]]
        return self.buscar_ConceptoJerquiaDev(jer,'',c+1)

    def buscar_ValConcepto(self,conc)->decimal.Decimal:
        conceptos=self.__valConJer+self.__valConJerDev
        for x in conceptos:
            if x[0]==conc:
                if x[1]=='-1':return decimal.Decimal(x[1].replace('-',''))
                elif x[1]!='0': return decimal.Decimal(x[1])/decimal.Decimal('100')
        return decimal.Decimal('0.08')

    def buscar_Definiciones(self,ofi,defsq)->list:
        def buscarMST(ofi,defsq)->list:
            for c in self.__definicionesMST:                
                if ofi==c[0] and str(defsq)==c[2]:                    
                    return [c[3],c[4]]
            return ['M','']
        for c in self.__definicionesM:
            if ofi==c[0] and c[2]=='1':               
                return buscarMST(ofi,defsq)
            if ofi==c[0] and c[2]=='0':
                return ['M','']
        return ['M','']     
    
    def verificar_TipoConcepto(self,ofi)->bool:
        self.cargar_Definiciones()
        for x in self.__definicionesM:
            if ofi==x[0] and x[2]=='1': return False
        return True

    def verificar_DiaActual(self,fecha)->bool:
        return self.__hoy.day==fecha.day and fecha.hour<=3

    def verificar_DiaAnterior(self,fecha)->bool:
        return self.__hoy.day-fecha.day==1 and fecha.hour>=3

    def verificar_MesAnterior(self,fecha)->bool:
        mesAnterior=self.__hoy.month-fecha.month==1
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        cambio=self.__hoy.day<2
        return mesAnterior and ultimoDiaMes and cambio

    def verificar_AnioAnterior(self,fecha)->bool:
        anioAnterior=self.__hoy.year-fecha.year==1
        ultimoMesAnio=fecha.month==12
        ultimoDiaMes=fecha.day==mr(fecha.year,fecha.month)[1] and fecha.hour>=3
        cambio=self.__hoy.day<2
        return anioAnterior and ultimoMesAnio and ultimoDiaMes and cambio

    def del_Reportes(self)->None:
        pass

    def analizarDb(self,sName,prop,ofi,repDia)->None:   
        try:
            datos=self.__ctcon.consultar(sName,self.__consulta)
            if len(datos)!=0:
                consulDia,vtas=[],[]
                for i in datos:
                    diaValido=self.verificar_DiaActual(i[1]) or self.verificar_DiaAnterior(i[1]) or self.verificar_MesAnterior(i[1]) or self.verificar_AnioAnterior(i[1])
                    datValido=(i[7]==1 or i[7]==2) and i[5]!=None and i[6]!=None and i[10]!=None and i[11]!=None
                    if diaValido and datValido:
                        consulDia.append(i)
                        vtas.append([i[0],i[1].strftime('%d%m%Y %H:%M'),i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
                print(arc.escribirConsulta(datos,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Bruta'))
                print(arc.escribirConsulta(consulDia,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d-%m-%Y'),'Diaria'))
                if repDia:
                    vtas=self.ordenar_Informacion(vtas,ofi)                    
                    print(arc().reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y'),self.__ipFtp,self.__userFtp,self.__passFtp))
                else:
                    vtas=arc.traerConsultaDiaria(prop,ofi)
                    vtas=self.convertir_Datos(vtas)
                    vtas=self.ordenar_Informacion(vtas,ofi)
                    print(arc().reportes(vtas,prop,ofi,(self.__hoy-timedelta(days=1)).strftime('%d%m%Y'),self.__ipFtp,self.__userFtp,self.__passFtp))
            else: print('No hay datos para Crear el reporte')
        except Exception as e:
            print(f'Error en el analisis de la Db\n Descripcion: {e}')

    def ordenar_Informacion(self,vtas,ofi)->list:
        info=self.separar_Descuentos(vtas)
        prop=self.calcular_Propinas(info[0],ofi)
        vtasf=self.aplicar_Descuentos(info[0],info[1])
        vtasf=self.suma_Productos(vtasf)
        vtasf=self.arreglar_Sushis(vtasf,ofi,prop)
        vtasf=self.orden_Final(vtasf,ofi)
        vtasf=self.adicionar_ConceptoJerarquia(vtasf,ofi)
        vtasf=self.calcular_Quitar_Ico(vtasf,ofi)
        vtasf=self.eliminar_Ceros(vtasf)
        vtasf=self.adicionar_Definiciones(vtasf)
        vtasf.append(self.adicionar_IpoConsumo(ofi))
        vtasf=self.arreglar_Domicilios(vtasf)
        vtasf=self.arreglar_Propina(vtasf)
        vtasf=self.arreglar_Negativos(vtasf)
        del info,vtas
        return vtasf

    def separar_Descuentos(self,vtas)->list:
        descuentos,datos=[],[]
        for x in vtas:
            if x[7]==2:descuentos.append(x)
            elif x[7]==1 and x[3]>99999:datos.append(x)
        return [datos,descuentos]

    def calcular_Propinas(self,vtas,ofi)->list:
        check,dat,sum=[],[],0
        aux=self.buscar_ConceptoJerarquia('prop',ctcon().buscarConexion('','',ofi)[3],0)
        for c in vtas:
            if c[0] not in check:                
                check.append(c[0])
                dat.append(c)
        for c in dat:
            if c[8]!=None: sum+=c[8]
            if c[9]!=None: sum+=c[9]
        if sum==0: return[]
        return [aux[0],'10','00','',aux[1],ofi,'','','',round(sum)]

    def aplicar_Descuentos(self,dat,desc)->list:
        datos=copy.deepcopy(dat)
        for x in desc:
            aux=0
            for y in datos:
                if x[0]==y[0] and y[2]!=9:aux+=y[6]
            for y in datos:
                if x[0]==y[0] and y[2]!=9:y[6]=y[6]-(y[6]*abs(x[6]/aux))
        return datos
    
    def suma_Productos(self,vtas)->list:
        datos,ppds=[],[]
        for x in vtas:
            if x[3]!=3:
                if len(ppds)==0:
                    ppds.append(x[3])
                    datos.append(x)
                elif x[3] in ppds:
                    for y in datos:
                        if x[3]==y[3]:
                            y[5]+=x[5]
                            y[6]+=x[6]
                            break
                else:
                    ppds.append(x[3])
                    datos.append(x)
        return datos

    def arreglar_Sushis(self,vtasf,ofi,prop)->list:
        datos=[]
        if ofi=='1320':
            for x in vtasf:
                if x[2]!=8:datos.append(x)
            if len(prop)>0: return datos+[prop]
            else: return datos
        elif ofi=='1355':
            for x in vtasf:
                if x[2]==8:datos.append(x)
            return datos
        else:
            if len(prop)>0:return vtasf+[prop]
            else: return vtasf

    def orden_Final(self,vtasf,ofi)->list:
        datos=[]
        for x in vtasf:
            if x[0]==self.buscar_ConceptoJerarquia('prop',ctcon().buscarConexion('','',ofi)[3],0)[0]:datos.append(x)
            else:datos.append(['Concepto','10','00','MST',x[2],ofi,str(x[4]),x[3],x[5],x[6]])
        return datos

    def adicionar_ConceptoJerarquia(self,vtasf,ofi)->list:
        datos,aparte,prop=[],[],None
        for x in vtasf:
            if x[0]==self.buscar_ConceptoJerarquia('prop',ctcon().buscarConexion('','',ofi)[3],0)[0]:
                prop=x
                continue
            if x[8]>0 and x[9]>0:
                conjer=self.buscar_ConceptoJerarquia(x[4],ctcon().buscarConexion('','',ofi)[3],0)
                self.aux_ConceptoJerarquia(x,conjer,x[4],datos,aparte)
            elif x[8]<0 and x[9]<0:
                conjer=self.buscar_ConceptoJerquiaDev(x[4],ctcon().buscarConexion('','',ofi)[3],0)
                self.aux_ConceptoJerarquia(x,conjer,x[4],datos,aparte)
        if prop!=None:return datos+[prop]+aparte
        return datos+aparte

    def aux_ConceptoJerarquia(self,x,conjer,jer,datos,aparte,)->None:
        if conjer[0]!=None:
            if self.verificar_TipoConcepto(jer):
                if conjer[2]=='n': datos.append([conjer[0],x[1],x[2],x[3],conjer[1],x[5],x[6],x[7],x[8],x[9]])
                elif conjer[2]=='s':
                    if len(aparte)!=0:
                        bandera=True
                        for y in aparte:
                            if y[0]==conjer[0] and y[4]==conjer[2]:
                                y[8]+=x[8]
                                y[9]+=x[9]
                                bandera=False
                                break
                            if bandera:aparte.append([conjer[0],x[1],x[2],x[3],conjer[1],x[5],'','',x[8],x[9]])
                    else:aparte.append([conjer[0],x[1],x[2],x[3],conjer[1],x[5],'','',x[8],x[9]])

    def calcular_Quitar_Ico(self,vtas,ofi):
        self.__icoTotal,datos=0,[]
        for x in vtas:
            if x[0]==self.buscar_ConceptoJerarquia('prop',ctcon().buscarConexion('','',ofi)[3],0)[0]:
                datos.append(x)
                continue
            valConcepto=self.buscar_ValConcepto(x[0])
            if valConcepto==self.__valIpoC:
                x[9]=round(x[9]/(1+self.__valIpoC))
                self.__icoTotal+=x[9]*self.__valIpoC
                datos.append(x)
            elif valConcepto==1:
                x[9]=round(x[9])
                datos.append(x)
            else:
                x[9]=round(x[9]/(1+valConcepto))
                datos.append(x)
        return datos

    def eliminar_Ceros(self,vtas)->list:
        datos=[]
        for x in vtas:
            if x[8]!=0:datos.append(x)
        return datos

    def adicionar_Definiciones(self,vtasf)->list:
        for x in vtasf:
            aux=self.buscar_Definiciones(x[5],x[6])
            x[3]=aux[0]
            x[6]=aux[1]
        return vtasf

    def adicionar_IpoConsumo(self,ofi)->list:
        aux=self.buscar_ConceptoJerarquia('ico','',0)
        if len(aux)!=0: return [aux[0],'10','00','',aux[1],ofi,'','','',round(self.__icoTotal)]
        return []

    def arreglar_Domicilios(self,vtasf)->list:
        for x in vtasf:
            if x[0]=='0010':
                x[3]=''
                x[4]=''
                x[8]=''
                break
        return vtasf

    def arreglar_Propina(self,vtasf)->list:
        for x in vtasf:
            if x[0]=='0007':
                x[3]=''
                break
        return vtasf

    def arreglar_Negativos(self,vtasf)->list:
        for x in vtasf:
            if type(x[8])!=str and type(x[9])!=str:
                if x[8]<0 or x[9]<0:
                    x[8]=abs(x[8])
                    x[9]=abs(x[9])
        return vtasf

    def rutina(self)->str:
        self.__conf=arc().configuraciones()
        self.cargarConfig()
        puntos=ctcon().getConexiones()
        for i in puntos:
            if self.comprobar_Reportes(i[1],i[2]):
                print(f'Creando->{i[1]}:')
                if self.__hoy.day==1: self.analizarDb(i[0],i[1],i[2],True)
                elif self.__hoy.day<10: self.analizarDb(i[0],i[1],i[2],False)
                elif self.__hoy.day==10: self.analizarDb(i[0],i[1],i[2],False)
                elif self.__hoy.day>10: self.analizarDb(i[0],i[1],i[2],True)
                else: print('Error inesperado')
            else: print(f'{i[1]}->Reporte existente')
        return f'Rutina Terminada: {self.__hoy}'''