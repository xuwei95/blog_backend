from rest_framework.views import APIView
from django.http.response import JsonResponse
from app.models import User, Website, Mail, Category, Artical, Comments, System_log, User_log, Tag
from app.serializers import UserSerializer, WebsiteSerializer, ArticleSerializer, Article_detail_Serializer, CategorySerializer, Serach_Serializer, CommentsSerializer
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.hashers import make_password
import logging
logger = logging.getLogger('django')
# Create your views here.


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100
    page_query_param = "page"


class Info(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        if 'category_id' in dic.keys():
            article_count = Artical.objects.filter(
                is_delete=0, category_id=dic['category_id']).count()
        else:
            article_count = Artical.objects.filter(is_delete=0).count()
        website = [Website.objects.first()]
        ser = WebsiteSerializer(instance=website, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)[0]
        data['article_count'] = article_count
        logger.info('userlog---someone access home page--ip:{}'.format(request.META['REMOTE_ADDR']))
        return JsonResponse(
            {'code': 20000, 'msg': "ok", 'data': data})


class User_api(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        meta = jwt_decode_handler(dic['token'])
        username = meta['username']
        logger.info('userlog---user:{}--access home page--ip:{}'.format(username, request.META['REMOTE_ADDR']))
        user = User.objects.filter(username=username).first()
        hrad_img = user.head_img
        data = {'name': username, 'head_img': hrad_img}
        return JsonResponse({'code': 20000, 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        username = dic['username']
        password = dic['password']
        repass = dic['repass']
        if password != repass:
            return JsonResponse(
                {'code': 20000, 'success': 0, 'msg': "两次输入密码不同，请重新输入"})
        user = User.objects.filter(username=username).first()
        if user is not None:
            return JsonResponse({'code': 20000, 'success': 0, 'msg': "用户名已存在"})
        else:
            password = make_password(password)
            user = User(username=username,
                        password=password)
            user.save()
            logger.info('userlog---new user:{}--regist--ip:{}'.format(user.username, request.META['REMOTE_ADDR']))
            return JsonResponse({'code': 20000, 'success': 1, 'msg': "注册成功"})


class Comments_api(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        article_id = dic['article_id']
        comments = Comments.objects.filter(artical_id=article_id).all()
        pg = MyPageNumberPagination()
        comment_list = pg.paginate_queryset(
            queryset=comments, request=request, view=self)
        ser = CommentsSerializer(instance=comment_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse({'code': 20000, 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        username = dic['username']
        content = dic['content']
        artical = dic['artical']
        user = User.objects.filter(username=username).first()
        user_id = user.id
        comment = Comments(
            content=content,
            artical_id=artical,
            user_id=user_id)
        comment.save()
        logger.info('userlog---user:{}--publish a comments:{}--article:{}--ip:{}'.format(username, content, artical, request.META['REMOTE_ADDR']))
        return JsonResponse({'code': 20000, 'success': 1, 'msg': "评论发表成功"})


class Article_api(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        if 'category_id' in dic.keys():
            all_Article = Artical.objects.filter(
                is_delete=0, category_id=dic['category_id']).order_by('-created_at').all()
        else:
            all_Article = Artical.objects.filter(
                is_delete=0).order_by('-created_at').all()
        pg = MyPageNumberPagination()
        Article_list = pg.paginate_queryset(
            queryset=all_Article, request=request, view=self)
        ser = ArticleSerializer(instance=Article_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})


class Article_detail(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        id = dic['id']
        Article = Artical.objects.filter(id=id).first()
        Article.viewers += 1
        Article.save()
        Article = [Article]
        ser = Article_detail_Serializer(instance=Article, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        logger.info('userlog---someone access detail page--{}-ip:{}'.format(Article[0].id, request.META['REMOTE_ADDR']))
        return JsonResponse(
            {'code': 20000, 'msg': "", 'data': data[0]})


class Article_hot(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        all_Article = Artical.objects.filter(
            is_delete=0).order_by('-viewers').all()
        if len(all_Article) > 10:
            all_Article = all_Article[:10]
        ser = ArticleSerializer(instance=all_Article, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})


class Category_api(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        if 'category_id' in dic:
            all_Catogory = Category.objects.filter(id=dic['category_id']).all()
        else:
            all_Catogory = Category.objects.all()
        ser = CategorySerializer(instance=all_Catogory, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        logger.info('userlog---someone access category page--ip:{}'.format(request.META['REMOTE_ADDR']))
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Catogory), 'data': data})


class Serach(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        query_String = dic['queryString']
        all_Article = Artical.objects.filter(
            is_delete=0).filter(
            title__icontains=query_String).all()
        ser = Serach_Serializer(instance=all_Article, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})
