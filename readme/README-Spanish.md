# PyPg2BigQuery
<p align="center">
  <img src='pypg2biqquery_logo.png' width=550>
</p>
<p align="center">
    【Español | <a href="..\README.md">English</a> | 
</p>

## 📖 Descripción General

Pypg2BiqQuery es un proyecto que tiene como objetivo simplificar y automatizar la sincronización de datos entre una base o más bases de datos PostgreSQL local y Google BigQuery en la plataforma de Google Cloud.
<br><br>
Este proyecto consta de dos scripts principales: db_to_csv.py y load_csv.py.
Ambos scripts operan con la frecuencia deseada para garantizar la consistencia y actualizaciones constantes de datos entre las dos plataformas.

## Características Clave

☑️ **db_to_csv.py**: Extracción de Datos desde PostgreSQL

  &ensp; ◾ Se conecta a una base de datos PostgreSQL local.

  &ensp; ◾ Invoca la función db_to_csv() para extraer datos y guardarlos en archivos CSV.

  &ensp; ◾ Configuración flexible de parámetros de conexión y rutas de archivos.

<br><br>

☑️ **load_csv.py**: Carga de Datos en BigQuery desde GCS

  &ensp; ◾ Consulta la tabla de configuración en PostgreSQL para operaciones en BigQuery.

  &ensp; ◾ Procesa archivos CSV, los carga en Google Cloud Storage (GCS) y sincroniza con tablas en BigQuery.

  &ensp; ◾ Determina si se deben insertar, actualizar o eliminar registros según la configuración.

  &ensp; ◾ Configuración flexible de parámetros de conexión y rutas de archivos.

<br><br>

## Uso Recomendado
  &ensp; 1. Clona el repositorio en tu entorno local. </br>
  &ensp; 2. Configura los parámetros de conexión y las rutas de archivos según sea necesario en ambos scripts. </br>
  &ensp; 3. Ejecuta db_to_csv.py periódicamente para extraer datos de PostgreSQL a archivos CSV. </br>
  &ensp; 4. Ejecuta load_csv.py periódicamente para cargar datos desde GCS a BigQuery y sincronizar tablas.

<br><br>

## Objetivo Principal

El objetivo principal de PyPg2BigQuery es proporcionar una solución eficiente y fácil de usar para mantener la consistencia entre una base de datos local y BigQuery en la plataforma Google Cloud.
Este proyecto busca simplificar la sincronización de datos, permitiendo a los usuarios gestionar sus datos de manera efectiva y aprovechar las capacidades de ambas plataformas de manera integrada.
<br><br>

**Nota**: PyPg2BigQuery se presenta como una herramienta esencial para aquellos que buscan una solución automatizada y confiable para la gestión de datos entre entornos locales y en la nube, contribuyendo a la eficiencia operativa y la toma de decisiones informada.

<br><br>

La centralización de datos con PyPg2BigQuery tiene como objetivo facilitar la creación de gráficas y dashboards en Looker Studio. Al consolidar la información de tu base de datos local en BigQuery, podrás aprovechar al máximo las capacidades de análisis y visualización ofrecidas por Looker Studio, permitiéndote tomar decisiones informadas y obtener información valiosa a partir de tus datos.
<br><br>
¡Aprovecha al máximo PyPg2BigQuery para potenciar tus análisis y visualizaciones en Looker Studio!

<br><br>

## 👨‍💻‍ Colaboradores del Software

<a href="https://github.com/emmanuhellt"><img src="https://avatars.githubusercontent.com/u/136921808?v=4" alt="Colaborador" style="width:5%; border-radius: 50%;"/></a>
<a href="https://github.com/jculebro"><img src="https://avatars.githubusercontent.com/u/2366703?v=4" alt="Colaborador" style="width:5%; border-radius: 50%;"/></a>

<br><br>

## Comparte un Café Virtual y Apoya a PyPg2BigQuery ☕

Si PyPg2BigQuery ha aportado valor a tus proyectos, ¡considera compartir un café virtual con nosotros! </br>
Tu contribución en <a href="https://www.buymeacoffee.com/pypg2bq">Buy Me a Coffee</a> nos ayuda a mantener nuestro código alimentado y respalda el desarrollo continuo. </br></br>

<a href="https://www.buymeacoffee.com/pypg2bq">¡Donar un Café a PyPg2BigQuery!</a>

 </br>

¡Gracias por ser parte de nuestra comunidad!

 </br></br>

## ⚖️ Licencia

- Licencia del Código Fuente: El código fuente de nuestro proyecto está licenciado bajo la Licencia Apache 2.0. Esta licencia permite el uso, modificación y distribución del código, sujeto a ciertas condiciones descritas en la Licencia Apache 2.0.
