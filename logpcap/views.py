from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math
from cores.convert_json import csv_to_json
from dateutil import parser


def logpcap_view(request):
    return render(request,'logpcap/index.html')

def logpcap_filter(request):
    csvFile = 'attack_ISCX_predictions.csv'
    data_dict = csv_to_json(csvFile)
    
    # Xử lý dữ liệu
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0

    # Xử lý lọc theo khoảng thời gian
    date_range = request.GET.get('dateRange', None)
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y %I:%M %p')
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y %I:%M %p')
        except ValueError:
            return JsonResponse({'error': 'Invalid date range format'}, status=400)

        filtered_data = [item for item in data_dict if start_date <= parser.parse(item['Timestamp']) <= end_date]
        return JsonResponse({'rows': filtered_data}, safe=False)

    # Trả về 100 bản ghi đầu tiên khi không có dateRange
    first_100_items = data_dict[:100]
    return JsonResponse({'total': len(data_dict), 'rows': first_100_items}, safe=False)