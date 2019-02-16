from app import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    sex = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'nickname',
            'email',
            'sex',
            'phone_number',
            'date_joined',
            'note']

    def get_sex(self, obj):
        if obj.sex == 0:
            return '男'
        else:
            return '女'


class ArticleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    category = serializers.CharField(source='category.name')
    tags = serializers.SerializerMethodField()
    is_public = serializers.SerializerMethodField()
    class Meta:
        model = models.Artical
        fields = [
            'id',
            'title',
            'author',
            'content',
            'created_at',
            'is_public',
            'is_delete',
            'category',
            'tags',
            ]

    def get_tags(self, obj):
        tags = obj.tag.all()
        s = ''
        for tag in tags:
            s += tag.name + ','
        if s != '':
            s = s[:-1]
        return s
    def get_is_public(self, obj):
        if obj.is_public == 1:
            return '是'
        else:
            return '否'

class CommentsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    article = serializers.CharField(source='artical.title')
    user = serializers.CharField(source='user.username')


    class Meta:
        model = models.Artical
        fields = [
            'id',
            'content',
            'article',
            'user',
            'created_at',
            ]


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = models.Category
        fields = [
            'id',
            'name',
            'created_at',
        ]


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Website
        fields = [
            'name',
            'domain',
            'max_upload',
            'title',
            'describe',
            'information',
        ]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mail
        fields = [
            'host',
            'port',
            'email',
            'nickname',
            'password',
        ]


class SyslogSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = models.System_log
        fields = [
            'id',
            'user',
            'behavior',
            'ip',
            'time',
        ]


class UserlogSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = models.User_log
        fields = [
            'id',
            'user',
            'behavior',
            'ip',
            'region',
            'source',
            'time',
        ]
