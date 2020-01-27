from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import StatusLog
from .serializers import LogsSerializer

import logging
import re

from django.http import HttpResponse

logger = logging.getLogger('db')


def file_view(start=None, end=None, level=None):
    logs = [line  for line in open("filename", "r")]
    filtered_logs = []
    for log in logs:
        split_strings = log.split(' ')
        timestamp = split_strings[0]
        if level:
            if re.match(r'{}'.format(level), log):
                filtered_logs.append(log)
        if start:
            if int(timestamp) >= start and int(timestamp) <= end:
                filtered_logs.append(log)
        else:
            return logs
    return filtered_logs


class get_update_log(RetrieveUpdateDestroyAPIView):
    serializer_class = LogsSerializer

    def get_queryset(self, request , pk, **kwargs):

        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        log_level = self.request.query_params.get('level')
        storage_type = self.request.query_params.get('storage')
        if storage_type == 'file_system':
            if date_from:
                log = file_view(start=date_from, end=date_to)
            elif log_level:
                file_view(level=log_level)

        elif storage_type == 'database':

            try:
                log = StatusLog.objects.get(pk=pk)
            except StatusLog.DoesNotExist:
                content = {
                    'status': 'Not Found'
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return log

    # Get a Logs
    def get(self, request, pk):

        log = self.get_queryset(pk)
        serializer = LogsSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update Logs
    def put(self, request, pk):

        movie = self.get_queryset(pk)

        if (request.user == movie.creator):  # If creator is who makes request
            serializer = LogsSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class get_post_logs(ListCreateAPIView):
    serializer_class = LogsSerializer


    def get_queryset(self):
        logs = StatusLog.objects.all()
        return logs

    # Get all logs
    def get(self, request):
        logs = self.get_queryset()
        paginate_queryset = self.paginate_queryset(logs)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    # Create a new Log
    def post(self, request):
        serializer = LogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)