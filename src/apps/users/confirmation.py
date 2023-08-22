from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone
from apps.users.models import CustomUser


# тут отправляется случайно сгенерированная ссылка для подтверждения почты пользователя
def mail_confirmation(user):
    conf_code = str(uuid.uuid4().hex)[:10]
    user.confirmation_code = conf_code
    user.confirmation_code_dt = timezone.now()
    user.save()
    print({str(settings.BASE_URL_MAIL) + conf_code})
    message = f"""
            Добрый день, {user.username}, для подтверждения адреса перейдите по ссылке:<br>
            <a href="{str(settings.BASE_URL_MAIL) + conf_code}">ссылка</a>
            """
    send_mail(
        "Подтверждение почтового адреса",
        f"Добрый день, {user.username}, для подтверждения адреса перейдите по ссылке",
        settings.EMAIL_HOST_USER,
        [f"{user.email}"],
        # ["q7j4lypoikqg@mail.ru"],
        fail_silently=False,
        html_message=message,
    )