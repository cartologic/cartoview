from rest_framework import serializers


class TagsListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        # you change the representation style here.
        return data.values_list('name', flat=True)
