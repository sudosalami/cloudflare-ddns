import smtplib
from email.mime.text import MIMEText
from auth import EMAIL_USER, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT


class Email:
    def __init__(self):
        self.smtp_server = EMAIL_SERVER
        self.smtp_port = EMAIL_PORT
        self.sender = EMAIL_USER
        self.recipient = EMAIL_USER
        self.password = EMAIL_PASSWORD
    

    def send_email(self, subject, body):
        email_variables = EMAIL_USER, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT
        not_empty = [var for var in email_variables if var != '']
        if not_empty:
            self.subject = subject
            self.body = body
            msg = MIMEText(self.body)
            msg['Subject'] = self.subject
            msg['From'] = self.sender
            msg['To'] = self.recipient
            smtp_server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, self.recipient, msg.as_string())
            smtp_server.quit()
        else:
            print('insufficient information to send an email')


    def new_info(self, old, new):
        subject = "IP Address change"
        body = f"""Your IP Address changed, which triggered this email.\n
        What do I have to do?
        Nothing. Records being managed by this program are being automatically updated with the new information.\n
        Previous IP Address: {old}
        New IP Address: {new}\n
        If this email has incorrect information, verify that your host instance is running properly and that custom records are configured properly."""

        Email.send_email(self, subject, body)
    

    def bad_api(self, api):
        subject = ""
        body = f"""The APIs used to get your public IP address have failed for over 24 hours.\n
        What do I have to do?
        Verify that your host instance can reach the internet and that these urls are accessible:
        {api[0]}
        {api[1]}
        {api[2]}\n
        If your IP address changes during this time your applications could stop working.
        """
        
        Email.send_email(self, subject, body)