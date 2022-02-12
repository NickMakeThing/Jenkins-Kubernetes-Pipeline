from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    # date = date_created = models.DateTimeField(auto_now_add=True) #how to force australian time?
    body = models.TextField()
    thumbnail = models.ImageField(upload_to='')
    # video?

class Images(models.Model):
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='')
"""
class Product(models.Model):
    code = models.CharField(max_length=50,null=False,unique=True)
    name = models.CharField(max_length=50,null=True)
    current_weight = models.FloatField()
    energy = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    sugars = models.FloatField()

class WeightChange(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_time = models.CharField(max_length=24) #change to datetime field
    weight_change = models.FloatField()
"""