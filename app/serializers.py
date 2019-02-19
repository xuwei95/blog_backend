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
        format="%Y-%m-%d", required=False, read_only=True)
    category = serializers.CharField(source='category.name')
    category_id = serializers.CharField(source='category.id')
    tags = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    class Meta:
        model = models.Artical
        fields = [
            'id',
            'title',
            'author',
            'content',
            'created_at',
            'is_delete',
            'category',
            'category_id',
            'tags',
            'viewers',
            ]

    def get_tags(self, obj):
        tags = obj.tag.all()
        s = ''
        for tag in tags:
            s += tag.name + ','
        if s != '':
            s = s[:-1]
        return s

    def get_content(self, obj):
        content = obj.content
        content = content.replace('#', '').replace('<br>', '')
        if len(content) > 120:
            content = content[:120] + '...'
        return content


class Serach_Serializer(serializers.ModelSerializer):
    value = serializers.CharField(source='title')
    class Meta:
        model = models.Artical
        fields = [
            'id',
            'value'
            ]

class Article_detail_Serializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d", required=False, read_only=True)
    category_id = serializers.CharField(source='category.id')
    category = serializers.CharField(source='category.name')
    tags = serializers.SerializerMethodField()
    class Meta:
        model = models.Artical
        fields = [
            'id',
            'title',
            'author',
            'content',
            'created_at',
            'is_delete',
            'category',
            'category_id',
            'tags',
            'viewers',
            ]

    def get_tags(self, obj):
        tags = obj.tag.all()
        s = ''
        for tag in tags:
            s += tag.name + ','
        if s != '':
            s = s[:-1]
        return s


class CommentsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    article = serializers.CharField(source='artical.title')
    user = serializers.CharField(source='user.username')
    head_img = serializers.CharField(source='user.head_img')

    class Meta:
        model = models.Artical
        fields = [
            'id',
            'content',
            'article',
            'user',
            'created_at',
            'head_img'
            ]

class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    article_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = [
            'id',
            'name',
            'created_at',
            'article_list'
        ]

    def get_article_list(self, obj):
        li = models.Artical.objects.filter(is_delete=0, category_id=obj.id).order_by('-viewers').all()
        artilce_list = []
        for i in li:
            artilce_list.append({'id': i.id, 'title': i.title})
        return artilce_list


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
