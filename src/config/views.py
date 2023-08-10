from django.views.generic import TemplateView
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.views import View
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
