#!/usr/bin/python3
#-*- coding: utf-8 -*-

from email.mime.base import MIMEBase
import smtplib
import mimetypes
import os, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import ntpath


# Import default vars
from pyutil import defaults
defaults = defaults.mail

home = os.path.expanduser("~")
user_settings_file = os.path.join(home, "pyutil_settings.json")

defaults = dict(defaults)

if os.path.exists(user_settings_file):
    with open(user_settings_file) as file:
        try:
            user_defaults = json.load(file)["mail"]
        except json.decoder.JSONDecodeError:
            print(user_settings_file+" does not contain valid JSON format!")
        except KeyError:
            # No user settings set, so dont orverwrite package defaults
            defaults = defaults
        else:
            defaults.update(user_defaults)

class Mail:
    def __init__(self, from_email=None, server=None, port=None, username=None, password=None, filepath=None):
        """ Sort out the given variables and if neccessary fill in default variables
        """

        self.server = server if server is not None else defaults["server"]
        self.port = port if port is not None else defaults["port"]
        self.filepath = filepath if filepath is not None else defaults["filepath"]
        self.from_email = from_email if from_email is not None else defaults["from_email"]
        self.username = username if username is not None else defaults["username"]
        self.password = password if password is not None else defaults["password"]

        self.server = smtplib.SMTP(self.server, self.port)
        self.msg = MIMEMultipart()
        # If a password is given, use it to login to the mailserver
        if self.password != "None":
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.username, self.password)

        self.msg["From"] = self.from_email

        # Check if user wants to send a file, if so read the specified file
        if self.filepath != None and os.path.exists(self.filepath):
            with open(self.filepath, "rb") as file:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment; filename="+ntpath.basename(self.filepath))
            # Attach the file to the message
            self.msg.attach(attachment)

    def send(self, subject, text, receipient):
        """ Send the mail
            Usage:
            instance.send(subject, text, [receipient1, receipent2])
            Or:
            instance.send(subject, text, receipient)
        """

        #.subject = subject
        #self.text = text
        #self.receipient = receipient

        # Set subject to mail
        self.msg["Subject"]  = subject

        # Set actual text of the email
        #body = text
        self.msg.attach(MIMEText(text, "html"))

        # If given receipients is a list object cycle through list of receipients
        if type(receipient) == list:
            for email in receipient:
                # Set receipient in email header
                self.msg["To"] = email
                # Built the massage object
                message = self.msg.as_string()

                # Try to send mail
                try:
                    self.server.sendmail(self.from_email, email, message)
                    self.server.quit()
                    print("Success: Sent email \""+subject+"\" from \""+self.from_email+"\" to \""+email+"\"")
                except:
                    print("Error: Unable to send email \""+subject+"\" from \""+self.from_email+"\" to \""+email+"\"")

        # If given receipients is not a list, just try to send the mail
        else:
            email = receipient
            # Set receipient in email header
            self.msg["To"] = email
            # Built the massage object
            message = self.msg.as_string()

            try:
                self.server.sendmail(self.from_email, email, message)
                self.server.quit()
                print("Success: Sent email \""+subject+"\" from \""+self.from_email+"\" to \""+email+"\"")
            except Exception as e:
                print("Error: Unable to send email \""+subject+"\" from \""+self.from_email+"\" to \""+email+"\"")
                raise e
