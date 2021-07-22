# PASO 1 IMPORTAR LIBRERIA
from armadillosql import Armadillosql
import json

# PASO 2 CREAR FUNCION PARA CONSULTAR LA CADENA DE CONEXIÓN
def get_config(bd):
	"""
	Recibe el nombre de la conexión json creada anteriormente
	"""
	try:            
		with open('conexion/' + bd +'.json') as f_in: 
			json_str = f_in.read()
			return json.loads(json_str)
	except:
		return "error"

# PASO 3 INSTANCIA DE armadillosql
try:
	sql = Armadillosql(get_config('coneccion_mysql')) 
except Exception as e:
	print("[Error] Problemas con la cadena de conexión " + str(e))


#PASO 4 DECLARAR VARIABLE CON LA UBICACIÓN DE LAS RUTINAS Y DIC CON LOS PARAMETROS
folder = 'rutinas_sql/'
params = {"variable" : 'GLOBAL'}

#PASO 5 USANDO UNO DE LOS METODOS DE LA LIBRERIA
"""
Ejecuta un archivo especificado en filePath si tiene 
devolucion entonces retorna un df de lo contrario
no retorna resultados
"""
df = sql.executeFile(folder + 'query.sql',params,devolucion=True)
print(df)


