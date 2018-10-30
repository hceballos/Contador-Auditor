#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import pandas as pd

cnx = sqlite3.connect('data.db')

consulta  = "SELECT \
t_last_year.cuenta as CUENTA, \
last_year as [AÑO PASADO], \
last_month as [MES PASADO], \
last_week as [SEMANA PASADA], \
current_week as [SEMANA ACTUAL] \
FROM \
	(SELECT \
		cuenta, \
		Sum(debe-haber) AS last_year \
	FROM \
		MovimientosTabla \
	WHERE \
		fecha between date('NOW', '-5 YEARS', 'START OF YEAR') and date('NOW', '-1 YEAR') \
	GROUP BY \
		cuenta \
	HAVING \
		cuenta LIKE '%' \
		AND \
		[last_year]<>0 \
	ORDER BY \
		cuenta asc \
	)t_last_year \
 \
LEFT JOIN \
	(SELECT \
		cuenta, \
		Sum(debe-haber) AS last_month \
	FROM \
		MovimientosTabla \
	WHERE \
		fecha between date('NOW', '-5 YEARS', 'START OF YEAR') and date('NOW', '-1 MONTHS') \
	GROUP BY \
		cuenta \
	HAVING \
		cuenta LIKE '%' \
		AND \
		[last_month]<>0 \
	ORDER BY \
		cuenta asc \
	)t_last_month \
 \
ON t_last_month.cuenta = t_last_year.cuenta \
 \
LEFT JOIN \
	(SELECT \
		cuenta, \
		Sum(debe-haber) AS last_week \
	FROM \
		MovimientosTabla \
	WHERE \
		fecha between date('NOW', '-5 YEARS', 'START OF YEAR') and date('NOW', '-7 DAYS') \
	GROUP BY \
		cuenta \
	HAVING \
		cuenta LIKE '%' \
		AND \
		[last_week]<>0 \
	ORDER BY \
		cuenta asc \
	)t_last_week \
 \
ON t_last_week.cuenta = t_last_year.cuenta \
LEFT JOIN \
	(SELECT \
		cuenta, \
		Sum(debe-haber) AS current_week \
	FROM \
		MovimientosTabla \
	WHERE \
		fecha between date('NOW', '-5 YEARS', 'START OF YEAR') and date('NOW') \
	GROUP BY \
		cuenta \
	HAVING \
		cuenta LIKE '%' \
		AND \
		[current_week]<>0 \
	ORDER BY \
		cuenta asc \
    )t_current_week \
ON t_current_week.cuenta = t_last_year.cuenta;"

datos = pd.read_sql_query(consulta, cnx)

writer = pd.ExcelWriter('Comparabilidad_de_estados_financieros.xlsx', engine='xlsxwriter')
datos.to_excel(writer, sheet_name='Todas las cuentas')
writer.save()

datos.to_html('Comparabilidad_de_estados_financieros.html')