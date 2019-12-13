from django.conf.urls import url
from django.urls import path

from . import views
from .views import IconView, LicenseView, MyIconsView

app_name = 'av_icons'

urlpatterns = [
    path('icons/', IconView.as_view()),
    # Редактирование иконки
    path('icons/<int:pk>', IconView.as_view()),
    # Просмотр текущей лицензии
    path('license/', LicenseView.as_view(), name='license'),
    # Покупка лицензии
    path('new_license/', views.new_license, name='new_license'),
    # Просмотр купленных иконок
    path('my_icons/', MyIconsView.as_view())
]