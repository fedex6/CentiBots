# -*- coding: utf-8 -*-
# 
#     ______              __   _               __      
#    / ____/___   ____   / /_ (_)____   ___   / /____ _
#   / /    / _ \ / __ \ / __// // __ \ / _ \ / // __ `/
#  / /___ /  __// / / // /_ / // / / //  __// // /_/ / 
#  \____/ \___//_/ /_/ \__//_//_/ /_/ \___//_/ \__,_/ 
#
#   Telegram: @fedex6
#
#-------------------------------------------------------#

## Imports
import mysql.connector
import time
from datetime import datetime, timedelta

## Conexion a la BD
mydb = mysql.connector.connect(
  host="-- IP FROM SERVER --",
  user="-- USER FROM BD --",
  passwd="-- PASS FROM BD --",
  database="-- BD NAME --"
)

## Fecha
fecha = str(datetime.now() + timedelta(days=+4)).split(' ')[0].split('-')

## Agrega en la BD
mycursor = mydb.cursor()
mycursor.execute("INSERT INTO cierre_camionetas SET fecha = '"+fecha[2]+"-"+fecha[1]+"-"+fecha[0]+"', camioneta = 'GARBA', fecha_cierra = '"+str(datetime.now()).split('.')[0]+"'")
mycursor.close()
mydb.commit()
mydb.close()

## LOG
log = open("log.txt", "a")
log.write('[ ' + time.ctime() + ' ] Reparto Garbarino >>> CERRADO EL REPATO PARA EL ' + fecha[2] + "-" + fecha[1] + "-" + fecha[0] + '.\n') ## Log
log.close()