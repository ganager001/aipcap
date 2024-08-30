from django.shortcuts import render
from django.http import JsonResponse
import os
import datetime
import pandas as pd
import math
from cores.convert_snort import read_snort
from collections import Counter


def data_snort():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'cores', 'snort.alert.fast')
    snort_list = read_snort(file_path)
    return snort_list

def logsnort_view(request):
    snort_list = data_snort()
    if snort_list is not None:
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['srcip'] for item in snort_list]
        srcport_list = [item['srcport'] for item in snort_list]
        destport_list = [item['destport'] for item in snort_list]
        
        # Đếm số lần xuất hiện của mỗi giá trị
        data = {
            'srcip_count': dict(Counter(srcip_list)),
            'srcport_count': dict(Counter(srcport_list)),
            'destport_count': dict(Counter(destport_list))
        }
        
    return render(request, 'logsnort/index.html',context = {'data':data})

def call_logsnort(request):
    snort_list = data_snort()
    if snort_list is not None:
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['srcip'] for item in snort_list]
        srcport_list = [item['srcport'] for item in snort_list]
        destport_list = [item['destport'] for item in snort_list]

        # Đếm số lần xuất hiện của mỗi giá trị
        srcip_count = Counter(srcip_list)
        srcport_count = Counter(srcport_list)
        destport_count = Counter(destport_list)
        return JsonResponse(snort_list,safe=False)



