# tasks.py
from celery import shared_task
from decouple import config
from email.mime.text import MIMEText
import smtplib

@shared_task
def process_invoices(file_path):
    from .ingestion import ingest_excel
    ingest_excel(file_path)

@shared_task
def send_remainder_emails(email_addresses):
    email_body = '<p>Reminder: Please upload your invoices for this month.</p>'
    remittent_email = config('REMITTENT_EMAIL')
    remittent_password = config('REMITTENT_PASSWORD')

    for customer_email_address in email_addresses:
        message = MIMEText(email_body, 'html')
        message['Subject'] = 'Monthly Reminder: Upload Invoices'
        message['From'] = remittent_email
        message['To'] = customer_email_address

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(remittent_email, remittent_password)
            server.sendmail(remittent_email, customer_email_address, message.as_string())
            server.quit()
        except Exception as error:
            print(f'Error sending the email to {customer_email_address}: {error}')
            return False
     
    print("Emails have been processed.")   
    return True
    
    # for customer_email_address in email_addresses:
    
    #     message['To'] = customer_email_address
        
    #     try:
    #         server = smtplib.SMTP('smtp.gmail.com:587')
    #         server.ehlo()
    #         server.starttls()
    #         server.login(remittent_email, remittent_password)
            
    #         server.sendmail(
    #             remittent_email, 
    #             customer_email_address, 
    #             message.as_string()
    #         )
            
    #         server.quit()
    #         return True
        
    #     except Exception as error:
    #         print('Error sending the email, {error}')
    #         return False;   
