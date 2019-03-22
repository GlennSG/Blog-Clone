from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    # author is set up so that only the superuser can update or create posts
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # creates post with the current time given the set timezone in settings.py (UTC)
    created_date = models.DateTimeField(default=timezone.now)
    # publishes post with or without a time
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        # sets the time when the post is published
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        # given a list of comments (approved and not approved), get only approved approve_comments
        # name comes from Comment class (approved_comments)
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        # after creating a post, go back to post_detail.html page
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        # returns the title of the post
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # approves comments for post, set to False as default
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_abolsute_url(self):
        # after sending comment, return to post_list.html page (main page)
        return reverse('post_list')

    def __str__(self):
        return self.text
