/*
Query para obtener 10 registros de system_variables de mysql
Nota: este tipo de query solo retorna registros
*/
SELECT variable_name,variable_scope
FROM information_schema.SYSTEM_VARIABLES
WHERE variable_scope = '{variable}'
LIMIT 10