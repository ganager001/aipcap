from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math,os
from cores.convert_json import csv_to_json
from dateutil import parser
from cores.get_latest_file import get_latest_file


def logpcap_view(request):
    return render(request,'logpcap/index.html')

def logpcap_filter(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory_path = os.path.join(base_dir, 'data_input')
    latest_file = get_latest_file(directory_path, "csv")
    data_dict = csv_to_json(latest_file)
    
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
    first_100_items = data_dict[:1500]

    unique_src_ips = set()
    count = 1
    for item in data_dict:
        src_ip = item['Src IP']
        if src_ip not in unique_src_ips:
            unique_src_ips.add(src_ip)
            count += 1
    return JsonResponse({'total': count, 'rows': first_100_items}, safe=False)