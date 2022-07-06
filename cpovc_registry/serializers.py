from rest_framework import serializers
from .models import RegOrgUnit, RegPerson
from django.contrib.auth.models import User


class RegPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegPerson
        fields = ['first_name', 'designation', 'other_names', 'id', 'surname']
