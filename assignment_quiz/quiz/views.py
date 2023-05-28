from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q, F
import collections
from rest_framework import permissions
from rest_framework.serializers import Serializer
from django.db.models.functions import Concat
import requests
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Q, Sum, Subquery, OuterRef, FloatField, Exists, Value, CharField
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from datetime import datetime, timedelta, timezone
from quiz.models import *
from quiz import serializers
from quiz.custom_authentication import PreSharedPermissionForQuiz
from custom_decorator import response_modify_decorator_list_or_get_after_execution_for_onoff_pagination, response_modify_decorator_get
from pagination import OnOffPagination
                              
# Create your views here.

class QuizQuestionAddView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = QuizCreation.objects.all()
    serializer_class = serializers.QuizQuestionAddSerializer

class QuizQuestionListView(APIView):
    permission_classes = [AllowAny]
    queryset = QuizCreation.objects.all().values()
    pagination_class = OnOffPagination

    def get_filter(self):
        queryset = self.queryset
        status = self.request.query_params.get('status', None)
        if status:
            queryset=queryset.filter(status__iexact=status)
        return queryset

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        # return Response1    
        count = self.request.query_params.get('count')

        # Pagination Functionalityresponse_modify_decorator_get
        paginator = OnOffPagination()
        page_size = self.request.GET['page_size']

        # Filter
        self.queryset = self.get_filter()
        
        if page_size == '0':
            response = self.queryset
            if count:
                count = len(response)
                return Response({'total_count': count})
        else:
            result_page = paginator.paginate_queryset(self.queryset, request)
            response = paginator.get_paginated_response(result_page)
            response = response.data
        return Response(response)

class QuizQuestionRightAnswerView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = QuizCreation.objects.all().values()

    def get(self, request, *args, **kwargs):
        question = self.request.query_params.get('question', None)
        if question:
            question_no = QuizCreation.objects.filter(id=question).first().options
            for each in question_no.keys():
                if int(each)==QuizCreation.objects.filter(id=question).first().right_answer:
                    answer = "The right answer is: " + question_no[each] 
                    return Response(answer)
        return super().get(request, *args, **kwargs)

class QuizStatusAutoUpdationView(APIView):
    # permission_classes = [PreSharedPermissionForQuiz]
    permission_classes = [AllowAny,]
    
    def get(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                current_datetime = datetime.now()
                all_quiz_list = list(QuizCreation.objects.values_list('id', flat=True))
                if all_quiz_list:
                     for each_quiz in all_quiz_list:
                        start_time_of_each_quiz = QuizCreation.objects.filter(id=each_quiz).first().start_date
                        end_time_of_each_quiz = QuizCreation.objects.filter(id=each_quiz).first().end_date

                        if start_time_of_each_quiz <= current_datetime and end_time_of_each_quiz <= current_datetime:
                            updation = QuizCreation.objects.filter(id=each_quiz).update(
                                    status='Finished'
                            )
                        if start_time_of_each_quiz >= current_datetime:
                            updation = QuizCreation.objects.filter(id=each_quiz).update(
                                    status='Inactive'
                            )
                        if start_time_of_each_quiz <= current_datetime and end_time_of_each_quiz >= current_datetime:
                            updation = QuizCreation.objects.filter(id=each_quiz).update(
                                    status='Active'
                            )
            msg = "Updation Successful"  
            return Response({'result':{"code":200,'result':msg}})
        except Exception as e:
            raise e
                        