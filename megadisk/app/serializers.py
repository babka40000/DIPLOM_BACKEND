from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from app.models import FilesAndFolders
from rest_framework.serializers import Serializer, FileField
from collections import OrderedDict


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    first_name = serializers.CharField()

    is_staff = serializers.BooleanField()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'], first_name=validated_data['first_name'],
                                        is_staff=validated_data['is_staff'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'is_staff')


class FilesAndFoldersSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = FilesAndFolders
        fields = '__all__'
        read_only_fields = ('user', )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        if validated_data["is_folder"]:
            validated_data["name"] = 'Новая папка'

        return super().create(validated_data)


class AmountFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesAndFolders
        fields = ('file', 'file_size')


class AdminOperationsSerializer(serializers.ModelSerializer):
    amount_files = AmountFilesSerializer(many=True, read_only=True)

    files_count = serializers.IntegerField(
        source='amount_files.count',
        read_only=True,
    )

    file_size_sum = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'is_superuser',
                  'is_staff', 'amount_files', 'files_count', 'file_size_sum')

    def to_representation(self, instance):
        result = super(AdminOperationsSerializer, self).to_representation(instance)

        for key in result:
            if key == 'amount_files':
                for elem in result[key].copy():
                    if elem['file'] is None:
                        result[key].remove(elem)
                        result['files_count'] = result['files_count'] - 1

        result["file_size_sum"] = sum([files["file_size"] for files in result['amount_files']])
        return result
