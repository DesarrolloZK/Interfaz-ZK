'''
----------Estaciones---------

---------Estaciones----------
def add_ConJer(self,datos:list,oficina:int,daportare:bool)->list:
        aux,salida,aparte=deepcopy(datos),[],[]
        def apartar(conjer:dict,dat:list,apar:list,flag=True)->None:
            if dat[0]==apar[0]:
                apar[8]+=apar[8]
                apar[9]+=apar[9]
                flag=False
                return None
            if flag:aparte.append([conjer['concepto'],dat[1],dat[2],dat[3],conjer['jerarquia'],dat[5],'','','',dat[9]])

        def add(dat:list)->None:
            conjer={}
            conjer=self.buscar_conceptoJer(dat[2],daportare,dat[12])
            if conjer:
                if not conjer['aparte']:
                    dat[0]=conjer['concepto']
                    dat[2]=conjer['jerarquia']
                    salida.append([dat[0],'10','00','MST',dat[2],oficina,dat[4],dat[3],dat[5],dat[6]])
                else:
                    if aparte:list(map(lambda x: apartar(conjer,dat,x),aparte))
                    else:aparte.append([conjer['concepto'],'10','00','',conjer['jerarquia'],oficina,'','','',dat[6]])
        list(map(add,aux))
        return salida+aparte'''