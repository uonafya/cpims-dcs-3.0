"""Test email."""
# !/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import settings


def send_email(email, tmsg, hmsg, params):
    """Method to send emails."""
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        fmail = "CPIMS Notification <%s>" % (sender)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = params['subject']
        msg['From'] = fmail
        msg['To'] = email
        if not tmsg:
            tmsg = 'Hello!\nThis is an alternative email. See attachment.'

        part1 = MIMEText(tmsg, 'plain')
        part2 = MIMEText(hmsg, 'html')

        msg.attach(part1)
        msg.attach(part2)

        # Attachment
        if 'attachment' in params:
            a_file = params['attachment']
            a_name = params['doc']
            # print(a_file, type(a_file))
            part = MIMEBase('application', "octet-stream")
            part.set_payload(a_file)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % (a_name))
            msg.attach(part)

        s = smtplib.SMTP(host, port, timeout=5)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, email, msg.as_string())
        s.quit()
        print('Email sent - %s' % (email))
    except Exception as e:
        print('Error sending email - %s' % (str(e)))
    else:
        pass


if __name__ == '__main__':
    pass
    '''
    em = 'nmugaya@gmail.com'
    tm = 'Hello!\nThis is an alternative email. See attachment.'
    report_id = 1
    pd = {}
    params = prepare_data(report_id, pd)
    hm = params['html']
    send_email(em, tm, hm, params)
    print('Email Sent')
    '''
