import copy
import json
from django.http import request
from rest_framework import serializers
from quiz.models import *
import numpy as np
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, F, Sum
from rest_framework.exceptions import APIException
from rest_framework.fields import IntegerField, FileField
from rest_framework.serializers import (ModelSerializer, Serializer, SerializerMethodField, CurrentUserDefault, CharField,
                                        ListField, BooleanField)
from datetime import datetime, timedelta
from django.db.models import F


class QuizQuestionAddSerializer(ModelSerializer):
    # created_by = CharField(default=CurrentUserDefault())

    class Meta:
        model = QuizCreation
        fields = '__all__'
    
    def create(self, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        current_date = datetime.now()
        creation = QuizCreation.objects.create(**validated_data)
        if start_date >= current_date:
            updation = QuizCreation.objects.filter(id=creation.id).update(
                        status='Inactive'
                            )
        if start_date <= current_date and end_date >= current_date:
            updation = QuizCreation.objects.filter(id=creation.id).update(
                        status='Active'
                            )
        validated_data['id'] = creation.id
        return validated_data
        # return super().create(validated_data)