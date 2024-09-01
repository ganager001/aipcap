from django.shortcuts import render
import csv
import os









def emailUser_view(request):
    file_path = file_path_email()
    dataEmail = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        
        # Read each row in the CSV file
        for row in reader:
            dataEmail.append(row)
    context = {
        'data_email': dataEmail,

    }
    return render(request, 'email_user/index.html', context)

def file_path_email():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data_output', 'email_user.csv')
    return file_path

def add_contact_to_csv(file_path, name,dayofbirth, email, phone):
    file_path = file_path_email()
    name = 'John Doe'
    dayofbirth = '12/12/1992'
    email = 'john.doe@example.com'
    phone = '123-456-7890'
    # Open the CSV file in append mode ('a')
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the name, email, and phone to the CSV file
        writer.writerow([name,dayofbirth, email, phone])

# Example usage

