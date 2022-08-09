from django.conf.urls import url
from .feeds import AllFeed, ArticleFeed, AlbumFeed, \
    FaceFeed, paintingFeed, ResourceFeed, feeds_list_page

urlpatterns = [
    url(r'^list/$', feeds_list_page, name="feeds_list_page"),
    url(r'^all/$', AllFeed(), name="all_feeds"),
    url(r'^articles/$', ArticleFeed(), name="article_feeds"),
    url(r'^albums/$', AlbumFeed(), name="album_feeds"),
    url(r'^faces/$', FaceFeed(), name="face_feeds"),
    url(r'^painting/$', paintingFeed(), name="painting_feeds"),
    url(r'^resources/$', ResourceFeed(), name="resource_feeds"),
]
