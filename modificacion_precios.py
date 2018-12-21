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
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

## Conexion a la BD
mydb = mysql.connector.connect(
  host="-- IP FROM SERVER --",
  user="-- USER FROM BD --",
  passwd="-- PASS FROM BD --",
  database="-- BD NAME --"
)

## Existen productos modificados
mycursor = mydb.cursor()
fecha = str(datetime.now() + timedelta(days=-1)).split()[0]
query = ("SELECT count(*) FROM historial_precios WHERE fecha LIKE \""+fecha+"%\"")

mycursor.execute(query)

for q in mycursor:
  log = open("log.txt", "a")
  if q[0] > 0:
    _fecha_inicio = str(datetime.now() + timedelta(days=-30)).split()[0]
    fecha_inicio = _fecha_inicio.split("-")
    fecha_fin = fecha.split("-")

    try:
      f = "-- FROM MAIL --"
      t = "-- TO MAIL --" 

      # Create message container - the correct MIME type is multipart/alternative.
      msg = MIMEMultipart('alternative')
      msg['Subject'] = "Precios modificados [Productos]"
      msg['From'] = f
      msg['To'] = t

      # Create the body of the message (a plain-text and an HTML version).
      text = "Hay productos que modificaron sus precios"
      html = """\
      <html>
        <head></head>
        <body>
        <img src="-- LOGO --" />
          <h2 align="center" style="color: #4c87cd;">Hay productos que modificaron sus precios</h2>
          <h4 align="center"><a href="--- URL AL LISTADO ---" target="_blank">Ir al listado</a></h4>
          <hr />
          Atte. El Centinela
        </body>
      </html>
      """

      # Guarda las partes del mensaje
      part1 = MIMEText(text, 'plain')
      part2 = MIMEText(html, 'html')

      # Agrega el cuerpo del mensaje
      msg.attach(part1)
      msg.attach(part2)

      server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # GMAIL, if you want to use other service, change the smtp server and port
      server.login('-- USER MAIL --', '-- PASS MAIL --')
      server.sendmail(f, t, msg.as_string())
      server.close()
      log.write('[ ' + time.ctime() + ' ] Modificacion >>> ENVIADO.\n') ## Log
    except:
      log.write('[ ' + time.ctime() + ' ] Modificacion >>> ERROR: No se envio el mail.\n') ## Log
  else :
    log.write('[ ' + time.ctime() + ' ] Modificacion >>> No existian modificaciones.\n') ## Log

mycursor.close()
mydb.close()
log.close()