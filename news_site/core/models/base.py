from django.db.models import Model, DateTimeField, Index


class AbstractDateTime(Model):
    """
    Абстрактная модель, предоставляющая поля даты и времени для отслеживания времени создания
    и последнего обновления объекта.
    """

    datetime_created = DateTimeField("Время создания", auto_now_add=True)
    datetime_updated = DateTimeField("Время обновления", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-datetime_created"]

        indexes = [Index(fields=["datetime_created"]), Index(fields=["datetime_updated"])]
