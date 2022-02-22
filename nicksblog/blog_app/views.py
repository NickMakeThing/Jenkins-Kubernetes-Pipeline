from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from .models import BlogPost, Images
from hashlib import sha256
import os
from django.http import HttpResponseForbidden

#list view
class Home(ListView):
    model = BlogPost
    template_name = 'index.html'
    ordering = ['-id']

#detail view
class ViewPost(DetailView):
    template_name = 'details.html'
    model = BlogPost
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Images.objects.filter(post=kwargs['object'])
        context['images'] = images
        return context

class CreatePost(CreateView):
    model = BlogPost
    fields = ['title','body','thumbnail']
    template_name = 'create.html'
    success_url='/'

    def post(self, request, *args, **kwargs):
        if self.authenticate(request):
            response = super().post(request)
            self.save_images(request,response)
        else:
            response = HttpResponseForbidden("<h1>403 Fordbidden/Wrong Password</h1>")
        return response

    def save_images(self,request,response):
        if 'images' in request.FILES and response.status_code < 400:
            image_files=[]
            for img in request.FILES.getlist('images'):
                image_files.append(Images(post=self.object,image=img))
            Images.objects.bulk_create(image_files)
    
    def authenticate(self, request):
        password = request.POST['password']
        password = bytes(password+'saltlol','utf-8')
        hash = sha256(password).hexdigest()
        return hash == os.getenv('BLOGPASSWORD')

#added this note to test pull requests
