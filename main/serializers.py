from rest_framework import serializers
from main.models import UsefulHabit


class UsefulHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsefulHabit
        exclude = ('owner',)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
