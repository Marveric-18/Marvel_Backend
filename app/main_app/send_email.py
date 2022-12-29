import os
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def send_email(SUBJECT, TO, BODY, ATTACHMENT=[]):
    # SET MESSAGE
    try:
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = os.getenv("SENDER_EMAIL_ADDRESS", "marvsizer018@gmail.com")
        MESSAGE.preamble = ""

        # create HTML_BODY
        HTML_BODY = MIMEText(BODY, 'html')

        MESSAGE.attach(HTML_BODY)

        for attachment in ATTACHMENT:
            # open the file to be sent 
            filename = attachment.split(".")[-2] + attachment.split(".")[-1]
            attachment = open(attachment, "rb")
            
            # instance of MIMEBase and named as p
            ATTACHMENT_BODY = MIMEBase('application', 'octet-stream')
            
            # To change the payload into encoded form
            ATTACHMENT_BODY.set_payload((attachment).read())
            
            # encode into base64
            encoders.encode_base64(ATTACHMENT_BODY)
            
            ATTACHMENT_BODY.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            MESSAGE.attach(ATTACHMENT_BODY)
        
        password = os.getenv("SENDER_EMAIL_ADDRESS_PASSWORD", "marvsizer")
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(MESSAGE['From'],password)
        server.sendmail(MESSAGE['From'], [MESSAGE['To']], MESSAGE.as_string())
        server.quit()
    except Exception as e:
        print("Exception: ", e)
        raise ValueError("Failed to send an email.")