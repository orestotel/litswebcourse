from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from .models import NewsItem
from .serializers import NewsItemSerializer


class NewsList(ListView):
    model = NewsItem

@csrf_exempt
def api_news_list(request):
    if request.method == 'GET':
        items = NewsItem.objects.all().order_by('-date')
        serializer = NewsItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NewsItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, staus=400)

@csrf_exempt
def api_news_detail(request, id):
    if request.method == 'GET':
        item = NewsItem.objects.get(id=id)
        serializer = NewsItemSerializer(item)
        return JsonResponse(serializer.data, safe=False)