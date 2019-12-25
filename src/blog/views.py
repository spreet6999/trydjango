from .forms import BlogPostForm, BlogPostModelForm
from .models import BlogPost
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render,get_object_or_404, redirect
# from django.utils import timezone

# Create / Update / Delete -> POST

# CRUD -> Create Retrieve Update Delete

# We are always gonna make view for each CRUD 

# we have to always take care of the data type of
# arguments passed in case of post_id

def blog_post_list_view(request):
	# list out objects
	# could be search
	# now = timezone.now()
	qs = BlogPost.objects.all().published() # queryset -> List of python objects
	# qs = BlogPost.objects.filter(publish_date__lte=now)
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
		print(my_qs)
	template_name = 'blog/list.html'
	context = {"object_list": qs}
	return render(request, template_name, context)

@staff_member_required
def blog_post_detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/detail.html'
	context = {"object": obj}
	return render(request, template_name, context)



@staff_member_required #this decorator ensures that user who is posting is logged in
def blog_post_create_view(request):	
	# create objects
	# ? use a form
	# request.user -> return something
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		obj.user = request.user
		form = BlogPostModelForm()
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name, context)
	# 	# obj = BlogPost.objects.create(title=title)
	# 	# OR
	# 	# title = form.cleaned_data['title']
	# 	#print(form.cleaned_data)
	# 	form = BlogPostForm()
	# 	obj = BlogPost.objects.create(**form.cleaned_data)
	# 	obj = BlogPost.objects.get(slug = slug)
	# 	raise Http404
	# 	raise Http404()
	# 	raise Http404()

	# django forms
	# django Model forms:
	# except BlogPost.DoesNotExist:
	# except ValueError:
	# form = BlogPostForm(request.POST or None)
	# if form.is_valid():
	# if queryset.count() ==0:
	# obj = queryset.first()
	# Retrieve/List -> GET
	# try: 
	#queryset = BlogPost.objects.filter(slug = slug)

	#print(slug.__class__)

@staff_member_required
def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	form = BlogPostModelForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect("/blog")
	template_name = 'form.html'
	context = {'form': form, "title": f"Update {obj.title}"}
	return render(request, template_name, context)


@staff_member_required  
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {"object": obj}
	return render(request, template_name, context)	

# Create your views here.
# filter -> [] objects, it would return a list of objects
# Get -> 1 object which means GET would return 
# only a single object
#@login_required  