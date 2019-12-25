from django.conf import settings
from django.db import models
from django.utils import timezone

from django.db.models import Q # we can chain different lookups together

# Create your models here.
# after making any changes to modes we have to check two things:
# -check name of our app settings in installed apps
# -run command "python manage.py makemigrations" and after that migrate
# this is because to make database known of the changes we had made in it

# we can use foreign key to tie one model to another

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		# BlogPost.objects
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (Q(title__icontains=query) | 
					Q(content__icontains=query) |
					Q(slug__icontains=query) |
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query) |
					Q(user__email__icontains=query))


		return self.filter(lookup)

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)


class BlogPost(models.Model): 
	# use blogpost_set -> would return queryset containing all data
	# of the user you associated foreign key with
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	# SET_NULL is similar to CASCADE that if we delete the default user it would
	# set NULL all the related items to it but CASCADE would rather delete them.
	# if we had deleted another user it would add the items related to that user
	# to our default user 
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique = True, null=True)
	content = models.TextField(null = True, blank = True)
	publish_date = models.DateTimeField(auto_now = False, auto_now_add = False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)

	objects = BlogPostManager()

	class Meta:
		ordering = ['-publish_date', 'updated', 'timestamp']

	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_published_url(self):
		self.publish_date = timezone.now()
		return f"/blog"

	def get_edit_url(self):
		return f"/blog/{self.slug}/edit"

	def get_delete_url(self):
		return f"/blog/{self.slug}/delete"