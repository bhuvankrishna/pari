from django.conf.urls import url
from django.views.generic import RedirectView


urlpatterns = [
                       url(r'^paintings/$', RedirectView.as_view(url='/categories/paintings/', permanent=True)),
                       ]
