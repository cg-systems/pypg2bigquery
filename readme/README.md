# PyPg2BigQuery

<p align="center">
  <img src='pypg2biqquery_logo.jpg' width=550>
</p>

<p align="center">
    【English | <a href="readme/README-Spanish.md">Spanish</a> | 
</p>

## 📖 Overview

Pypg2BiqQuery is a project aimed at simplifying and automating data synchronization between a local PostgreSQL database and Google BigQuery on the Google Cloud platform. 
<br>
This project consists of two main scripts: db_to_csv.py and load_csv.py. 
Both scripts operate at the desired frequency to ensure consistency and constant data updates between the two platforms.

## Key Features


☑️ **db_to_csv.py**: Data Extraction from PostgreSQL

◾ Connects to a local PostgreSQL database.

◾ Invokes the db_to_csv() function to extract data and store it in CSV files.

◾ Flexible configuration of connection parameters and file paths.

<br>

☑️ **load_csv.py**: Data Loading into BigQuery from GCS

◾ Queries the configuration table in PostgreSQL for BigQuery operations.

◾ Processes CSV files, uploads them to Google Cloud Storage (GCS), and synchronizes with tables in BigQuery.

◾ Determines whether to insert, update, or delete records based on the configuration.

◾ Flexible configuration of connection parameters and file paths.

<br>

## Recommended Usage

1. Clone the repository to your local environment.
2. Configure connection parameters and file paths as needed in both scripts.
3. Run db_to_csv.py periodically to extract data from PostgreSQL to CSV files.
4. Run load_csv.py periodically to load data from GCS to BigQuery and synchronize tables.

<br>

## Primary Objective

The primary goal of PyPg2BigQuery is to provide an efficient and user-friendly solution for maintaining consistency between a local database and BigQuery on the Google Cloud Platform. 
This project aims to simplify data synchronization, enabling users to manage their data effectively and leverage the capabilities of both platforms in an integrated manner.
<br>

**Note:** PyPg2BigQuery is presented as an essential tool for those seeking an automated and reliable solution for data management between local and cloud environments, contributing to operational efficiency and informed decision-making.

<br>

## 👨‍💻‍ Software Contributors

<a href="https://github.com/emmanuhellt"><img src="https://avatars.githubusercontent.com/u/136921808?v=4" alt="Contributor" style="width:5%; border-radius: 50%;"/></a>
<a href="https://github.com/jculebro"><img src="https://avatars.githubusercontent.com/u/2366703?v=4" alt="Contributor" style="width:5%; border-radius: 50%;"/></a>

