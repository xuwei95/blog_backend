from rest_framework.views import APIView
from django.http.response import JsonResponse
from app.models import User, Website, Mail, Category, Artical, Comments, System_log, User_log, Tag
from app.serializers import UserSerializer, WebsiteSerializer, ArticleSerializer, Article_detail_Serializer, CategorySerializer, Serach_Serializer
import json
from rest_framework.pagination import PageNumberPagination
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
            article_count = Artical.objects.filter(is_delete=0, category_id=dic['category_id']).count()
        else:
            article_count = Artical.objects.filter(is_delete=0).count()
        website = [Website.objects.first()]
        ser = WebsiteSerializer(instance=website, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)[0]
        data['article_count'] = article_count
        return JsonResponse(
            {'code': 20000, 'msg': "ok", 'data': data})


class Article_list(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        if 'category_id' in dic.keys():
            all_Article = Artical.objects.filter(is_delete=0, category_id=dic['category_id']).order_by('-created_at').all()
        else:
            all_Article = Artical.objects.filter(is_delete=0).order_by('-created_at').all()
        pg = MyPageNumberPagination()
        Article_list = pg.paginate_queryset(queryset=all_Article, request=request, view=self)
        ser = ArticleSerializer(instance=Article_list, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})


class Article_hot(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        all_Article = Artical.objects.filter(is_delete=0).order_by('-viewers').all()
        if len(all_Article) > 10:
            all_Article = all_Article[:10]
        ser = ArticleSerializer(instance=all_Article, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})

class Article_category(APIView):
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
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Catogory), 'data': data})


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
        return JsonResponse(
            {'code': 20000, 'msg': "", 'data': data[0]})

class Serach(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dic = request.query_params
        query_String = dic['queryString']
        all_Article = Artical.objects.filter(is_delete=0).filter(title__icontains=query_String).all()
        ser = Serach_Serializer(instance=all_Article, many=True)
        data = json.dumps(ser.data, ensure_ascii=False)
        data = eval(data)
        return JsonResponse(
            {'code': 20000, 'msg': "", 'count': len(all_Article), 'data': data})
