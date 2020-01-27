from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^api/v1/logs/(?P<pk>[0-9]+)$', # Url to get update logs
        views.get_update_log.as_view(),

    ),
    path('api/v1/logs/', # urls list all and create new one
        views.get_post_logs.as_view(),
        name='get_post_logs'
    )
]