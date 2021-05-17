from django.urls import path
from .views import urlInput

# http://127.0.0.1/api/
urlpatterns = [
    path('', urlInput, name='urlInput'),
]
