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
"""

import psycopg2
import os
import sys
import subprocess

# Parámetros de conexión
dbname = 'bd'
host = 'localhost'
port = '5432'
user = 'user'
password = 'pass'

# Rutas de archivos de salida y errores
OUTPUT_PATH = r'C:\bq\bq_salida.txt'
OUTPUT_PATHERR = r'C:\bq\bq_errores.txt'
log_f1 = open(OUTPUT_PATH, "a+")
log_f2 = open(OUTPUT_PATHERR, "a+")
sys.stdout = log_f1
sys.stderr = log_f2

process_ok = True

# Función para imprimir en el archivo de salida
def imprimir_en_salida(texto):
    print(texto)

# Función para imprimir en el archivo de errores
def imprimir_en_errores(texto):
    print(texto, file=sys.stderr)

imprimir_en_salida("Ver: 1.0.1")

# Conectar a la base de datos
try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = connection.cursor()

    # Ejecutar la consulta para obtener los valores de bq_bucket_name, bq_project_name y bq_dataset_name
    query = "SELECT bq_empresa, bq_tabla, bq_campos_select, bq_campo_llave_primaria_1, bq_bucket_name, bq_project_name, bq_dataset_name FROM bq_sync ORDER BY bq_clave"
    cursor.execute(query)

    # Procesar los resultados
    for row in cursor.fetchall():

        bq_empresa = row[0]  # Obtén el valor de bq_empresa
        bq_tabla = row[1]
        bq_campo_llave_primaria_1 = row[3]
        bq_bucket_name = row[4]
        bq_project_name = row[5]
        bq_dataset_name = row[6]

        # Generar la ruta local dinámica basada en bq_empresa
        local_path = os.path.join(r'C:\bq', bq_empresa)

        # Verificar si la ruta local existe, si no, créala
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        # Obtener archivos CSV que contienen el nombre de la tabla en la ruta C:\bq\bq_empresa\
        csv_files = [filename for filename in sorted(os.listdir(local_path)) if bq_tabla in filename and filename.endswith('.csv')]

        for csv_file in csv_files:
            # Generar las rutas para Google Cloud Storage
            gsutil_source = os.path.join(local_path, csv_file)
            gsutil_destination = f'gs://{bq_bucket_name}/{bq_empresa}/{csv_file}'  # Utilizar gs:// para la ruta de destino
            bq_schema_url = f"gs://{bq_bucket_name}/{bq_tabla}_schema.json"
            bq_schema_file = os.path.join(r'C:\bq', f'{bq_tabla}_schema.json')

            try:

                imprimir_en_salida(f"Procesando archivo: {gsutil_source}")

                # Subir el archivo a Google Cloud Storage utilizando gsutil
                gsutil_cmd = ['gsutil', 'cp', gsutil_source, gsutil_destination]
                res_process = subprocess.run(gsutil_cmd, check=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, shell=True)  # Verificar si hubo un error
                imprimir_en_salida('returncode:' + str(res_process.returncode))
                imprimir_en_salida(res_process.stdout)
                imprimir_en_errores(res_process.stderr)

                if res_process.returncode != 0:
                    raise Exception('returncode:' + str(res_process.returncode))

                imprimir_en_salida(f"Archivo {csv_file} subido exitosamente a Google Cloud Storage.")

                # Determinar si el archivo debe cargarse en la tabla bq_tabla_upd o bq_tabla_del
                if '_del' in csv_file:
                    bq_table = f'{bq_project_name}:{bq_dataset_name}.{bq_tabla}_del'
                    bq_load_command = f'bq load --autodetect --noreplace {bq_table} {gsutil_destination}'
                else:
                    bq_table = f'{bq_project_name}:{bq_dataset_name}.{bq_tabla}_upd'
                    bq_load_command = f'bq load --autodetect --noreplace {bq_table} {gsutil_destination} {bq_schema_file}'

                # Ejecutar bq load
                bq_load_result = os.system(bq_load_command)

                if bq_load_result == 0:  # 0 indica éxito
                    imprimir_en_salida(f"Carga a {bq_table} exitosa.")

                    if '_del' in csv_file:

                        # Generar la consulta DELETE
                        consulta_delete = (
                            f'bq query --use_legacy_sql=false '
                            f'"DELETE {bq_dataset_name}.{bq_tabla} f '
                            f'WHERE CONCAT(f.{bq_campo_llave_primaria_1}, \'-\', f.empresa) IN '
                            f'(SELECT CONCAT(hist_transaccion, \'-\', empresa) from {bq_dataset_name}.{bq_tabla}_del)"'
                        )

                        # Ejecutar la consulta DELETE en BigQuery
                        delete_result = subprocess.run(consulta_delete, capture_output=True, text=True, shell=True)

                        if delete_result.returncode == 0 or "[DONE]" in delete_result.stdout:
                            imprimir_en_salida(f"Consulta DELETE para {bq_table} ejecutada exitosamente.")
                            imprimir_en_salida(delete_result.stdout)
                        else:
                            imprimir_en_errores(f"Error en la consulta DELETE para {bq_table}:")
                            imprimir_en_errores(delete_result.stderr)
                            process_ok = False

                    else:

                        # Obtener la lista de campos a actualizar / insertar
                        bq_campos_select = row[2].split(',')

                        # Campos clave
                        campos_clave = ['empresa', bq_campo_llave_primaria_1]

                        # Crear la lista de campos a actualizar / insertar excluyendo los campos clave
                        campos_actualizar = [campo for campo in bq_campos_select if campo not in campos_clave]

                        # Generar la lista de campos para las consultas SET y SELECT
                        campos_set = ', '.join([f't.{campo} = s.{campo}' for campo in campos_actualizar])
                        campos_select = ', '.join(campos_clave + campos_actualizar)

                        # Generar la consulta UPDATE
                        consulta_update = (
                            f'bq query --use_legacy_sql=false '
                            f'"UPDATE {bq_dataset_name}.{bq_tabla} t '
                            f'SET {campos_set} '
                            f'FROM {bq_dataset_name}.{bq_tabla}_upd s '
                            f'WHERE s.empresa = UPPER(\'{bq_empresa}\') AND t.{campos_clave[0]} = s.{campos_clave[0]} AND t.{campos_clave[1]} = s.{campos_clave[1]}"'
                        )

                        # Generar la consulta INSERT
                        consulta_insert = (
                            f'bq query --use_legacy_sql=false '
                            f'"INSERT {bq_dataset_name}.{bq_tabla} ({campos_select}) '
                            f'"SELECT {campos_select} '
                            f'FROM {bq_dataset_name}.{bq_tabla}_upd '
                            f'WHERE NOT CONCAT({campos_clave[1]}, \'-\', {campos_clave[0]}) IN '
                            f'(SELECT CONCAT({campos_clave[1]}, \'-\', {campos_clave[0]}) FROM {bq_dataset_name}.{bq_tabla})"'
                        )

                        # Ejecutar la consulta UPDATE en BigQuery
                        update_result = subprocess.run(consulta_update, capture_output=True, text=True, shell=True)

                        if update_result.returncode == 0 or "[DONE]" in update_result.stdout:
                            imprimir_en_salida(f"Consulta UPDATE para {bq_table} ejecutada exitosamente.")
                            imprimir_en_salida(update_result.stdout)
                        else:
                            imprimir_en_errores(f"Error en la consulta UPDATE para {bq_table}:")
                            imprimir_en_errores(consulta_update)
                            imprimir_en_errores(update_result.stderr)
                            imprimir_en_errores(update_result.stdout)
                            process_ok = False

                        # Ejecutar la consulta INSERT en BigQuery
                        insert_result = subprocess.run(consulta_insert, capture_output=True, text=True, shell=True)

                        if insert_result.returncode == 0 or "[DONE]" in insert_result.stdout:
                            imprimir_en_salida(f"Consulta INSERT para {bq_table} ejecutada exitosamente.")
                            imprimir_en_salida(insert_result.stdout)
                        else:
                            imprimir_en_errores(f"Error en la consulta INSERT para {bq_table}:")
                            imprimir_en_errores(insert_result.stderr)
                            process_ok = False

                        # Generar la consulta DELETE para [tabla]_upd
                        consulta_delete_upd = (
                            f'bq query --use_legacy_sql=false '
                            f'"DELETE {bq_dataset_name}.{bq_tabla}_upd f WHERE f.empresa = UPPER(\'{bq_empresa}\')"'
                        )

                        # Ejecutar la consulta DELETE en BigQuery
                        delete_upd_result = subprocess.run(consulta_delete_upd, capture_output=True, text=True, shell=True)

                        if delete_upd_result.returncode == 0 or "[DONE]" in delete_upd_result.stdout:
                            imprimir_en_salida(f"Consulta DELETE para {bq_table}_upd ejecutada exitosamente.")
                            imprimir_en_salida(delete_upd_result.stdout)
                        else:
                            imprimir_en_errores(f"Error en la consulta DELETE para {bq_table}_upd:")
                            imprimir_en_errores(delete_upd_result.stderr)
                            process_ok = False

                    if process_ok:
                        # Si todo fue exitoso, eliminar el archivo CSV
                        os.remove(gsutil_source)
                        # Eliminar el archivo de Google Cloud Storage utilizando gsutil
                        gsutil_cmd_del = ['gsutil', 'rm', gsutil_destination]
                        subprocess.run(gsutil_cmd_del, check=False, shell=True)  # Verificar si hubo un error

                else:
                    imprimir_en_errores(f"Error al cargar a {bq_table}.")

            except Exception as e:
                imprimir_en_errores(f"Error al subir el archivo {csv_file} a Google Cloud Storage:" + str(e))

except psycopg2.Error as e:
    imprimir_en_errores("Error en la conexión o consulta:" + str(e))
except Exception as e1:
    imprimir_en_errores("Error general: " + str(e1))
finally:
    # Cerrar la conexión
    imprimir_en_salida("Conexión cerrada.")
