from django.conf.urls import url
from .views import shorten_url, get_original_url


urlpatterns = [
    url(r'^(?P<unique_id>[-\w]+)/$', get_original_url, name='get_original_url'),
    url('apis/url/create', shorten_url, name='shorten_url')
]
