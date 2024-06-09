import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from app.forms import UploadFileForm
from .models import Invoice, Total
from django.conf import settings
from . import tasks

def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': invoices})

@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        tasks.process_invoices.delay(file_path)
        return redirect('index')

    totals = Total.objects.all()
    form = UploadFileForm()
    return render(request, 'index.html', {'form': form, 'totals': totals})

# TODO to test
def get_invoice_totals(request):
    totals = Total.objects.values('revenue_source', 'total_value', 'total_advance', 'total_expected_fee')
    return JsonResponse(list(totals), safe=False)

# TODO to test
@csrf_exempt
def post_upload_invoices(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        tasks.process_invoices.delay(file_path)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)