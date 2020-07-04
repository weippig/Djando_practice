from django.shortcuts import render,get_object_or_404
from .models import Post
#翻頁
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView

#share post
from .forms import EmailPostForm,CommentForm

from taggit.models import Tag

def post_list(request,tag_slug=None):
  object_list = Post.published.all()
  tag = None
  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug)
    object_list = object_list.filter(tags__in = [tag])
  paginator = Paginator(object_list,3)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger: #page不是整數，轉到第一頁
    posts = paginator.page(1)
  except EmptyPage:  #page out of range>>deliver to last page
    posts = paginator.page(paginator.num_pages)	
  return render(request,
          'blog/post/list.html',
          {'posts':posts,
          'page':page,
          'tag':tag})

# 展現單獨ㄉ帖子

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published')
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
        
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments, 
                  'new_comment': new_comment,
                  'comment_form': comment_form})

class PostListView(ListView): #類似上面的post_list
	queryset = Post.published.all()
	#查詢集
	context_object_name = 'posts'
	paginate_by = 3 #分頁處理每頁顯示三個對象
	template_name = 'blog/post/list.html'



# from django.http import HttpResponseRedirect
# def redirect_root(request):
# 	return HttpResponseRedirect('/blog/')