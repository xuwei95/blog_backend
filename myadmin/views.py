from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.http.response import JsonResponse
from app.models import User, Website, Mail, Category, Artical, Comments, System_log, User_log, Tag
from myadmin.serializers import UserSerializer, WebsiteSerializer, EmailSerializer,\
    CategorySerializer, ArticleSerializer, CommentsSerializer, SyslogSerializer, UserlogSerializer
import json
from django.contrib.auth.hashers import make_password, check_password
from myadmin.permission import AdminPermission
from rest_framework_jwt.utils import jwt_decode_handler
from myadmin.utils import disk_stat, getCPUstate, getMemorystate, network, count_user
import datetime
# Create your views here.


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100
    page_query_param = "page"


class Info(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        meta = jwt_decode_handler(dic['token'])
        user = User.objects.filter(username=meta['username']).first()
        view_count = count_user()
        user_count = User.objects.count()
        article_count = Artical.objects.count()
        comments_count = Comments.objects.count()
        # https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif
        data = {'roles': user.username,
                'name': user.username,
                'avatar': user.head_img,
                'view_count': view_count,
                'user_count': user_count,
                'article_count': article_count,
                'comments_count': comments_count}
        return JsonResponse({'code': 20000, 'data': data})


class Admin_User(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        meta = jwt_decode_handler(dic['token'])
        user = [User.objects.filter(username=meta['username']).first()]
        ser = UserSerializer(instance=user, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'data': data[0]})

    def post(self, request, *args, **kwargs):
        dic = request.data
        id = dic['id']
        user = User.objects.filter(id=id).first()
        if dic['sex'] == '男':
            sex = 0
        elif dic['sex'] == '女':
            sex = 1
        else:
            return JsonResponse({'code': 'sex_error'})
        if user is None:
            User.objects.create(username=dic['username'],
                                nickname=dic['nickname'],
                                phone_number=dic['phone_number'],
                                email=dic['email'],
                                sex=sex,
                                note=dic['note'],
                                )
        else:
            user.username = dic['username']
            user.nickname = dic['nickname']
            user.phone_number = dic['phone_number']
            user.email = dic['email']
            user.sex = sex
            user.note = dic['note']
            user.save()
        return JsonResponse({'code': 20000, 'msg': '修改成功'})


class User_password(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        dic = request.data
        old_password = dic['old_password']
        new_password = dic['new_password']
        repass = dic['repass']
        user = User.objects.first()
        password = user.password
        is_valid = check_password(old_password, password)
        if not is_valid:
            return JsonResponse({'code': 20000, 'msg': '密码错误'})
        elif new_password != repass:
            return JsonResponse({'code': 20000, 'msg': '两次密码输入不同，请重新输入'})
        else:
            user.password = make_password(new_password)
            user.save()
            return JsonResponse({'code': 20000, 'msg': '密码修改成功'})


class User_list(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        ser = UserSerializer(instance=users, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(data), 'data': data})


class Comments_api(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        comments = Comments.objects.all()
        pg = MyPageNumberPagination()
        comment_list = pg.paginate_queryset(
            queryset=comments, request=request, view=self)
        ser = CommentsSerializer(instance=comment_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(comments), 'data': data})


class Category_api(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        all_category = Category.objects.all()
        pg = MyPageNumberPagination()
        category_list = pg.paginate_queryset(
            queryset=all_category, request=request, view=self)
        ser = CategorySerializer(instance=category_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_category), 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        name = dic['category']
        category = Category.objects.filter(name=name).first()
        if category:
            return JsonResponse({'code': 20000, 'msg': '标题已存在'})
        else:
            category = Category(name=name)
            category.save()
            return JsonResponse({'code': 20000, 'msg': 'ok'})

    def put(self, request, *args, **kwargs):
        dic = request.data
        id = dic['id']
        name = dic['name']
        category = Category.objects.filter(name=name).first()
        if category:
            return JsonResponse({'code': 20000, 'msg': '分类已存在'})
        category = Category.objects.filter(id=id).first()
        if category:
            category.name = name
            category.save()
            return JsonResponse({'code': 20000, 'msg': 'ok'})
        else:
            return JsonResponse({'code': 20000, 'msg': 'error'})

    def delete(self, request, *args, **kwargs):
        dic = request.data
        id = dic['id']
        category = Category.objects.filter(id=id).first()
        if category:
            try:
                category.delete()
            except BaseException:
                return JsonResponse({'code': 20000, 'msg': '删除失败，已有文章属于该分类'})
            return JsonResponse({'code': 20000, 'msg': 'ok'})
        else:
            return JsonResponse({'code': 20000, 'msg': 'error'})


class Article_api(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        all_Article = Artical.objects.filter(is_delete=0).all()
        pg = MyPageNumberPagination()
        Article_list = pg.paginate_queryset(
            queryset=all_Article, request=request, view=self)
        ser = ArticleSerializer(instance=Article_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        title = dic['title']
        meta = jwt_decode_handler(dic['token'])
        user = User.objects.filter(username=meta['username']).first()
        article = Artical.objects.filter(title=title).first()
        if article is None:
            category = Category.objects.filter(name=dic['category']).first()
            article = Artical.objects.create(title=dic['title'],
                                             content=dic['content'],
                                             category=category,
                                             is_public=int(dic['is_public']),
                                             author=user.username
                                             )
            tags = dic['tags'].split(',')
            for t in tags:
                tag = Tag.objects.filter(name=t).first()
                if tag is None:
                    tag = Tag.objects.create(name=t)
                article.tag.add(tag)
            article.save()
            return JsonResponse({'code': 20000, 'msg': '添加成功'})
        else:
            return JsonResponse({'code': 20000, 'msg': '文章名称已存在，请重新输入'})

    def put(self, request, *args, **kwargs):
        dic = request.data
        id = dic['id']
        title = dic['title']
        article = Artical.objects.filter(id=id).first()
        category = Category.objects.filter(name=dic['category']).first()
        article.title = title
        article.content = dic['content']
        article.category = category
        if dic['is_public']:
            article.is_public = 1
        else:
            article.is_public = 0
        article.tag.clear()
        tags = dic['tags'].split(',')
        for t in tags:
            tag = Tag.objects.filter(name=t).first()
            if tag is None:
                tag = Tag.objects.create(name=t)
            article.tag.add(tag)
        article.save()
        return JsonResponse({'code': 20000, 'msg': '更新成功'})

    def delete(self, request, *args, **kwargs):
        dic = request.data
        id = dic['id']
        real_delete = int(dic['real_delete'])
        article = Artical.objects.filter(id=id).first()
        if article:
            if real_delete == 0:
                article.is_delete = 1
                article.save()
                return JsonResponse({'code': 20000, 'msg': '已移入回收站'})
            elif real_delete == 1:
                comments = Comments.objects.filter(artical_id=id).all()
                for comment in comments:
                    comment.delete()
                article.delete()
                return JsonResponse({'code': 20000, 'msg': '删除成功'})
        else:
            return JsonResponse({'code': 20000, 'msg': '未知错误'})


class Recly(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        all_Article = Artical.objects.filter(is_delete=1).all()
        pg = MyPageNumberPagination()
        Article_list = pg.paginate_queryset(
            queryset=all_Article, request=request, view=self)
        ser = ArticleSerializer(instance=Article_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        if 'id' in dic.keys():
            article = Artical.objects.filter(id=dic['id']).first()
            article.is_delete = 0
            article.save()
            return JsonResponse({'code': 20000, 'msg': '文章还原成功'})
        else:
            try:
                articles = Artical.objects.filter(is_delete=1).all()
                for article in articles:
                    comments = Comments.objects.filter(
                        artical_id=article.id).all()
                    for comment in comments:
                        comment.delete()
                    article.delete()
                return JsonResponse({'code': 20000, 'msg': '清空回收站成功'})
            except BaseException:
                return JsonResponse({'code': 20000, 'msg': '未知错误'})


class Web_site(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        website = [Website.objects.first()]
        ser = WebsiteSerializer(instance=website, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "ok", 'data': data[0]})

    def post(self, request, *args, **kwargs):
        dic = request.data
        website = Website.objects.first()
        if website is None:
            Website.objects.create(name=dic['name'],
                                   domain=dic['domain'],
                                   max_upload=dic['max_upload'],
                                   title=dic['title'],
                                   describe=dic['describe'],
                                   information=dic['information'],
                                   )
        else:
            website.name = dic['name']
            website.domain = dic['domain']
            website.max_upload = dic['max_upload']
            website.title = dic['title']
            website.describe = dic['describe']
            website.information = dic['information']
            website.save()
        return JsonResponse({'code': 20000, 'msg': '修改成功'})


class Email(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        email = Mail.objects.all()
        ser = EmailSerializer(instance=email, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        if len(data) == 0:
            data = []
        else:
            data = data[0]
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(data), 'data': data})

    def post(self, request, *args, **kwargs):
        dic = request.data
        email = Mail.objects.first()
        if email is None:
            Mail.objects.create(host=dic['host'],
                                port=dic['port'],
                                email=dic['email'],
                                nickname=dic['nickname'],
                                password=dic['password'])
        else:
            email.host = dic['host']
            email.port = dic['port']
            email.email = dic['email']
            email.nickname = dic['nickname']
            email.password = dic['password']
            email.save()
        return JsonResponse({'code': 20000, 'msg': '修改成功'})


class Syslog(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        syslogs = System_log.objects.all()
        ser = SyslogSerializer(instance=syslogs, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(data), 'data': data})


class Sys_info(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        cpu = getCPUstate()
        memory = getMemorystate()
        disk = disk_stat()
        sent, recv = network()
        time = (datetime.datetime.now().utcnow() + datetime.timedelta(hours=8)).strftime("%H:%M:%S")
        dic = {'time': time,
               'cpu': cpu,
               'memory': memory,
               'sent': sent,
               'recv': recv,
               'disk': disk}
        return JsonResponse(
            {'code': 20000, 'msg': "", 'data': dic})


class Network_info(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        sent, recv = network()
        time = (datetime.datetime.now().utcnow() + datetime.timedelta(hours=8)).strftime("%H:%M:%S")
        dic = {'time': time,
               'sent': sent,
               'recv': recv
               }
        return JsonResponse(
            {'code': 20000, 'msg': "", 'data': dic})


class Userlog(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        email = User_log.objects.all()
        ser = UserlogSerializer(instance=email, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(data), 'data': data})
