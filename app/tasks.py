from celery import shared_task
from .ingestion import ingest_excel

@shared_task
def process_invoices(file_path):
    ingest_excel(file_path)
