#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import smtplib # This is the SMTP library we need to send the email notification
import time # This is the time library, we need this so we can use the sleep function

smtp_username = 'enter_username_here' # This is the username used to login to your SMTP provider
smtp_password = 'enter_password_here' # This is the password used to login to your SMTP provider
smtp_host = 'enter_host_here' # This is the host of the SMTP provider
smtp_port = 25 # This is the port that your SMTP provider uses

smtp_sender = "sender@email.com" # This is the FROM email address
smtp_receivers = ['receiver@email.com'] # This is the TO email address


# This is the message that will be sent when moisture IS detected.

message_save_pump = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification - Save the Pump!
Water detected, please check the pump!
"""

# This is our sendEmail function

def sendEmail(smtp_message):
  try:
    smtpObj = smtplib.SMTP(smtp_host, smtp_port)
    smtpObj.login(smtp_username, smtp_password) # If you don't need to login to your smtp provider, simply remove this line
    smtpObj.sendmail(smtp_sender, smtp_receivers, smtp_message)
    print "Successfully sent email"
  except SMTPException:
    print "Error: unable to send email"

# How often to check the soil moisture when it's wet (the water is off)
poll = 15*60 # seconds

# Count like a grown-up
GPIO.setmode(GPIO.BCM)

# GPIO 17 is our digital sensor input
GPIO.setup(17, GPIO.IN)

# GPIO 18 is used to power the digital sensor board when polling
# This is generally a really bad idea, but this is a very low power
# board and it works well for me anyway.
GPIO.setup(18, GPIO.OUT)

try:
  while True:
    GPIO.output(18, GPIO.HIGH)
    time.sleep(.2) # Wait for digital sensor to settle
    if not GPIO.input(17):
        print ','.join((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "WATER DETECTED!"))
        sendEmail(message_save_pump)
    GPIO.output(18, GPIO.LOW)
    time.sleep(poll)
except KeyboardInterrupt:
    GPIO.cleanup()
