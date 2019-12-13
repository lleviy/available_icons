from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LicenseForm
from .models import Icon, License

from .serializers import IconSerializer, LicensedIconSerializer, LicenseSerializer

from django.contrib.auth.models import User, Group


class MyIconsView(APIView):
    """Класс для представления купленных пользователем иконок"""
    def get(self, request):
        my_icons = Icon.objects.filter(buyers=request.user)
        serializer = LicensedIconSerializer(my_icons, many=True)
        return Response({"my icons": serializer.data})


class LicenseView(APIView):
    """Класс для представления лицензии, приобретенной пользователем"""
    def get(self, request):
        checking_for_end_of_license(request)
        license = License.objects.filter(owner=request.user)
        serializer = LicenseSerializer(license, many=True)
        return Response({"License": serializer.data})


class IconView(APIView):
    """Класс для представления всех имеющихся на сайте иконок"""
    def get(self, request):
        icons = Icon.objects.all()
        licensed_users = Group.objects.get(name="licensed").user_set.all()
        basic_icons = Icon.objects.filter(category='basic')
        basic_serializer = LicensedIconSerializer(basic_icons, many=True)
        if request.user.is_authenticated:
            checking_for_end_of_license(request)
            my_icons = Icon.objects.filter(buyers=request.user)
            my_icons_serializer = LicensedIconSerializer(my_icons, many=True)
        if request.user not in licensed_users:
            serializer = IconSerializer(icons.exclude(category='basic').exclude(buyers=request.user), many=True)
        else:
            serializer = LicensedIconSerializer(icons.exclude(category='basic'), many=True)
        return Response({"my icons:": my_icons_serializer.data, "icons": serializer.data, "basic_icons": basic_serializer.data})

    def post(self, request):
        icon = request.data.get('icon')
        serializer = IconSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            icon_saved = serializer.save()
        return Response({"success": "Icon '{}' created successfully".format(icon_saved.name)})

    def put(self, request, pk):
        saved_icon = get_object_or_404(Icon.objects.all(), pk=pk)
        # data = request.data.get('icon')
        serializer = IconSerializer(instance=saved_icon, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            icon_saved = serializer.save()
        return Response({
            "success": "Icon '{}' updated successfully".format(icon_saved.name)
        })


@login_required
def new_license(request):
    """Покупка лицензии"""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = LicenseForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = LicenseForm(request.POST)
        if form.is_valid():
            new_license = form.save(commit=False)
            new_license.owner = request.user
            new_license.save()
            licensed_group = Group.objects.get(name='licensed')
            licensed_group.user_set.add(request.user)
            return HttpResponseRedirect(reverse('av_icons:license'))
    context = {'form': form}
    return render(request, 'av_icons/new_license.html', context)


@login_required
def checking_for_end_of_license(request):
    """Проверяет, кончился ли срок лицензии. Если кончился, удаляет лицензию и пользователя из группы licensed"""
    license = License.objects.filter(owner=request.user)[0]
    if license:
        if license.end_of_license:
            license.delete()
            licensed_group = Group.objects.get(name='licensed')
            licensed_group.user_set.remove(request.user)