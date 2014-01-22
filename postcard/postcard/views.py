#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from models import *
from django.http import HttpResponse
from django import template
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import os
import datetime
from django.contrib.auth.decorators import login_required
import StringIO
from capcha import capthaGenerate
import urllib2
import hashlib
from PIL import Image
import random
import settings
######################################################################
def menu():
	d={}
	t = get_template("menu.html")
	c = Context(d)
	html = t.render(c)
	html=html
	return html

######################################################################
@csrf_exempt
def view(request,id,passwd):
	list = Send.objects.filter(id=id)
	if len(list)==0:
		return redirect('/')
	obj=list[0]
	if obj.password != passwd:
		return redirect('/')
	if obj.visit == 0:
		obj.visit = 1
		obj.date_view = datetime.datetime.now()
		obj.save()
		dic={'name':obj.fromname,'url':settings.MY_SITE+'/view/'+id+'/'+passwd}
		t2 = get_template("rr.html")
		c2 = Context(dic)
		text = t2.render(c2)
		sabj = 'Su correo entregado'
		send_mail(sabj, text, settings.EMAIL_HOST_USER,    [obj.from_email], fail_silently=False)
		
	body = Body.objects.filter(id = obj.body)[0]
	#return HttpResponse(body.img.url)
	ul= body.img.url
	d1={'text':body.text,'img': ul}
	t = get_template("postcard.html")
	c = Context(d1)
	html = t.render(c)
	d={'fromname':obj.fromname,'from_email':obj.from_email,'to_email':obj.to_email,'html':html,'text':body.text,'img': ul,'to_name':obj.toname}
	t = get_template("view.html")
	c = Context(d)
	html2 = t.render(c)
	
	return HttpResponse(html2)
	
######################################################################
@csrf_exempt
def check_capcha(request):
# return HttpResponse(5)
	if request.method == 'POST':
		pass

	else:
		m = capthaGenerate(request)
		mm = hashlib.md5()
		mm.update(m[1])
		d={'capcha_value': mm.hexdigest(), 'capcha': m[0]}
		t = get_template("capcha_group.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(html)
######################################################################
@csrf_exempt
def home(request):
	return HttpResponse('Hello')
######################################################################
def sending(id):
	obj=Send.objects.filter(id=id)[0]
	if (obj.dateto <= datetime.datetime.now()) and (obj.send==0):
		obj.send=1
		obj.save()
		url=settings.MY_SITE+'/view/'+str(obj.id)+'/'+obj.password
		d={'name':obj.toname,'from_name':obj.fromname,'from_email':obj.from_email,'url':url,'site':settings.MY_SITE}
		t = get_template("send.html")
		c = Context(d)
		text = t.render(c)
		sabj = 'Has recibido una tarjeta virtual de '+ obj.fromname+' ('+obj.from_email+')'
		send_mail(sabj, text, settings.EMAIL_HOST_USER,    [obj.to_email], fail_silently=False)
######################################################################
def ninona(request):
	if request.method == "GET":
		d={'url':'http://ninona.wordpress.com/'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
def collectorsweekly(request):
	if request.method == "GET":
		d={'url':'http://www.collectorsweekly.com/postcards'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
def orsay(request):
	if request.method == "GET":
		d={'url':'http://www.musee-orsay.fr/'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
def picasion(request):
	if request.method == "GET":
		d={'url':'http://picasion.com/es/'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
def picmonkey(request):
	if request.method == "GET":
		d={'url':'http://www.picmonkey.com/'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
def pixlr(request):
	if request.method == "GET":
		d={'url':'http://pixlr.com/editor/'}
		t = get_template("iframe.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
######################################################################
@csrf_exempt
@login_required
def send_postcard(request):
	if request.method == "POST":
		obj=Send()
		obj.user = request.user.id
		obj.date = datetime.datetime.now()
		obj.body =  request.POST['id']
		obj.fromname = request.POST['from_name']
		obj.toname = request.POST['to_name']
		obj.from_email = request.user.email
		obj.to_email = request.POST['to_email']
		obj.dateto = datetime.datetime.strptime(request.POST['date'],'%m/%d/%Y')
		obj.visit=0
		obj.send=0
		st=''
		for i in range(20):
			st = st + random.choice("abcdefghijklmnopqrstu")
		obj.password = st
		obj.save()
		d={}
		t = get_template("mail.html")
		c = Context(d)
		html = t.render(c)
		sending(obj.id)
		return HttpResponse(html)
######################################################################
@csrf_exempt
@login_required
def add(request):
	if request.method == "GET":
		cap=  capthaGenerate(request)
		st = ''#request.user.first_name + ' '+ request.user.last_name
		mm = hashlib.md5()
		mm.update(cap[1])
		obj = Body()

		obj.date = datetime.datetime.now()
		obj.save()
		
		d1={}
		t = get_template("postcard.html")
		c = Context(d1)
		html = t.render(c)
		dd=str(datetime.datetime.now())
		d3=dd[5:7]+'/'+dd[8:10]+"/"+dd[0:4]
		d={'view':html,'id':obj.id,'from_email':request.user.email,'from_name': (request.user.first_name +' '+request.user.last_name),'date':d3,'capcha':cap[0],'capcha_value':mm.hexdigest()}
		t = get_template("add.html")
		c = Context(d)
		html = t.render(c)
		return HttpResponse(menu()+html)
		
	if request.method == "POST":


		obj = Body.objects.filter(id = request.POST['id'])[0]

		obj.text = request.POST['text']
		try:
			obj.img = request.FILES['file']
			ul= obj.img.url
		#return HttpResponse(ul)
			d1={'text':obj.text,'img': ul,'id':obj.id}
		except:
			d1={'text':obj.text,'id':obj.id}
		obj.save()
		t = get_template("postcard.html")
		c = Context(d1)
		html = t.render(c)
		return HttpResponse(html)
######################################################################