# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# create message object instance
class Send():
    def sendMessage(self,senha,email):
        

        msg = MIMEMultipart()
        
        message = "Sua senha é: " + senha
        
        # setup the parameters of the message
        password = "yfxrrmlbauwmdnbz"
        msg['From'] = "conhecendoapoli@gmail.com"
        msg['To'] = email
        msg['Subject'] = "OLHA QUE LEGAL!"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()
        
        print ("successfully sent email to %s:" % (msg['To']))