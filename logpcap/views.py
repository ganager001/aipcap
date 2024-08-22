from django.shortcuts import render
from django.http import JsonResponse
import csv,os
import datetime
import pandas as pd
import math


def formatTime(time):
    formatted_time = datetime.datetime.fromtimestamp(float(time))
    time_resual = formatted_time.strftime('%d-%m-%Y %H:%M:%S')
    return time_resual

def loadData():
    arr_data = []
    with open('output/data_output.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            row[00] = formatTime(row[00])
            arr_data.append(row)
    return arr_data


def logpcap_view(request):
    return render(request,'logpcap/index.html')

def logpcap_filter(request):
    # Đường dẫn đến file CSV của bạn
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(base_dir, 'output', 'attack_ISCX_predictions.csv')

    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": "File không tồn tại"}, status=404)

    try:
        # Đọc dữ liệu từ file CSV
        data = pd.read_csv(csv_file_path)

        # Kiểm tra nếu file CSV trống
        if data.empty:
            return JsonResponse([], safe=False)
        date_range = request.GET.get('dateRange', None)
        if date_range:
            try:
                start_date_str, end_date_str = date_range.split(' - ')
                start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y %I:%M %p')
                end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%Y %I:%M %p')
            except ValueError:
                return JsonResponse({'error': 'Invalid date range format'}, status=400)

        if start_date and end_date:
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')  # Giả sử cột thời gian trong CSV là 'time'
            data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]

        # Chuyển dữ liệu sang dạng danh sách từ điển
        data_dict = data.to_dict(orient='records')
        for item in data_dict:
            for key, value in item.items():
                if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                    item[key] = None
                elif isinstance(value, int) and (value < 0):
                    item[key] = 0
        # Trả dữ liệu về dưới dạng JSON
        return JsonResponse(data_dict, safe=False)

    except pd.errors.EmptyDataError:
        return JsonResponse({"error": "File không tồn tại"})

    except Exception as e:
        # Xử lý các ngoại lệ khác
        return JsonResponse({"error": "File không tồn tại"})


