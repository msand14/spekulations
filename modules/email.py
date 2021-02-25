import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from modules.loggingSettings import *

port = 465  # For SSL
context = ssl.create_default_context() # Create a secure SSL context


def setEmailCredentials():

    """
    Check if the credentials already exist in the environment variables
    :return:
    """
    # Note: Its important that the receiver email user, allows less secure apps to ON.
    # Be aware that this makes it easier for others to gain access to your account.
    # More info here: https://realpython.com/python-send-email/

    if not os.getenv('SENDER_EMAIL_USER'):
        os.environ['SENDER_EMAIL_USER'] = input("Enter Email for the sender: ")
    if not os.getenv('EMAIL_PASSWORD'):
        os.environ['EMAIL_PASSWORD'] = input("Enter Email Password: ")
    if not os.getenv('RECEIVER_EMAIL_USER'):
        os.environ['RECEIVER_EMAIL_USER'] = input("Enter the receiver email: ")
    print('Credentials Done!')


def send_email(news, pdfpath: str = ''):
    """
    Method that sends an email to a receiver (with open email to not secure devices)
    :param news: The Stocks news that we include in the email
    :param pdfpath: Location of a PDF. Blank if you dont't want to add any PDF
    :return:
    """
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(os.getenv('SENDER_EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(os.getenv('SENDER_EMAIL_USER'), os.getenv('RECEIVER_EMAIL_USER'),
                        getMessage(news, pdfpath))


# def createPDF(pdfpath: str, name: str):
#    """"
#    :param pdfpath: Location where to save the PDF
#    :param name: Name of the pdf file
#    :return:
#    """

# To do!
# def attachPDF(pdfpath: str):
#    """
#    Includes a PDF into the email
#    :param pdfpath: Location of the PDF
#    :return: MIME Base Object to the email
#    """
#    # Open PDF file in binary mode
#    with open(pdfpath, "rb") as attachment:
#        # Add file as application/octet-stream
#        # Email client can usually download this automatically as attachment
#        part = MIMEBase("application", "octet-stream")
#        part.set_payload(attachment.read())
#        # Encode file in ASCII characters to send by email
#        encoders.encode_base64(part)
#        # Add header as key/value pair to attachment part
#        part.add_header(
#            "Content-Disposition",
#            f"attachment; filename= {pdfpath}", )
#    return part


def getMessage(news: list, pdfpath: str):
    """
    Creates the message of the email
    :param news: The Stocks news that we include in the email
    :param pdfpath: Location of the PDF
    :return: String with message, to be included in the email
    """
    message = MIMEMultipart()
    bodyNews = """"""
    logging.info('Received:' + str(len(news)) + ' news to send by email')
    for new in news:
        logging.info(new[2])
        bodyNews = bodyNews + """
 Company: """ + new[0] + """
 Headline:  """ + new[2] + """
 Time:     """ + new[1] + """
 URL:      """ + new[3] + """\n"""

    subject = 'Some interesting Stocks headlines '
    body = """\
 Dear User,
 We would like to inform you that some news have been written in Media over interresting Stocks: """ + """
                """ + bodyNews + """

We will keep you updated with more news

 Message sent from Python."""
    message["From"] = os.getenv('SENDER_EMAIL_USER')
    message["To"] = os.getenv('RECEIVER_EMAIL_USER')
    message["Subject"] = subject
    # message["Bcc"] = os.getenv('RECEIVER_EMAIL_USER') # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # To implement
    # if pdfpath != '':
    #    part = attachPDF(pdfpath)
    #    # Add attachment to message and convert message to string
    #    message.attach(part)
    text = message.as_string()
    return text
