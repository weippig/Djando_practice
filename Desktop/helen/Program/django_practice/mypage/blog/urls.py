from django.urls import path
from . import views


urlpatterns = [
	path(r'', views.post_list, name='post_list'),
	path(r'tag/<tag_slug>',views.post_list,name='post_list_by_tag'),
	# path(r'',views.PostListView.as_view(),name='post_list'),
	path(r'<int:year>/<int:month>/<int:day>/<post>/',
        views.post_detail,
        name='post_detail'),
	# path(r'<int:post_id>/share/',views.post_share,name='post_share'),
]