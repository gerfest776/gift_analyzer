from django.db import models


class Villager(models.Model):
    """Information about villager"""

    citizen_id = models.PositiveIntegerField(verbose_name="Паспортный номер")
    town = models.CharField(max_length=30, verbose_name="Название города")
    street = models.CharField(max_length=50, verbose_name="Улица")
    building = models.CharField(
        max_length=50, verbose_name="Номер дома, корпус и строение"
    )
    apartment = models.PositiveSmallIntegerField(verbose_name="Номер квартиры")
    name = models.CharField(max_length=50, verbose_name="Полное имя")
    birth_date = models.DateField(verbose_name="Дата рождения в формате ДД.ММ.ГГГГ")
    gender = models.CharField(max_length=6, verbose_name="Гендер")
    importer = models.ForeignKey(
        "Importer", on_delete=models.CASCADE, related_name="villagers"
    )
    relatives = models.ManyToManyField("self")

    def __str__(self):
        return f"{self.importer}, citizen_id: {self.citizen_id}, pk: {self.pk}"

    class Meta:
        db_table = "villager"


class Importer(models.Model):
    import_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "importer"
