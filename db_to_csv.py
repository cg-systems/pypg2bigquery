"""
Copyright 2023 CG Systems Ingenieria de Software

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


This solution is based on a proposal by Faisal K K on their blog:
   https://hevodata.com/blog/postgresql-to-bigquery-data-migration/


Authors:
   - Oscar Emmanuel Torres Carrillo (etorres@cg-sys.com)
   - Julio César Culebro González (jculebro@cg-sys.com) - LinkedIn: linkedin.com/in/julio-c%C3%A9sar-culebro-gonz%C3%A1lez-92038443/

File Name: db_to_csv.py
Version: 1.0.1
Creation Date: 2023-09

Description: This code connects to the postgres database (local) and invokes the database function db_to_csv(), 
you must configure the connection parameters to postgres, they are after the comment "# Connection parameters",
you can also adjust the path and names of output and error files, they are after the comment "# Output and Error file's paths".
It must be invoked with the frequency that we want to synchronize the data, either with cron or with scheduled Windows tasks.

Descripcion: Este código se conecta a la base de datos postgres (local) e invoca la función de base de datos db_to_csv(), 
debes configurar los parámetros de conexión a postgres, están después del comentario "# Parámetros de conexión", 
tambien puedes ajustar la ruta y nombres de archivos de salida y error, están después del comentario "# Rutas de archivos de salida y errores".
Se debe invocar con la frencuencia que deseamos sincronizar los datos, ya sea con cron o con tareas programadas de windows. 
"""

import psycopg2
import os
import sys

# Connection parameters
# Parámetros de conexión
dbname = 'bd'
host = 'localhost'
port = '5432'
user = 'user'
password = 'pass'

# Output and Error file's paths 
# Rutas de archivos de salida y errores
OUTPUT_PATH = r'C:\bq\pg_salida.txt'
OUTPUT_PATHERR = r'C:\bq\pg_errores.txt'
log_f1 = open(OUTPUT_PATH, "a+")
log_f2 = open(OUTPUT_PATHERR, "a+")
sys.stdout = log_f1
sys.stderr = log_f2

# Function to print to output file
# Función para imprimir en el archivo de salida
def imprimir_en_salida(texto):
    print(texto)

# Function to print to error file
# Función para imprimir en el archivo de errores
def imprimir_en_errores(texto):
    print(texto, file=sys.stderr)

imprimir_en_salida ("Ver: 1.0.1")

sql_query = "select db_to_csv()"

try:
    imprimir_en_salida ("Conectando")

    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Run SQL query
    # Ejecutar la consulta SQL
    cursor.execute(sql_query)
    for row in cursor:
        imprimir_en_salida (row[0])
    connection.commit()

except psycopg2.Error as e:
    # Catch errors and print to error file
    # Capturar errores y escribirlos en el archivo de errores
    imprimir_en_errores(str(e))

finally:
    # Connection Close
    # Cerrar la conexión
    if connection:
        cursor.close()
        connection.close()
        imprimir_en_salida ("Conexión cerrada.")
