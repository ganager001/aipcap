import os
import glob

def get_latest_file(directory, file_extension="*"):
   
    # Tạo đường dẫn với phần mở rộng file
    search_pattern = os.path.join(directory, f"*.{file_extension}")
    
    # Lấy danh sách tất cả các file trong thư mục với phần mở rộng đã cho
    list_of_files = glob.glob(search_pattern)
    
    if not list_of_files:
        return None
    
    # Tìm file mới nhất dựa trên thời gian chỉnh sửa cuối cùng
    latest_file = max(list_of_files, key=os.path.getmtime)
    
    return latest_file

# Sử dụng hàm
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# directory_path = os.path.join(base_dir, 'data_input')
# latest_file = get_latest_file(directory_path, "csv")
# print(f"File mới nhất: {latest_file}")
