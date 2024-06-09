import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from app.forms import UploadFileForm
from .models import Invoice, Total
from .ingestion import ingest_excel
from django.conf import settings

# TODO to test
def get_invoice_totals(request):
    totals = Total.objects.values('revenue_source', 'total_value', 'total_advance', 'total_expected_fee')
    return JsonResponse(list(totals), safe=False)

# TODO to test
def invoice_totals(request):
    totals = Total.objects.values('revenue_source', 'total_value', 'total_advance', 'total_expected_fee')
    return render(request, 'invoice_totals.html', {'totals': totals})

@csrf_exempt
def post_upload_invoices(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        ingest_excel(file_path)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
def upload_invoices(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        ingest_excel(file_path)
        return redirect('invoice_totals')
    else:
        form = UploadFileForm()
    return render(request, 'upload_invoices.html', {'form': form})
