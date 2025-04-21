import json
import os
from django.core.management.base import BaseCommand
from users.models import Payment, User


class Command(BaseCommand):
    help = 'Create a user and payment data, then save it to a JSON file'

    def handle(self, *args, **options):
        params = dict(email="test@example.com", password="qwerty")
        user, user_status = User.objects.get_or_create(**params)

        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("User created successfully."))

        payments_data = [
            {
                "owner": user,  # Передаем сам объект User
                "payment_date": "2023-10-01",
                "paid_course_id": 5,
                "paid_lesson_id": None,
                "amount": 100.00,
                "type": "CASH",
            },
            {
                "owner": user,  # Передаем сам объект User
                "payment_date": "2023-10-02",
                "paid_course_id": None,
                "paid_lesson_id": 15,
                "amount": 150.00,
                "type": "BANK_TRANSFER",
            }
        ]

        # Сохранение платежей в базе данных
        for payment in payments_data:
            Payment.objects.create(**payment)

        # Подготовка данных для записи в JSON
        output_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            },
            'payments': [
                {
                    'owner_id': payment['owner'].id,  # Сохраняем только ID пользователя для JSON
                    'payment_date': payment['payment_date'],
                    'paid_course_id': payment['paid_course_id'],
                    'paid_lesson_id': payment['paid_lesson_id'],
                    'amount': payment['amount'],
                    'type': payment['type'],
                }
                for payment in payments_data
            ]
        }

        # Укажите полный путь к файлу или используйте os.path.join для создания файла в нужной директории
        json_file_path = os.path.join(os.getcwd(), 'payments_data.json')

        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(output_data, json_file, indent=4)
            self.stdout.write(self.style.SUCCESS(f"Данные о платежах успешно загружены и сохранены в {json_file_path}!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при записи файла: {e}"))