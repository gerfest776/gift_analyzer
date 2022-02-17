from collections import Counter
from datetime import date

from django.db import transaction
from rest_framework import serializers

from villagers.models import Importer, Villager


class VillagerSerializer(serializers.ModelSerializer):
    """Villager Serializer which include all model fields"""

    importer = serializers.IntegerField(read_only=True)
    relatives = serializers.ListSerializer(child=serializers.IntegerField())
    birth_date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])

    class Meta:
        model = Villager
        fields = "__all__"
        read_only_fields = ["importer"]


class UPCitizenSerializer(serializers.ModelSerializer):
    """Serializer for patch method imports/<import_id>/citizens"""

    birth_date = serializers.DateField(
        required=False, format="%d.%m.%Y", input_formats=["%d.%m.%Y"]
    )

    class Meta:
        model = Villager
        fields = [
            "citizen_id",
            "town",
            "street",
            "building",
            "apartment",
            "name",
            "birth_date",
            "gender",
            "relatives",
        ]


class PartialSerializer(serializers.ModelSerializer):
    """Serializer for patch method imports/<import_id>/citizens/<citizen_id>"""

    birth_date = serializers.DateField(
        required=False, format="%d.%m.%Y", input_formats=["%d.%m.%Y"]
    )

    class Meta:
        model = Villager
        fields = [
            "town",
            "street",
            "building",
            "apartment",
            "name",
            "birth_date",
            "gender",
            "relatives",
        ]

        extra_kwargs = {
            "town": {"required": False},
            "street": {"required": False},
            "building": {"required": False},
            "apartment": {"required": False},
            "name": {"required": False},
            "gender": {"required": False},
            "relatives": {"required": False},
        }

    def update(self, obj, validated_data):
        obj = obj.villagers.filter(
            citizen_id=self.context["view"].kwargs["citizen_id"]
        ).first()
        if validated_data.get("relatives"):
            relatives = validated_data.pop("relatives")
            obj.relatives.set(relatives)

        for attr, value in validated_data.items():
            setattr(obj, attr, value)
        obj.save()

        return obj


class ImportSerializer(serializers.ModelSerializer):
    """Serializer for post method imports"""

    villagers = VillagerSerializer(many=True, write_only=True)

    class Meta:
        model = Importer
        fields = ["villagers"]

    def create(self, validated_data):
        """
        Checking for relative. If exits - save it in dict and pop from villager in validated data
        Use bulk_create for instant create massive
        """
        relatives = {}
        new_villagers_objs = []

        with transaction.atomic():
            current_import = Importer.objects.create()

            for villager in validated_data["villagers"]:
                relatives[villager["citizen_id"]] = villager.pop("relatives")
                new_villagers_objs.append(Villager(**villager, importer=current_import))

            new_villagers = Villager.objects.bulk_create(new_villagers_objs)

            # Check that if the object has a relative added, then the object is also added for relative.
            for key, values in relatives.items():
                [
                    relatives[item].append(key)
                    for item in values
                    if key not in relatives[item]
                ]

            for villager in new_villagers:
                if relatives[villager.citizen_id]:
                    villager.relatives.set(
                        vlgs.id
                        for vlgs in new_villagers
                        if vlgs.citizen_id in relatives[villager.citizen_id]
                    )
        return current_import

    def to_representation(self, instance):
        response = super(ImportSerializer, self).to_representation(instance)
        response["data"] = {"import_id": instance.import_id}
        return response


class BirthdaySerializer(serializers.ModelSerializer):
    """Serializer for retrieve method citizens/birthdays"""

    data = serializers.SerializerMethodField()

    class Meta:
        model = Importer
        fields = [
            "data",
        ]

    def get_data(self, obj):
        """
        Counter counts number of relatives and append to dict with key in set
        presents - quantity of the same relative in month. citizen_id - their id
        """
        villagers = obj.villagers.prefetch_related("relatives")
        data = {str(i): [] for i in range(1, 13)}

        for villager in villagers:
            for relative in villager.relatives.all():
                data[f"{villager.birth_date.month}"].append(relative.citizen_id)

        for month, month_value in data.items():
            if data[month]:
                count_present = Counter(month_value)
                villagers_and_present = []
                for villager_and_present in set(month_value):
                    presents = count_present[villager_and_present]
                    total_data = {
                        "citizen_id": villager_and_present,
                        "presents": presents,
                    }
                    villagers_and_present.append(total_data)
                data[month] = villagers_and_present
        return data


class PercentileSerializer(serializers.ModelSerializer):
    """Serializer for retrieve method towns/stat/percentile/age"""

    data = serializers.SerializerMethodField()

    class Meta:
        model = Importer
        fields = [
            "data",
        ]

    def get_data(self, obj):
        # check ages in towns. if exists append it. use formula of percentile to values
        villagers = obj.villagers.all()
        data = []
        dates = {}
        for villager in villagers:
            town = villager.town
            age = date.today().year - villager.birth_date.year
            if not dates.get(town):
                dates[town] = [age]
            else:
                dates[town].append(age)
        for town, ages in dates.items():
            data.append(
                {
                    "town": town,
                    "p50": [round(0.5 * len(ages))],
                    "p75": [round(0.75 * len(ages))],
                    "p99": [round(0.99 * len(ages))],
                }
            )
        return data
