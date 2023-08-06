from django.urls import path
from django.conf.urls import url

from . import views


app_name = "buybacks"

urlpatterns = [
    path("", views.index, name="index"),
    path("setup", views.setup, name="setup"),
    url(
        r"^item_autocomplete/$",
        views.item_autocomplete,
        name="item_autocomplete",
    ),
    path("my_notifications", views.my_notifications, name="my_notifications"),
    path("my_stats", views.my_stats, name="my_stats"),
    url(
        r"^notification/(?P<notification_pk>[0-9]+)/remove$",
        views.notification_remove,
        name="notification_remove",
    ),
    url(
        r"^notification/(?P<notification_pk>[0-9]+)/edit$",
        views.notification_edit,
        name="notification_edit",
    ),
    path("program_add", views.program_add, name="program_add"),
    path("program_add_2", views.program_add_2, name="program_add_2"),
    url(
        r"^program/(?P<program_pk>[0-9]+)/edit$",
        views.program_edit,
        name="program_edit",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)$",
        views.program,
        name="program",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/remove$",
        views.program_remove,
        name="program_remove",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/calculate$",
        views.program_calculate,
        name="program_calculate",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/stats$",
        views.program_stats,
        name="program_stats",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/notify$",
        views.program_notify,
        name="program_notify",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/notifications$",
        views.program_notifications,
        name="program_notifications",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/add_item$",
        views.program_add_item,
        name="program_add_item",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/add_location$",
        views.program_add_location,
        name="program_add_location",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/remove_item/(?P<item_type_pk>[0-9]+)$",
        views.program_remove_item,
        name="program_remove_item",
    ),
    url(
        r"^program/(?P<program_pk>[0-9]+)/remove_location/(?P<office_pk>[0-9]+)$",
        views.program_remove_location,
        name="program_remove_location",
    ),
]
