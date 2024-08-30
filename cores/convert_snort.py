import re

def read_snort(file_name):
    key_list = []
    value_list = []
    snort_list = []

    with open(file_name, 'r') as f:
        start_line = f.readlines()

    for i in start_line:
        # Sử dụng biểu thức chính quy để tách thời gian và sự kiện
        x = re.search(r'^((?:\d{2}[-\/:.]){5}\d{6})(.*{TCP}|.*{UDP}|.*{ICMP})\s*(.*)', i)
        if not x:
            continue  # Bỏ qua dòng nếu không khớp

        date_time = x.group(1)
        event = x.group(2).lstrip()
        ip_info = x.group(3)

        key_list.append("time")
        value_list.append(date_time)

        if "{ICMP}" in event:
            icmp_formatted = re.search(r'((?:\d{1,3}\.){3}\d{1,3})\s*->\s*((?:\d{1,3}\.){3}\d{1,3})', ip_info)
            if not icmp_formatted:
                continue

            icmp_src_ip = icmp_formatted.group(1)
            icmp_dest_ip = icmp_formatted.group(2)

            key_list.extend(["srcip", "srcport", "destip", "destport"])
            value_list.extend([icmp_src_ip, "none", icmp_dest_ip, "none"])

        elif "{TCP}" in event or "{UDP}" in event:
            ip_formatted = re.search(r'((?:\d{1,3}\.){3}\d{1,3}):(\d{1,6})\s*->\s*((?:\d{1,3}\.){3}\d{1,3}):(\d{1,6})', ip_info)
            if not ip_formatted:
                continue

            src_ip = ip_formatted.group(1)
            src_port = ip_formatted.group(2)
            dest_ip = ip_formatted.group(3)
            dest_port = ip_formatted.group(4)

            key_list.extend(["srcip", "srcport", "destip", "destport"])
            value_list.extend([src_ip, src_port, dest_ip, dest_port])

        # Lấy mô tả sự kiện và phân loại
        get_event_desc = re.search(r'(\[\*\*\].*?\[\*\*\])\s*(.*?\[Classification:.*?\])', event)
        if get_event_desc:
            event_desc = get_event_desc.group(1).strip()
            classification = get_event_desc.group(2).split('[Classification:')[1].strip(']')

            key_list.extend(["event", "classification"])
            value_list.extend([event_desc, classification])

        # Lưu trữ các cặp key-value vào danh sách
        snort_list.append(dict(zip(key_list, value_list)))

        # Reset key_list và value_list cho lần lặp tiếp theo
        key_list.clear()
        value_list.clear()

    return snort_list


