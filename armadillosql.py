"""
Created on Mon Feb 10 10:51:34 2020
@author: leonardo.patino
"""
import io
import mysql.connector # MySQL
import psycopg2 #postgresql
import sqlalchemy
import pandas as pd
import time
#import pdb
import logging

logging.basicConfig(level = 10,  format   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt  = '%Y-%m-%d %H:%M:%S',  filename = 'log.log',  filemode = 'w')

class Armadillosql():    
    def __init__(self,cache):
        self.debug=False
        self.cache = cache
        self.log = logging.getLogger('')
        
        self.motor               = self.cache["database_motor"]
        self.database_username   = self.cache["database_username"]
        self.database_password   = self.cache["database_password"]
        self.database_ip         = self.cache["database_ip"]
        self.database_name       = self.cache["database_name"]
        self.database_port       = self.cache["database_port"]
        self.database_driver     = self.cache["database_driver"]
        self.database_options    = self.cache["database_options"]
        
    
    def engine(self):
        """ crea la conexión engine multimotor """
        if self.motor == 'mysql':
            return sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
                    format(self.cache["database_username"],
                           self.cache["database_password"], 
                           self.cache["database_ip"],
                           self.cache["database_port"],
                           self.cache["database_name"])
                    ) 
        elif self.motor == 'postgresql':
            return sqlalchemy.create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'.
                    format(self.cache["database_username"],
                           self.cache["database_password"], 
                           self.cache["database_ip"],
                           self.cache["database_name"]),
                    connect_args={'options': '-c search_path={0}'.
                                  format(self.cache["database_options"])}
                    ) 
                  
    def conection(self):
        """
        Crear cursor del motor bd
        """
        if self.motor == 'mysql':
            return mysql.connector.connect(
                      host=self.database_ip, 
                      user=self.database_username,
                      passwd=self.database_password,
                      database=self.database_name,
                      port=self.database_port,
                    )
        elif self.motor == 'postgresql':
            return psycopg2.connect(
                      host=self.database_ip,                      
                      user=self.database_username,
                      password=self.database_password,
                      database=self.database_name,
                      #options='-c search_path=' + self.database_options,
                    )  
        
    def insert_sql(self,df,name_table,metodo='replace',debug=True):  
        """ Inserta un un dataframe a la base de datos, creando la estrucura"""
        database_connection = self.engine()
        try:
            df.to_sql(con=database_connection, name=name_table, if_exists=metodo,index=False)
            if debug:
                msg = "Tabla creada en sql con el nombre:" + str(name_table) + " metodo: " + str(metodo) + " en la base de datos: " + str(self.database_name)
                self.log.info(msg)
            conn = database_connection.connect()
            conn.close()
            return 'registros Insertados'
        except Exception as e:
            msg = "Problemas para insertar en sql " + str(e)
            self.log.error(msg)
      
    def insert_sql_masivo(self,df,name_table,lote=300,metodo="replace"):
        """Inserta de forma masiva un dataframe a la base de datos, 
        , recibe parametro metodo=append para agregar, si no recibe este parametro
        por defecto creara la estructura en el primer recorrido,
        tambien recibe como parametro los lotes en el que se divide la ingesta masiva"""
        try:
            n = len(df)
            incremento = lote
            aux = 0
            v_lote = []            
            while aux < n: 
                if lote > n:
                    lote = n
                #print("de: ",aux, " hasta: ",lote, "  -  ",aux," es menor a ",n," ",aux < n)                          
                df_ = df.loc[aux:lote,]
                self.insert_sql(df_,name_table,metodo=metodo,debug=False)
                metodo = "append"                                     
                aux = lote + 1
                lote += incremento
                v_lote.append(lote)                                
            res = 'registros Insertados, ciclos: ',len(v_lote)   
            return res    
        except Exception as e:
            msg = "Problemas inserción masiva en sql " + str(e)
            self.log.error(msg)
            self.escribirLog_config("[Error] " + msg)
        
    def listar_sql(self,query,fichero=False,nombre=False):
        """Ejecuta un query y lo convierte a objeto pandas, si fichero es True entonces lo 
           guarda en la carpeta ficheros"""
        try:            
            res = self.execute(query,param='interno')            
            data = pd.DataFrame(data=res) 
            if fichero:
                if nombre == False:
                    time.ctime()
                    nombre = time.strftime('%Y%m%d%H%M%S')
                else:
                    nombre = nombre
                data.to_csv('ficheros/' + str(nombre) + '.csv', header=True, index=False)
                msg = "Archivo " + str(nombre) + " generado en la carpeta ficheros correctamente"
                self.log.info(msg)   
                self.escribirLog_config("[Info] " + msg)                 
                return "Archivo generado correctamente"
            else:
                return data
        except Exception as e:
            msg = "Problemas para listar en sql " + str(e)
            self.log.error(msg)
    
    """Pendiente hacer: Ejecuta un query y lo guarda en filePath"""
    
    def removeComment( self , text):
        """Remueve los posibles comentarios que el query enviado pudiera tener."""
        try:
            a = text.find("--")
            if a > -1:
                return text[:a]
            else:
                return text
        except Exception as e:
            msg = "Problemas con removeComment!: " + str(e)
            self.log.info(msg)
            raise
            
    def getQueries(self,path,params=None):
        """Trae los queries sin comentarios de un archivo y devuelve una lista con cada uno"""
        try:
            qs = []
            tex = ''
            with io.open (path , encoding = 'UTF-8') as fi:
                for line in fi:
                    tex += self.removeComment(line)

            spli = tex.split(";")
            for el in spli:
                if el.strip() != '':
                    # Se convierten los parámetros
                    if params is not None:
                        el = el.format(**params)
                        #print(el)
                    qs.append( el.strip() )

            if self.debug:
                msg = "Retornando {0} consultas".format(len(qs))
                self.log.info(msg)       
            return qs
        except Exception as e:
            msg = "Problemas con getQueries!: " + str(e)
            self.log.error(msg)
            raise
    
            
    def executeFile(self,filePath,params=None, devolucion=False, debug=False):
        """Ejecuta un archivo especificado en filePath si tiene devolucion entonces retorna un df 
           de lo contrario no retorna resultados"""
        i = 1
        try:
            tic = time.time()
            msg = 'Ejecutando Archivo: {0}'.format(filePath)
            self.log.info(msg)
            """
            if self.motor != 'mysql':
                self.escribirLog_config("[Info] " + msg)
            """
            #lenMsg = self.lengthMSG
            queries = self.getQueries(filePath, params)
            
            if devolucion: #ejecutar solo el último lote (sql separado por coma) y devolverlo como df 
                for q in queries:
                    if debug:
                        print(q) #solo mostrar query
                        res = 'sin resultados'
                    else:    
                        res = self.listar_sql(q)
                        
            else: #recorrer lostes separados por coma y ejecutar en el motor 1 a 1 sin devolución de resultados
                for q in queries:
                    if debug:
                        print(q) #solo mostrar query
                        res = 'sin resultados'
                    else:
                        if self.debug: #debug del contructor
                            msg = '->Ejecutando Consulta {0} del archivo'.format(i)
                            self.log.info(msg)
                        """    
                        if self.motor != 'mysql':
                            self.escribirLog_config("[Info] " + msg)    
                        """    
                        res = self.execute(q)
                        i += 1                
            toc = time.time()
            msg = 'Duración de Archivo (s): {0}'.format( int(toc-tic) )
            self.log.info(msg)
            """
            if self.motor != 'mysql':
                self.escribirLog_config("[Info] " + msg)
            """
            return res
        except Exception as e:
            msg = "Problemas con executeFile!, Query {0}, Error: {1} ".format( i , e)
            self.log.error(msg)
            if self.motor != 'mysql':
                self.escribirLog_config("[Error] " + msg)
            raise
   
        
    def execute(self,query,param=None):
        """Ejecuta una instrucción en específico, si param es 'none' sin devolución 
           de resultados de lo contrario devuelve las filas recuperadas"""  
        conection = self.conection()   
        try:
            #pdb.set_trace()            
            cur = conection.cursor()            
            cur.execute(query)                      
            if param is None:               
                return "ejecución ok"
            else:              
                res = cur.fetchall() #método, que recupera todas las filas de la última instrucción ejecutada.
                return res
        except Exception as e:            
            msg = "Problemas para ejecutar en sql " + str(e)
            #pdb.set_trace()
            self.log.error(msg)            
            return "error"
        finally:
            conection.commit()            
            cur.close()
            conection.close() 
            
    def curTime(self):
        """Devuelve la decha en formato YYYY-MM-DD HH:MM:SS."""
        time.ctime()
        return  '[' + time.strftime('%Y-%m-%d %H:%M:%S') + '] '
