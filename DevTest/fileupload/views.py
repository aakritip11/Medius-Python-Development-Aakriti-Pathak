# fileupload/views.py
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import UploadFileForm

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                return HttpResponse("Unsupported file type.")

            # Selecting only the relevant columns
            df = df[['Cust State', 'Cust Pin', 'DPD']]  # Keep only the desired columns
            
            # Renaming columns if necessary (adjust if the original names are different)
            df.columns = ['Cust State', 'Cust Pin', 'DPD']  
            
            # Creating a formatted HTML table
            data_preview = df.to_html(index=False, classes='table table-striped', border=0)  # You can customize classes
            
            return render(request, 'fileupload/upload_success.html', {'data': data_preview})
    else:
        form = UploadFileForm()
    
    return render(request, 'fileupload/upload.html', {'form': form})
