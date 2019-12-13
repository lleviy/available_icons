from rest_framework import serializers

from .models import Icon


class IconSerializer(serializers.Serializer):
    """Сериализатор для иконок, доступных только в формате .png"""
    name = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=17)
    status = serializers.CharField(max_length=17)
    png_filepath = serializers.CharField(max_length=255)
    date_added = serializers.DateTimeField()

    def create(self, validated_data):
        return Icon.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.svg_filepath = validated_data.get('svg_filepath', instance.svg_filepath)
        instance.png_filepath = validated_data.get('png_filepath', instance.png_filepath)
        instance.date_added = validated_data.get('date_added', instance.date_added)

        instance.save()
        return instance


class LicensedIconSerializer(IconSerializer):
    """Сериализатор для иконок, доступных в формате как в .png, так и в .svg"""
    svg_filepath = serializers.CharField(max_length=255)


class LicenseSerializer(serializers.Serializer):
    """Сериализатор для лицензии"""
    date_created = serializers.DateTimeField()
    date_ended = serializers.DateField()
