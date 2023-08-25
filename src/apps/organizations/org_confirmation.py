from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone
from apps.organizations.models import Organization


# тут отправляется случайно сгенерированная ссылка для подтверждения почты организации
def org_mail_confirmation(org):
    conf_code = str(uuid.uuid4().hex)[:10]
    org.confirmed = False
    org.confirmation_code = conf_code
    org.confirmation_code_dt = timezone.now()
    org.save()
    message = f"""
            Добрый день, {org.org_name}, для подтверждения адреса перейдите по ссылке:<br>
            <a href="{str(settings.BASE_URL_MAIL) + 'organizations/verification/' + conf_code}">ссылка</a>
            """
    send_mail(
        "Подтверждение почтового адреса",
        f"Добрый день, {org.org_name}, для подтверждения адреса перейдите по ссылке",
        settings.EMAIL_HOST_USER,
        [f"{org.email}"],
        # ["q7j4lypoikqg@mail.ru"],
        fail_silently=False,
        html_message=message,
    )
