from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from apps.users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("в разработке")


@method_decorator([csrf_exempt,])
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        print(uploaded_file)
        # Обработка файла (например, сохранение на сервере)
        # В этом примере файл не сохраняется, только возвращается успешное сообщение
        return JsonResponse({"message": "Файл успешно загружен."})
    return render(request, "crm/upload.html")

