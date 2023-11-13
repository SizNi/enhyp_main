from django.views.generic import TemplateView
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import render
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


class MapView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        # Ваши данные из модели Django, содержащие координаты и информацию о маркерах
        markers_data = [
            {"lat": 51.5, "lng": -0.09, "info": "Тут такая инфа"},
            {"lat": 51.505, "lng": -0.1, "info": "А тут другая"},
            {"lat": 51.51, "lng": -0.1, "info": "А тут ее нет"},
            {"lat": 51.505, "lng": -0.09, "info": "А тут и не будет"},
        ]
        return {"markers_data": markers_data}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
