from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager #添加標籤用

# Create your models here.

class PublishedManager(models.Manager):
	def get_query(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')

class  Post(models.Model):
	"""docstring for  Posr"""
	STATUS_CHOICES=(
			('draft','Draft'),
			('published','Published')
	)
	title = models.CharField(max_length=250) 
	slug = models.SlugField(max_length=250,unique_for_date='publish') 
	author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
	objects = models.Manager()
	published = PublishedManager()
	tags = TaggableManager()
	class Meta:
		ordering = ('-publish',)
	def get_absolute_url(self):
		   #reverse 允许你通过它们的名字和可选的参数来构建URLS
		   # blog:post_detail
		return reverse('blog:post_detail',
					args=[self.publish.year,
						  self.publish.strftime('%m'),
						  #用strftime保證個位數前面會帶上0
						  self.publish.strftime('%d'),
						  self.slug]) 
	def __str__(self):
		return self.title
	def get_home_page(self):
		return reverse('blog:post_list')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)