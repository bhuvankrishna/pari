from django.conf.urls import url
from django.views.generic import RedirectView

from .views import paintingList, paintingDetail

urlpatterns = [
                       url(r'^painting/$', RedirectView.as_view(url='/categories/painting/', permanent=True)),
                       url(r'^categories/painting/$', paintingList.as_view(), name='painting-list'),
                       url(r'^categories/painting/(?P<alphabet>\w)/$', paintingDetail.as_view(),
                           name='painting-detail'),
                       url(r'^categories/painting/(?P<alphabet>\w)/(?P<slug>[\w\-]+)/$', paintingDetail.as_view(),
                           name='painting-detail-single'),
                       ]
