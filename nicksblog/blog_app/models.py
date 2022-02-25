from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    # date = date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to='')

class Images(models.Model):
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')
