from django.shortcuts import render

from blog.models import BlogPost
# Create your views here.
from .models import SearchQuery

def search_view(request):
	query = request.GET.get('q', None)#None is the default value
	user = None
	template_name = 'searches/view.html'
	if request.user.is_authenticated:
		user = request.user
		context = {"query": query}

	if query is not None:
		SearchQuery.objects.create(user=user, query=query)
		blog_list = BlogPost.objects.all().search(query=query)
		context['blog_list'] = blog_list

	else:
		SearchQuery.objects.create(user=user, query=query)
		blog_list = BlogPost.objects.all().search(query=query)
		context['blog_list'] = blog_list
		template_name = 'blog/'

	return render(request, template_name, context) 