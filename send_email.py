# Import smtplib for the actual sending function
from datetime import datetime
import os

import smtplib

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
# 상수
import constant
# 공통 모듈
import common

def send_email(email_to, logfile_path):
    """
    parms - 수신 메일주소
    """
    email_from = constant.C_ADMIN_MAIL_ADDRESS
    email_to = email_to
    email_subject = '[EMWS] 프로세스 수행 결과 공유'

    # email_content = 'Sending an emaiil test'
    email_content_file = open(common.resource_path('html\RESULT_MAIL_TEMPLATE.html'), 'r', encoding='utf8')
    # email_content_file = open(f'{constant.C_ROOT_PATH}\html\RESULT_MAIL_TEMPLATE.html', 'r', encoding='utf8')
    email_content = email_content_file.read()

    # html 내용 수정
    email_content = email_content.replace("PROCESS_NAME", "EMWS").replace("YYYY", datetime.now().strftime('%Y'))


    # Create a text/plain message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject

    body = MIMEText(email_content, 'html', 'utf-8')
    msg.attach(body)

    # 첨부파일 추가
    attach_binary = MIMEBase('application', 'octet-stream')
    binary = open(logfile_path, 'rb').read()
    attach_binary.set_payload(binary)
    encoders.encode_base64(attach_binary)
    attach_binary.add_header('Content-Disposition', 'attachment', filename=os.path.basename(logfile_path))
    msg.attach(attach_binary)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(email_from, 'jtiuflyturrxifpl')
    result = smtp.sendmail(email_from, email_to, msg.as_string())

    # print(msg.as_string())

    smtp.quit()

    return result

# # Import smtplib for the actual sending function
# import smtplib

# # Import the email modules we'll need
# from email.message import EmailMessage

# email_from = 'hyunhee.lee@vntgcorp.com'
# email_to = 'hyunhee.lee@vntgcorp.com'
# email_subject = 'Email Test.'

# email_content = 'Sending an emaiil test'
# # email_content_file = open("./RESULT_MAIL_TEMPLATE.html", 'r', encoding='utf8')
# # email_content = email_content_file.read()

# # Create a text/plain message
# msg = EmailMessage()
# msg.set_content(email_content)
# # From == the sender's email address
# # To == the recipient's email address
# msg['From'] = email_from
# msg['To'] = email_to
# msg['Subject'] = email_subject

# # Send the message via our own SMTP server
# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.starttls()
# smtp.login('hyunhee.lee@vntgcorp.com', 'jtiuflyturrxifpl')
# smtp.send_message(msg)

# print(msg.as_string())

# smtp.quit()
