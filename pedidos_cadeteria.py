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

## Basic imports & configuration
import os
import sys
import time
import random
import datetime
import telepot
import mysql.connector
from datetime import datetime, timedelta, date

## Conexion a la BD
mydb = mysql.connector.connect(
  host="-- IP FROM SERVER --",
  user="-- USER FROM BD --",
  passwd="-- PASS FROM BD --",
  database="-- BD NAME --"
)

## Bot data
token       =   '-- TOKEN BOT --'
chat_id     =   '-- ID DEL CHAT DE DESTINO --'
bot         =   telepot.Bot(token)

## PEDIDOS
manana  = str(datetime.now() + timedelta(days=+1)).split(' ')[0]
data    = mydb.cursor()
data.execute("SELECT * FROM cadeteria WHERE auth = 's' AND fecha LIKE \""+ manana +"%\";")

for fm in data:
    bot.sendMessage(chat_id, '#MOTO'+ str(fm[0]) + 
        '\n -- Fecha: '+ str(fm[15]).split(' ')[0] +' -- '+
        '\nInicia en: \n'+ str(fm[1].encode('ascii',  'ignore').decode('ascii')) +' ('+ str(fm[2].encode('ascii',  'ignore').decode('ascii')) +')\nPreguntar por: '+ str(fm[3].encode('ascii',  'ignore').decode('ascii')) +
        '\n\nDestino: \n'+ str(fm[4].encode('ascii',  'ignore').decode('ascii')) +' ('+ str(fm[5].encode('ascii',  'ignore').decode('ascii')) +')\nPreguntar por: '+ str(fm[16].encode('ascii',  'ignore').decode('ascii')) +
        '\n\nHorario: '+ str(fm[6]) +' hasta las '+ str(fm[7]) +
        '\n\nTramite: '+ str(fm[8].encode('ascii',  'ignore').decode('ascii')) +
        '\n\nObs. Tramite: '+ str(fm[9].encode('ascii',  'ignore').decode('ascii')) +
        '\n\nPago: '+ str(fm[10]) +' '+ str(fm[11].encode('ascii',  'ignore').decode('ascii')) +
        '\n\nObservaciones Generales:\n'+  str(fm[12].encode('ascii',  'ignore').decode('ascii')) )


    ########################################
    ## YO SOLO CONVIERTO LOS CAMPOS       ##
    ## QUE SE QUE PUEDEN TENER CARACTERES ##
    ## RAROS, EL RESTO SON FIJOS QUE SON  ##
    ## NUMEROS O FECHAS, SI PONEN OTRA    ##
    ## COSA LOS FRENA EL SISTEMA DONDE    ##
    ## SE CARGAN LOS PEDIDOS.             ##
    ########################################