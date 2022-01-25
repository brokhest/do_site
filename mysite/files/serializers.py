from rest_framework.serializers import Serializer, FileField
from .models import File


class UploadSerializer(Serializer):
    file = FileField()
    class Meta:
        model = File
        fields = "__all__"

    def create(self, validated_data):
        file_data = validated_data.get('file')
        file = File(file=file_data, name=file_data.name)
        file.save()
        return file