
import os
import pandas as pd
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
from .models import Invoice, Total
from . import tasks

REQUIRED_COLUMNS = [
    'date',
    'invoice number',
    'value',
    'haircut percent',
    'Daily fee percent',
    'currency',
    'Revenue source',
    'customer',
    'Expected payment duration'
]

@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            df = pd.read_excel(file_path)
            if not all(column in df.columns for column in REQUIRED_COLUMNS):
                return JsonResponse({'status': 'fail', 'message': 'File is missing required columns.'}, status=400)
        except Exception:
            return JsonResponse({'status': 'fail', 'message': 'File is not readable or not in correct format.'}, status=400)

        tasks.process_invoices.delay(file_path)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail', 'message': 'No file provided.'}, status=400)


def get_invoice_totals(request):
    totals = Total.objects.values('revenue_source', 'total_value', 'total_advance', 'total_expected_fee')

    if totals.exists():
        return JsonResponse(list(totals), safe=False)

    return JsonResponse({'status': 'fail'}, status=400)


def load_invoices(request):
    page_number = request.GET.get('page', 1)
    invoices_list = Invoice.objects.all().order_by('-id')
    paginator = Paginator(invoices_list, 20)
    page_obj = paginator.get_page(page_number)

    if page_obj.object_list.exists():
        data = {
            'invoices': list(page_obj.object_list.values()),
            'has_previous': page_obj.has_previous(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'has_next': page_obj.has_next(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'num_pages': page_obj.paginator.num_pages,
            'current_page': page_obj.number,
        }
        return JsonResponse(data, safe=False)

    return JsonResponse({'status': 'fail'}, status=400)
