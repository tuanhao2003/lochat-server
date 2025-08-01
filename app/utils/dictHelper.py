from rest_framework import serializers

class DictHelper():
    @staticmethod
    def parse_python_dict(serializer: serializers.ModelSerializer):
        if serializer.is_valid():
            return serializer.validated_data
        return None
