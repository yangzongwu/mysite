import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.utils.html import strip_tags
from taggit.managers import TaggableManager
from PIL import Image

class Website_views(models.Model):
    nid = models.AutoField(primary_key=True)
    views = models.IntegerField()


class view_ip(models.Model):
    nid = models.AutoField(primary_key=True)
    user_ip = models.CharField(max_length=15, null=False)
    create_time = models.DateTimeField(auto_now_add=True)

class view_ip_history(models.Model):
    nid = models.AutoField(primary_key=True)
    user_ip = models.CharField(max_length=15, null=False)
    create_time = models.DateTimeField(auto_now_add=True)


class BlogClassify(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)
    def _str__(self):
        return self.name

class BlogDifficulty(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class BlogClassifyDataStructure(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class BlogAlgorithm(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)
    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)
    abstract = models.CharField(max_length=200, blank=True)
    classify = models.ForeignKey(BlogClassify, null=True, on_delete=models.CASCADE, related_name='blog')
    tags = models.ManyToManyField(Tag, blank=True)
    avatar = models.ImageField(upload_to='blog/%Y%m%d/', blank=True)
    difficulty=models.ForeignKey(BlogDifficulty,null=True,on_delete=models.CASCADE, related_name='blog')
    datastructrue=models.ForeignKey(BlogClassifyDataStructure,null=True,on_delete=models.CASCADE, related_name='blog')
    algorithm=models.ForeignKey(BlogAlgorithm,null=True,on_delete=models.CASCADE, related_name='blog')

    class Meta:
        ordering = ('-created_time',)

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.abstract = strip_tags(md.convert(self.body))[:200]

        blog = super(Blog, self).save(*args, **kwargs)

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return blog

    def _str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.id])


