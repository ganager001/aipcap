import csv
import json
import os
from django.http import JsonResponse


def csv_to_json(csv_file_path):

    if not os.path.exists(csv_file_path):
            return JsonResponse({"error": "File không tồn tại"}, status=404)
    # Mở file CSV và đọc nội dung
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Chuyển dữ liệu từ CSV sang danh sách các dictionary
        data_json = [row for row in csv_reader]
    return data_json

