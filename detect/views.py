from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math,os
from cores.convert_json import csv_to_json
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
from cores.get_latest_file import get_latest_file

def detect_view(request):
    return render(request,'detect/index.html')

def detect_core():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory_path = os.path.join(base_dir, 'data_output', "normal_ISCX_predictions.csv")
    # latest_file = get_latest_file(directory_path)
    # csvFile = 'normal_ISCX_predictions.csv'
    data_dict = csv_to_json(directory_path)
    
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
    # tải file pcap xử lý
    if request.method == 'POST' and 'pcap-file' in request.FILES:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploaded_file = request.FILES['pcap-file']
        save_path = os.path.join(base_dir, 'pcap_log', uploaded_file.name)
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)      
        data = detect_core()
        unique_src_ips = []
        count = 0
        
        for item in data:
            if item["Label"] == '1.0':
                src_ip = item['Dst IP']
                if src_ip not in unique_src_ips:
                    unique_src_ips.append(src_ip)
                    count += 1

    return JsonResponse({'count': count, 'data': data}, safe=False)

@csrf_exempt
def logpcap_filter_time(request):
    data_dict = detect_core()
    # Xử lý dữ liệu
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0
    # Xử lý lọc theo khoảng thời gian
    date_range = request.GET.get('daterange-with-time', None)
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
    count = 0
    for item in data_dict:
        src_ip = item['Src IP']
        if src_ip not in unique_src_ips:
            unique_src_ips.add(src_ip)
            count += 1
    return JsonResponse({'total': count, 'rows': first_100_items}, safe=False)