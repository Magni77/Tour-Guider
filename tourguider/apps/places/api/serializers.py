from rest_framework import serializers

from apps.places.models import OpeningHour, Place, Guide


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = '__all__'

    def create(self, validated_data):
        validated_data['opening_hour'] = validated_data['opening_hour'].replace(tzinfo=None)
        validated_data['closing_hour'] = validated_data['closing_hour'].replace(tzinfo=None)
        hour = OpeningHour.objects.filter(
            **validated_data
        ).first()
        if not hour:
            hour = OpeningHour(
                **validated_data
            )
            hour.save()
        return hour

    def update(self, instance, validated_data):
        instance.weekday = validated_data.get('weekday', instance.weekday)
        instance.opening_hour = validated_data.get(
            'opening_hour', instance.opening_hour).replace(tzinfo=None)
        instance.closing_hour = validated_data.get(
            'closing_hour', instance.closing_hour).replace(tzinfo=None)
        instance.save()

        return instance


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
  #  guides = GuideSerializer(many=True)

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('created',)


class PlaceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('created',)