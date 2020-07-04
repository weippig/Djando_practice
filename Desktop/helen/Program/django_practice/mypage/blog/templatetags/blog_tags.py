from django import template

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
	return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts':latest_posts}

from django.db.models import Count

# @register.assignment_tag
# def get_most_commented_posts(count=5):
# 	return Post.published.annotate(
# 		total_comments=Count('comments')
# 		).order_by('-total_comments')[:count]
@register.simple_tag
def get_most_commented_posts(count=3):
	return Post.published.annotate(
			total_comments = Count('comments')
		).order_by('-total_comments')[:count]

# @register.simple_tag
# def get_most_commented_posts(count=3):
# 	most_comment=Post.published.annotate(total_comments = Count('comments')
# 		).order_by('-total_comments')[:count]
# 	return {'most_comment':most_comment}