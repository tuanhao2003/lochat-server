from rest_framework import serializers
from app.entities.accounts import Accounts

class AccountsMapping(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Accounts
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'created_at', 'updated_at']