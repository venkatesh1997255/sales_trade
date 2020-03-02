# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python Imports

# Third Party Imports

# DRF Imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Django Imports
from django.db.models import F, Avg, Min, Max
from django.db.models.functions import TruncMonth

# Local Imports
from salesapp.models import Sales
from salesapp.serializers import (
    SalesSerializer,
    BulkUploadSerializer,
    DateStampSerializer,
)
from salesapp.services import upload_sales_from_url


class TradedViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    @action(detail=False, methods=["POST"])
    def bulk_upload(self, request):
        """
        :param request:Creates the data and inserts into the database
        :return:displays the message successful if data is dump else error message
        """
        serializer = BulkUploadSerializer(data=request.data)
        if serializer.is_valid():
            upload_sales_from_url(url=serializer.validated_data["source"])
            return Response({"message": "Successfully uploaded the data."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def high_trade(self, request):
        """
        :param request: request from the user
        :return: traded turnover in mentioned dates
        """
        serializer = DateStampSerializer(data=request.data)
        if serializer.is_valid():
            query_set = Sales.objects.filter(date__range=(serializer.validated_data["start_date"],
                                                          serializer.validated_data["end_date"]),
                                             open__gt=F('close'))
            return Response(SalesSerializer(query_set, many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def avg_turnover(self, request):
        """
        :param request:request from the user
        :return: difference of the high and low prices in mentioned dates
        """
        serializer = DateStampSerializer(data=request.data)
        if serializer.is_valid():
            query_set = Sales.objects.filter(date__range=(
                serializer.validated_data["start_date"], serializer.validated_data["end_date"])) \
                .aggregate(turn_over=Avg('turnover'))
            return Response({"turnover": query_set["turn_over"]})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def avg_diff_high_low(self, request):
        """
        :param request:request from the user44444
        :return: difference avg high and low prices
        """
        serializer = DateStampSerializer(data=request.data)
        if serializer.is_valid():
            query_set = Sales.objects.filter(date__range=(
                serializer.validated_data["start_date"], serializer.validated_data["end_date"])) \
                .aggregate(high=Avg('high'),low=Avg('low'))
            return Response({"high": query_set["high"],"low": query_set["low"],
                             "difference":query_set["high"]-query_set["low"]})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def avg_open_close(self, request):
        """
        :param request:request from user
        :return: Month wise average of the open and close price
        """
        query_set = Sales.objects.annotate(month=TruncMonth('date')).values('month') \
            .annotate(avg_open_price=Avg('open'), avg_close_price=Avg('close'))[:10:]
        return Response(query_set)

    @action(detail=False, methods=["GET"])
    def aggregate_turnover(self, request):
        """
        :param request: request from user
        :return:Day name wise Turnover (Rs. Cr)'s average, minimum, maximum
        """
        query_set = Sales.objects.values('date') \
            .annotate(min_turnover=Min('open'), max_turnover=Max('close'), avg_turnover=Avg('turnover'))
        return Response(query_set)

    @action(detail=False, methods=["GET"])
    def volatility_records(self, request):
        """
        :param request: request from user
        :return: complete negative volatility for daywise
        """
        query_set = Sales.objects.filter(open=F('high')).annotate(diff_high_low=F('high') - F('low'))
        return Response(query_set.values('date', 'open', 'high', 'low', 'diff_high_low', 'turnover'))
