import datetime
from celery import shared_task
from users.models import User


@shared_task
def my_task():
    """
    Проверка пользователей по дате последнего входа и, если пользователь не заходил более месяца, блокировка его.
    """
    users = User.objects.all()
    today = datetime.date.today()
    deactivate_time = datetime.timedelta(days=30)
    for user in users:
        if today - user.last_login > deactivate_time:
            user.is_active = False
            print(f'{user} отключен')
            user.save()