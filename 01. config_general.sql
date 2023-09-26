/*
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
*/

CREATE TABLE bq_sync
  (
    bq_clave serial NOT NULL,
    bq_tabla character varying(50) NOT NULL, --Tabla local
    bq_fecha timestamp without time zone NOT NULL, -- Fecha de la última fecha de sincronización de la tabla
    bq_campo_filtro character varying NOT NULL, -- Campo que indica el nombre del campo con el cual se van a identificar los registros de la tabla que necesitan ser sincronizados
    bq_campo_llave_primaria_1 character varying NOT NULL, -- Indica el nombre del campo que funciona como Llave Primaria en la tabla indicada en el campo 'bq_tabla'
    bq_campo_llave_primaria_2 character varying, -- Para tablas con mas de una llave primaria
    bq_campos_select character varying, -- Si el valor es *, se seleccionan todos los campos; Si es diferente se seleccionan los campos indicados
    bq_empresa character varying NOT NULL DEFAULT ''::character varying, -- Identifica a que empresa o segmento de negocio pertenece la tabla a sincronizar
    bq_filtro_condiciones character varying NOT NULL DEFAULT ''::character varying, -- Condiciones adicionales para delimitar los registros a sincronizar
    bq_bucket_name character varying NOT NULL DEFAULT ''::character varying, -- Nombre del Bucket en Google Coud Storage
    bq_project_name character varying NOT NULL DEFAULT ''::character varying, -- Nombre del Proyecto en Google Coud Services
    bq_dataset_name character varying NOT NULL DEFAULT ''::character varying, -- Nombre del DataSet en Google BigQuery
    CONSTRAINT bq_sync_pkey PRIMARY KEY (bq_clave)
  );

CREATE TABLE bq_delete
  (
    bq_clave serial NOT NULL,
    bq_tabla character varying NOT NULL, --Tabla local
    bq_fecha_sincronizacion timestamp without time zone NOT NULL DEFAULT now(), -- Indica la fecha más reciente de sincronización a Google Big Query
    bq_llave_primaria_1 character varying NOT NULL, -- Indica el nombre del campo que funciona como Llave Primaria en la tabla indicada en el campo 'bq_tabla'
    bq_llave_primaria_2 character varying, -- Para tablas con mas de una llave primaria
    bq_empresa character varying NOT NULL DEFAULT ''::character varying, -- Identifica a que empresa o segmento de negocio pertenece la tabla a sincronizar
    CONSTRAINT bq_delete_pkey PRIMARY KEY (bq_clave)
  );

CREATE OR REPLACE FUNCTION db_to_csv(var_empresa text)
  RETURNS void AS
$BODY$
DECLARE
	aux_tables RECORD;
	statement TEXT;
	path TEXT;

BEGIN
--Conversi�n de los resultados de una Consulta a un archivo CSV
--Usado para la sincronizaci�n de PostgreSQL a Big Query

	path := 'C:\bq\';

	FOR aux_tables IN
		SELECT *
		FROM bq_sync
		LOOP

			--Buscar Registros para Insertar / Actualizar
			statement := 'COPY (SELECT ''' || var_empresa || ''' AS Empresa, ' || aux_tables.bq_campos_select || ' FROM ' || aux_tables.bq_tabla || ' WHERE ' || aux_tables.bq_campo_filtro || ' > ''' || aux_tables.bq_fecha || ''''
					') TO ''' || path || aux_tables.bq_tabla || '.csv' ||''' DELIMITER '','' CSV HEADER;';
			EXECUTE statement;


			--Buscar Registros para Eliminar
			statement := 'COPY (SELECT ''' || var_empresa || ''' AS Empresa, bq_llave_primaria_1 AS ' || aux_tables.bq_campo_llave_primaria_1 ||
					CASE WHEN ISNULL(aux_tables.bq_campo_llave_primaria_2,'') <> '' THEN ', bq_llave_primaria_1 AS ' || aux_tables.bq_campo_llave_primaria_2 ELSE '' END ||
					' FROM bq_delete WHERE bq_tabla = ''' || aux_tables.bq_tabla || ''' AND bq_fecha_sincronizacion > ''' || aux_tables.bq_fecha || ''''
					') TO ''' || path || aux_tables.bq_tabla || '_del.csv' ||''' DELIMITER '','' CSV HEADER;';
			EXECUTE statement;

			--Marcar el Registro como actualizado en la tabla de Configuraci�n de Sincronizaci�n
			statement := 'UPDATE bq_sync SET bq_fecha = NOW() WHERE bq_clave = ' || aux_tables.bq_clave;
			EXECUTE statement;

		END LOOP;
	return;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE;
