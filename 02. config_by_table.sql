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

CREATE OR REPLACE FUNCTION table2sync_tgfn_bq_sync()
  RETURNS trigger AS
$BODY$
BEGIN

	IF (TG_OP = 'DELETE') THEN
		-- Marcar el registro eliminado para que sea sincronizado a Google Big Query
		INSERT INTO bq_delete (bq_tabla, bq_llave_primaria_1) VALUES ('table2sync', OLD.hist_transaccion);

		RETURN OLD;

	ELSE
		-- Marcar registro agregado/modificado para que sea sincronizado a Google Big Query
		NEW.hist_bq_sync := NOW();

		RETURN NEW;

	END IF;

END;$BODY$
  LANGUAGE plpgsql VOLATILE;


CREATE TRIGGER table2sync_tg_bq_sync
  BEFORE INSERT OR UPDATE OR DELETE
  ON table2sync
  FOR EACH ROW
  EXECUTE PROCEDURE table2sync_tgfn_bq_sync();
