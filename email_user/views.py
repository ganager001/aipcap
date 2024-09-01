from django.shortcuts import render,redirect
import csv
import os
from django.contrib import messages

def save_email(request):
    if request.method == "POST":
        name = request.POST.get('input-fullname')
        birthday = request.POST.get('input-birthday')
        email = request.POST.get('input-email')
        phone = request.POST.get('input-phone')
        file_path = file_path_email()
        add_contact_to_csv(file_path, name, birthday, email, phone)
        messages.success(request, 'Thêm dữ liệu Email thành công!')
        return redirect('emailUser')


def emailUser_view(request):
    file_path = file_path_email()
    dataEmail = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        
        # Read each row in the CSV file
        for row in reader:
            if len(row)>0:
                item = {
                    'name': row[0],
                    'birthday': row[1],
                    'email': row[2],
                    'phone': row[3]
                }
                dataEmail.append(item)
    context = {
        'data_email': dataEmail,

    }
    return render(request, 'email_user/index.html', context)


def file_path_email():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data_output', 'email_user.csv')
    return file_path


def add_contact_to_csv(file_path, name,dayofbirth, email, phone):
    # Open the CSV file in append mode ('a')
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the name, email, and phone to the CSV file
        writer.writerow([name,dayofbirth, email, phone])