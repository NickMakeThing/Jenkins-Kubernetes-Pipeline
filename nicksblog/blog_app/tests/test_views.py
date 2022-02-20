import pytest
from django.test import RequestFactory
from blog_app.views import CreatePost, Home, ViewPost
from blog_app.models import BlogPost, Images
from django.shortcuts import render
from datetime import datetime
from hashlib import sha256
import os

def setup_module(module):
    password = 'test_password'
    password = bytes(password+'saltlol','utf-8')
    hash = sha256(password).hexdigest()
    os.environ['BLOGPASSWORD'] = hash
    os.environ['DJANGOKEY'] = 'test_key'

def teardown_module(module):
    for file in os.listdir('nicksblog/media/'):
        if file[:9] == 'testimage':
            os.remove('nicksblog/media/'+file)

def check_image(image_entry, image_name):
    return str(image_entry)[:10] == image_name and str(image_entry)[-4:] == '.jpg'

def make_blogpost(factory, password="test_password", title="test_title"):
    thumbnail = open('nicksblog/blog_app/tests/testimage1.jpg','rb')
    body_image1 = open('nicksblog/blog_app/tests/testimage2.jpg','rb')
    body_image2 = open('nicksblog/blog_app/tests/testimage3.jpg','rb')
    post_data = {
        "title":title,
        "body":"test_body",
        "thumbnail": thumbnail,
        "images": [body_image1, body_image2],
        "password": password
    }
    request = factory.post('/create/',post_data)
    view = CreatePost.as_view()
    response = view(request)
    return response

@pytest.mark.django_db
def test_createpost():
    rf = RequestFactory()
    response = make_blogpost(rf)
    post = BlogPost.objects.first()
    first_image = Images.objects.first()
    last_image = Images.objects.last()

    assert BlogPost.objects.all().count() == 1
    assert Images.objects.all().count() == 2
    assert first_image.post == post
    assert last_image.post == post
    assert post.title == "test_title"
    assert post.body == "test_body"
    assert check_image(post.thumbnail,'testimage1') 
    assert check_image(first_image.image,'testimage2')
    assert check_image(last_image.image,'testimage3')
    images = [post.thumbnail, first_image.image, last_image.image]
    for image in images:
        assert str(image) in os.listdir('nicksblog/media/')

    #testing incorrect password
    response = make_blogpost(rf, password='wrong_password')
    post = BlogPost.objects.first()
    first_image = Images.objects.first()
    last_image = Images.objects.last()
    assert response.status_code == 403
    assert BlogPost.objects.all().count() == 1
    assert Images.objects.all().count() == 2

@pytest.mark.django_db
def test_viewpost():
    rf = RequestFactory()
    response = make_blogpost(rf)
    assert BlogPost.objects.all().count() == 1

    request = rf.get('') #???
    view = ViewPost.as_view()
    response = view(request,pk=1) #???
    assert response.status_code == 200
    assert 'test_title' in response.rendered_content
    assert 'test_body' in response.rendered_content
    assert 'testimage2' in response.rendered_content
    assert 'testimage3' in response.rendered_content

@pytest.mark.django_db
def test_home():
    rf = RequestFactory()
    for i in range(3):
        title = "test_title"+str(i+1)
        response = make_blogpost(rf, title=title)

    request = rf.get('')
    view = Home.as_view()
    response = view(request)
    assert response.status_code == 200
    assert BlogPost.objects.all().count() == 3
    assert 'test_title1' in response.rendered_content
    assert 'test_title3' in response.rendered_content
    assert 'testimage1' in response.rendered_content
