from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    '''
    用户表
    '''
    nickname = models.CharField("昵称", max_length=30)
    sex = models.SmallIntegerField(default=1)
    phone_number = models.CharField("手机号", max_length=30)
    head_img = models.CharField("头像", max_length=200, default='/static/images/head.jpg')
    note = models.CharField("备注", max_length=200)

    class Meta(AbstractUser.Meta):
        pass


class Website(models.Model):
    '''
    网站设置
    '''
    name = models.CharField("网站名称", max_length=30)
    domain = models.CharField("域名", max_length=30)
    max_upload = models.IntegerField('最大文件上传', default=2048)
    title = models.CharField("首页标题", max_length=30)
    describe = models.CharField("描述", max_length=200)
    information = models.CharField("版权信息", max_length=100)


class Mail(models.Model):
    '''
    邮件设置
    '''
    host = models.CharField("服务器", max_length=30)
    port = models.CharField("端口", max_length=30)
    email = models.CharField("发件人邮箱", max_length=30)
    nickname = models.CharField("发件人昵称", max_length=30)
    password = models.CharField("邮箱登录密码", max_length=30)


class Category(models.Model):
    '''
    文章分类
    '''
    name = models.CharField("分类", max_length=20)
    created_at = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("标签", max_length=20)

    def __str__(self):
        return self.name


class Artical(models.Model):
    '''文章内容'''
    title = models.CharField("标题", max_length=30)
    author = models.CharField("作者", max_length=20, default="admin")
    content = models.TextField("正文")
    created_at = models.DateTimeField("发布时间", auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=True)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    is_public = models.SmallIntegerField("是否公开", default=1)
    is_delete = models.SmallIntegerField("是否被删除", default=0)
    viewers = models.PositiveIntegerField("访问量", default=0)

    def __str__(self):
        return self.title


class Comments(models.Model):
    '''
    评论
    '''
    user = models.ForeignKey(User, verbose_name="评论者", on_delete=True)
    artical = models.ForeignKey(Artical, verbose_name="文章", on_delete=True)
    content = models.TextField("内容")
    created_at = models.DateTimeField("评论时间", auto_now=True)


class User_log(models.Model):
    '''
    用户操作日志
    '''
    user = models.ForeignKey(User, verbose_name="用户", on_delete=True)
    behavior = models.CharField(verbose_name="行为", max_length=30)
    ip = models.CharField(verbose_name="ip地址", max_length=30)
    region = models.CharField(verbose_name="地区", max_length=30)
    source = models.CharField(verbose_name="来源", max_length=30)
    time = models.DateTimeField('操作时间', auto_now=True)


class System_log(models.Model):
    '''
    系统操作日志
    '''
    user = models.ForeignKey(User, verbose_name="用户", on_delete=True)
    behavior = models.CharField(verbose_name="行为", max_length=30)
    ip = models.CharField(verbose_name="ip地址", max_length=30)
    time = models.DateTimeField('操作时间', auto_now=True)


class List(models.Model):
    '''
    友链
    '''
    friend = models.URLField(verbose_name="链接", blank=True)
    name = models.CharField(verbose_name="名称", max_length=30)

    class Meta:
        verbose_name = "友链"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
