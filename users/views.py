import jsonn
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render


class MainView(View):
    def get(self, request):
        return JsonResponse({"Hello": "World"}, status=200)
