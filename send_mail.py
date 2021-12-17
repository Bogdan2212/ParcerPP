import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import token
async def send_mail(mail,info):
    try:
        from_email='avitoparser228@gmail.com'
        password=token.password
        msg=MIMEMultipart()
        to_email=mail
        message=f'Товар найден\n{info}.'
        msg['Subject'] = 'Новое объявление'
        msg.attach(MIMEText(message,'plain'))
        server=smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login(from_email,password)
        server.sendmail(from_email,to_email,msg.as_string())
        server.quit()
    except Exception:
        raise Exception