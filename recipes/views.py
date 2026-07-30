from django.shortcuts import render
from django.http import HttpResponse


def test_view(request):
    return render(
        request,
        'recipes/pages/home.html',
    )
