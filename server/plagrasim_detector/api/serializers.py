# api/serializers.py
from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'text_content']

    def create(self, validated_data):
        uploaded_file = validated_data['file']
        text_content = uploaded_file.read().decode('utf-8')
        validated_data['text_content'] = text_content
        return super().create(validated_data)
