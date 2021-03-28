from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .forms import MyForm
from .itvps_lab_3 import add_to_csv


def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            file_name = form.cleaned_data.get("file")
            add_to_csv("/Users/daana/Projects/SEMESTR_6/ITvPS/itvps_lab_3/news/"+file_name,
                       "/Users/daana/Projects/SEMESTR_6/ITvPS/itvps_lab_3/itvps_lab_3_db")
    else:
        form = MyForm()
    return render(request, 'main/index.html', {'form': form})


# запуск : python3 manage.py runserver
