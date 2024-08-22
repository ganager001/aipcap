from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math
from .convert_json import csv_to_json
from dateutil import parser


def logpcap_view(request):
    return render(request,'logpcap/index.html')

def logpcap_filter(request):
    data_dict = csv_to_json()
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0
    
    date_range = request.GET.get('dateRange', None)
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y %I:%M %p')
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y %I:%M %p')
        except ValueError:
            return JsonResponse({'error': 'Invalid date range format'}, status=400)

        if start_date and end_date:
            data_time = {}
            for item in data_dict:
                time = parser.parse(item['Timestamp'])
                if start_date <= time <= end_date:
                    data_time.append(item)
            return JsonResponse(data_time, safe=False)
    return JsonResponse(data_dict, safe=False)