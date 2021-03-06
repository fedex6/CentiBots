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
owner_id     =   '-- ID DEL CHAT DEL PROPIETARIO --' # En este caso hay una sola persona en Sistemas.
bot         =   telepot.Bot(token)

## Comandos
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    # Cargan un ticket
    if command.startswith('/ticket'):
        # Es empleado ?
        empleado = mydb.cursor()
        empleado.execute("SELECT user, nombre FROM usuarios WHERE id_tlg = '"+ str(chat_id) +"' LIMIT 1;")

        for e in empleado:
            if e != '':
                #Obtener el Problema
                problema = command.split('/ticket ')[1]

                if problema != '':
                    # Cargar ticket
                    newTicket = mydb.cursor()
                    newTicket.execute("INSERT INTO tickets_sistemas SET usuario = '"+ e[0] +"', problema = '"+ problema +"', fecha_carga = '"+ str(time.strftime("%Y-%m-%d %H:%M:%S")) +"';")
                    mydb.commit()

                    # Ultimo Ticket
                    lastTicket = mydb.cursor()
                    lastTicket.execute("SELECT max(id) as last FROM tickets_sistemas;")

                    for lt in lastTicket:
                        setTracking = mydb.cursor()
                        setTracking.execute("UPDATE tickets_sistemas SET tracking = 'TLG"+ str(lt[0]) +"' WHERE id = "+ str(lt[0]) +";")
                        mydb.commit()
                        setTracking.close()

                        # Enviar mensajes
                        bot.sendMessage(chat_id, 'Ticket cargado: #TLG'+ str(lt[0])) # Avisar que se cargo
                        bot.sendMessage(owner_id, '-- Nuevo Ticket --\n#TLG'+ str(lt[0]) +'\nDe: '+ e[1] +'\n\nProblema: '+ problema +'\nFecha de carga: '+ str(time.strftime("%d-%m-%Y %H:%M")) ) # Avisarle a Sistemas
                    lastTicket.close()
                    newTicket.close()
            else:
                bot.sendMessage(chat_id, 'No autorizado') # ERROR
                stikers = ['CAADAgADlgMAAkcVaAn0Ao0SlzscmgI', 'CAADAQADjgADrsViAAHXGlXCEhIXKgI'] # Mandarle un sticker
                bot.sendSticker(chat_id, str(random.choice(stikers)) )

        empleado.close()

bot.message_loop(handle)

while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Terminado')
            exit()

    ########################################
    ## DE ESTA MANERA SE PUEDEN CARGAR    ##
    ## TICKETS PARA QUE SEAN SOLUCIONADOS ##
    ## POR EL AREA DE SISTEMAS.           ##
    ## EN ESTE CASO, SOLO ES QUIEN ESTA   ##
    ## COMO owner_id                      ##
    ########################################