from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math
from cores.convert_json import csv_to_json
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt


def detect_view(request):
    return render(request,'detect/index.html')

def detect_core():
    csvFile = 'normal_ISCX_predictions.csv'
    data_dict = csv_to_json(csvFile)
    
    # Xử lý dữ liệu
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0
    return data_dict

@csrf_exempt
def detect_filter(request):
    if request.method == 'POST' and 'pcap-file' in request.FILES:
        pcapFile = request.FILES['pcap-file']      
        data = detect_core()
        count = sum(1 for item in data if item["Label"] == '1.0')
    return JsonResponse({'count': count, 'data': data}, safe=False)