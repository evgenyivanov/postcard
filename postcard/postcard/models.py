from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign
import datetime
import os
import requests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
############################################
class Postcard(models.Model):

	user = models.CharField(max_length=100)
	date = models.DateTimeField()
	count = models.IntegerField(blank=True, null=True)
	body =  models.CharField(max_length=100)
############################################

class Send(models.Model):

	user = models.CharField(max_length=100)
	date = models.DateTimeField()
	body =  models.CharField(max_length=100)
	fromname = models.CharField(max_length=100)
	toname = models.CharField(max_length=100)
	from_email = models.CharField(max_length=100)
	to_email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	visit = models.IntegerField()
	send = models.IntegerField()
	dateto = models.DateTimeField()
	date_view = models.DateTimeField(blank=True, null=True)
############################################

class Body(models.Model):
	def upload_postcard(self, filename):
		return '{file}'.format(file=os.path.basename(filename))
	date = models.DateTimeField()
	img = models.ImageField(blank=True, null=True, upload_to=upload_postcard)
	text = models.TextField(blank=True, null=True)
#############################################

ULOGIN_FIELDS = ['first_name', 'last_name', 'sex', 'email']                                                                                                            
ULOGIN_OPTIONAL = ['photo', 'photo_big', 'city', 'country', 'bdate']       

class UserInfo(models.Model):
    """
    Example model that stores extra information received from authentication
    provider
    """

    # Describes the response with code 'sex': 1 for female
    SEX_FEMALE = 1

    # and 2 for male
    SEX_MALE = 2

    def upload_photo(self, filename):
        return 'avatars/{network}/{uid}/{file}'.format(network=self.ulogin.network,
                                                      uid=self.ulogin.uid,
                                                      file=os.path.basename(filename))

    def upload_photo_big(self, filename):
        return 'photos/{network}/{uid}/{file}'.format(network=self.ulogin.network,
                                                      uid=self.ulogin.uid,
                                                      file=os.path.basename(filename))

    ulogin = models.ForeignKey(ULoginUser)
    sex = models.IntegerField(blank=True, null=True, 
        choices = (
            (SEX_MALE, 'male'),
            (SEX_FEMALE, 'female'),
        ))
    photo = models.ImageField(null=True, blank=True, upload_to=upload_photo_big)
    photo_big = models.ImageField(null=True, blank=True, upload_to=upload_photo_big)
    city = models.CharField(blank=True,  default='', max_length=255)
    country = models.CharField(blank=True,  default='', max_length=255)
    bdate = models.DateField(verbose_name='Birthday', blank=True, null=True)


def catch_ulogin_signal(*args, **kwargs):
    user   = kwargs['user']
    ulogin = kwargs['ulogin_user']
    json   = kwargs['ulogin_data']

    if kwargs['registered']:
        #
        user.first_name = json['first_name']
        user.last_name = json['last_name']
        user.email = json['email']
        user.save()
        
        #######################
        
        ########################

        data = {'ulogin': ulogin}

        for fld in ['sex', 'city', 'country']:
            if fld not in json:
                return
            data[fld] = json[fld]

        if 'bdate' in json and json['bdate']:
            d, m, y = json['bdate'].split('.')
            data['bdate'] = datetime.datetime(int(y), int(m), int(d))
        
        userinfo = UserInfo.objects.create(**data)

        for fld in ['photo', 'photo_big']:
            if fld not in json:
                continue
            getattr(userinfo, fld).save(os.path.basename( json[fld] ),                                                                                                        
                                        ContentFile( requests.get( json[fld] ).raw.read() ))  
           
        userinfo.save()
            

assign.connect(receiver = catch_ulogin_signal,
               sender   = ULoginUser,
               dispatch_uid = 'customize.models')

###############################################################################################