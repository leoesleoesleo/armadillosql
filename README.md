<p align="center">
  <a href="https://leoesleoesleo.github.io/pagina_armadillo/"><img src="https://leoesleoesleo.github.io/pagina_armadillo/img/logo.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>ArmadilloSQL es una libreria para conectarnos a diferentes motores de bases de datos relacionales y hacer operaciones como ingestas masivas, ejecutar un archivo sql externo, crear diferentes cursores para diferentes motores de bases de datos.</em>
</p>

</p>
<p align="center">
<a href="#" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
</p>

Documentación: https://leoesleoesleo.github.io/pagina_armadillo/

Código: https://github.com/leoesleoesleo/armadillosql

Armadillosql es una solución rápida para manipular datos en diferentes motores de base de datos relacionales, de momento funciona con mysql y postgresql, en las próximas versiones tendremos Oracle, SQL server, SQLLite entre otros.

Las características clave son:

* **Rápido**: Alto rendimiento para hacer ingestas masivas con sqlalchemy, usa la tenica de cargas por lotes para hacer insersion de grandes volumnes de datos.
* **Rápido para codificar**: aumente la velocidad para desarrollar soluciones BI y análitica entre un 100% y un 200%. 
* **Menos errores**: Reduzca aproximadamente el 40% de los errores inducidos por humanos (desarrolladores). 
* **Fácil**: Diseñado para que sea fácil de usar y aprender. Menos tiempo leyendo documentos.
* **Corto**: Minimiza la duplicación de código. Varias características de cada declaración de parámetro. Menos errores.

## Requirements

Python 3.6+

ArmadilloSQL se apoya en los hombros de gigantes::

* <a href="https://pypi.org/project/SQLAlchemy/" class="external-link" target="_blank">sqlalchemy</a> Para ingestas masivas de datos.
* <a href="https://pypi.org/project/psycopg2/" class="external-link" target="_blank">psycopg2</a> Adaptador de base de datos PostgreSQL.
* <a href="https://pypi.org/project/mysql-connector/" class="external-link" target="_blank">mysql.connector</a> Controlador MySQL.

## Ejemplo de uso

### Create

- Para Mysql crear archivo `coneccion_mysql.json` con la siguiente estructura:

	```Javascript
	{   
		"database_motor": "mysql", 
		"database_username" : "root" ,
		"database_password" : "" ,
		"database_ip" : "localhost",
		"database_name" : "prueba",
		"database_driver": "mysql+mysqlconnector" ,	
		"database_options" : "" 
	}
	```

- Para PostgreSQL  crear archivo `coneccion_postgresql.json` con la siguiente estructura:

	```Javascript
	{
		"database_motor": "postgresql",
		"database_username" : "postgres" ,
		"database_password" : "clave" ,
		"database_ip" : "localhost",
		"database_name" : "name_bd",
		"database_driver": "postgresql+psycopg2",
		"database_options" : "dbo,public" 
	}
	```

- Crear carpeta rutinas_sql para almacenar todos los archivos .sql
	```
	mkdir rutinas_sql && cd rutinas_sql
	```

- Si utiliza anaconda puede crear un entorno por separado para su programa (opcional)
	```
	conda create -n nuevo_proyecto python=3.7
	conda activate nuevo_proyecto
	```

- Navegue hasta la carpeta que creó "rutinas_sql" e instale las dependencias de armadillosql.
	```
	pip install -r requirements.txt
	```

- Crear archivo `main.py` con:

```Python
from armadillosql import Armadillosql

def get_config(self,bd):
	"""
	Recibe el nombre de la conexión json creada anteriormente
	"""
	try:            
		with open(bd+'.json') as f_in:
			json_str = f_in.read()
			return json.loads(json_str)
	except:
		return "error"

#Instancia armadillosql
try:
	sql = Armadillosql(get_config('coneccion_mysql'),log) 
except Exception as e:
	alert("[Error] Problemas con la cadena de conexión" + str(e))

#uso de armadillosql
folder = 'rutinas_sql/'
params = {"periodo" : '2021-01-01'}
df = sql.executeFile(folder + 'query.sql',params,devolucion=True)
```

## License

Este proyecto tiene la licencia de acuerdo con los términos de la licencia del MIT.
