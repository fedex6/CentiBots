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
fecha = str(datetime.now()).split()[0]
c_query = ("SELECT count(*) FROM promociones WHERE fecha_inicio <= '"+fecha+" 00:00:00' AND fecha_fin >= '"+fecha+" 00:00:00';")
	## This query search promos that are available at the BD

mycursor.execute(c_query)

for q in mycursor:
  if q[0] > 0:
    log = open("log.txt", "a")

    f = "-- FROM MAIL"
    t = "-- TO MAIL --" 

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "PROMOS vigentes [Promociones]"
    msg['From'] = f
    msg['To'] = t

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hay promociones vigentes"
    html = """\
    <html>
      <head></head>
      <body>
      <img src="-- LOGO --" />
        <h1>PROMOS</h1>
        <table width="850px" cellpadding="0" cellspacing="0">
          <thead>
            <tr style="background-color: #4c87cd; color: #FFF;">
              <th>Inicio</th>
              <th>Fin</th>
              <th>Producto</th>
              <th width="425px">Detalle</th>
            </tr>
          </thead>

          <tbody>
    """

    query = ("SELECT * FROM promociones WHERE fecha_inicio <= '"+fecha+" 00:00:00' AND fecha_fin >= '"+fecha+" 00:00:00';")
    rows = mydb.cursor()
    rows.execute(query)

    for x in rows:
      _fini = str(x[1]).split()[0]
      fini = _fini.split('-')
      _ffin = str(x[2]).split()[0]
      ffin = _ffin.split('-')
      obs = x[4].encode('ascii',  'ignore').decode('ascii')

      html += """\
      <tr valign="top">
          <td>"""+fini[2]+"""/"""+fini[1]+"""/"""+fini[0]+"""</td>
          <td>"""+ffin[2]+"""/"""+ffin[1]+"""/"""+ffin[0]+"""</td>
          <td>"""+x[3]+"""</td>
          <td>"""+obs+"""</td>
      </tr>

      <tr>
        <td colspan="4"><hr /></td>
      </tr>
      """

    html += """</tbody>
        </table>
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

    # Enviar el Mail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # GMAIL, if you want to use other service, change the smtp server and port
    server.login('-- USER MAIL --', '-- PASS MAIL --')
    server.sendmail(f, t, msg.as_string())
    server.close()
    log.write('[ ' + time.ctime() + ' ] Promociones >>> ENVIADO.\n') ## Log
  else :
    log.write('[ ' + time.ctime() + ' ] Promociones >>> No hay promociones vigentes.\n') ## Log

mycursor.close()
mydb.close()
log.close()