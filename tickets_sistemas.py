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
owner_id     =   '-- ID DEL CHAT DE DESTINO --'
bot         =   telepot.Bot(token)

## Comandos
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    # Cargan un ticket
    if command.startswith('/ticket'):
        # Es empleado ?
        empleado = mydb.cursor()
        empleado.execute("SELECT user, nombre FROM usuarios WHERE id_tlg = '"+ chat_id +"' LIMIT 1;")

        for e in empleado:
            if e != '':
                #Obtener el Problema
                problema = commnand.split('/ticket ')[1]

                if problema != '':
                    # Cargar ticket
                    newTicket = mydb.cursor()
                    newTicket.execute("INSERT INTO tickets_sistemas SET usuario = '"+ e[0] +"', problema = '"+ problema +"', fecha_carga = '"+ str(time("%Y-%m-%d %H:%i:%s")) +"';")
                    
                    # Ultimo Ticket
                    lastTicket = mydb.cursor()
                    lastTicket.execute("SELECT max(id) as last FROM tickets_sistemas;")
                    for lt in lastTicket:
                        setTracking = mydb.cursor()
                        setTracking.execute("UPDATE tickets_sistemas SET tracking = 'TLG"+ lastTicket[0] +"' WHERE id = '"+ lastTicket[0] +"';")

                        # Enviar mensajes
                        bot.sendMessage(chat_id, 'Ticket cargado: #TLG'+ lastTicket[0]) # Avisar que se cargo
                        bot.sendMessage(owner_id, '-- Nuevo Ticket --\n#TLG'+ lastTicket[0] +'\nDe: '+ empleado[1] +'\n\nProblema: '+ problema +'\nFecha de carga: '+ str(time("%d-%m-%Y %H:%i")) ) # Avisarle a Sistemas
                    lastTicket.close()
                    newTicket.close()
            else:
                bot.sendMessage(chat_id, 'No autorizado') # ERROR
                stikers = ['CAADAgADlgMAAkcVaAn0Ao0SlzscmgI', 'CAADAQADjgADrsViAAHXGlXCEhIXKgI'] # Mandarle un sticker
                bot.sendSticker(chat_id, str(random.choice(stikers)) )

        empleado.close()

bot = telepot.Bot(token) ## Poner el Token mas arriba
bot.message_loop(handle)



    ########################################
    ## DE ESTA MANERA SE PUEDEN CARGAR    ##
    ## TICKETS PARA QUE SEAN SOLUCIONADOS ##
    ## POR EL AREA DE SISTEMAS.           ##
    ## EN ESTE CASO, SOLO ES QUIEN ESTA   ##
    ## COMO owner_id                      ##
    ########################################