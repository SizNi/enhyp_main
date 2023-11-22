from django.views.generic import TemplateView
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import os


class Index(TemplateView):
    template_name = "index.html"


class PassportExampleView(View):
    def get(self, request, *args, **kwargs):
        pdf_path = os.path.join(settings.MEDIA_ROOT, "geology/well_passport.pdf")
        if os.path.exists(pdf_path):
            print(pdf_path)
            return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
        else:
            return HttpResponse("PDF not found", status=404)


class MapView_1(TemplateView):
    template_name = "map_1.html"

    def get_context_data(self, **kwargs):
        # Ваши данные из модели Django, содержащие координаты и информацию о маркерах
        markers_data = [
            {"lat": 51.5, "lng": -0.09, "info": "Тут такая инфа", "param": "J"},
            {"lat": 51.505, "lng": -0.1, "info": "А тут другая", "param": "C"},
            {"lat": 51.51, "lng": -0.1, "info": "А тут ее нет", "param": "C"},
            {"lat": 51.505, "lng": -0.09, "info": "А тут и не будет", "param": "Q"},
        ]
        return {"markers_data": markers_data}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class PointsView(View):
    def get(self, request, *args, **kwargs):
        file_path = (
            "static/map_2/points.geojson"  # Замените на реальный путь к вашему файлу
        )
        with open(file_path, "rb") as f:
            geojson_data = json.load(f)

        return JsonResponse(geojson_data, safe=False)


class MapView_2(TemplateView):
    template_name = "map_2.html"

    def get_context_data(self, **kwargs):
        # Ваши данные из модели Django, содержащие координаты и информацию о маркерах
        markers_data = [
            {"lat": 51.5, "lng": -0.09, "info": "Тут такая инфа", "param": "J"},
            {"lat": 51.505, "lng": -0.1, "info": "А тут другая", "param": "C"},
            {"lat": 51.51, "lng": -0.1, "info": "А тут ее нет", "param": "C"},
            {"lat": 51.505, "lng": -0.09, "info": "А тут и не будет", "param": "Q"},
        ]
        return {"markers_data": markers_data}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class MapView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        # Ваши данные из модели Django, содержащие координаты и информацию о маркерах
        markers_data = [
            {"lat": 51.5, "lng": -0.09, "info": "Тут такая инфа", "param": "J"},
            {"lat": 51.505, "lng": -0.1, "info": "А тут другая", "param": "C"},
            {"lat": 51.51, "lng": -0.1, "info": "А тут ее нет", "param": "C"},
            {"lat": 51.505, "lng": -0.09, "info": "А тут и не будет", "param": "Q"},
        ]
        return {"markers_data": markers_data}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
