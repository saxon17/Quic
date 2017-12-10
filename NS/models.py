#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import  reverse
from django.contrib.auth.models import  User
from Quic.settings import  MEDIA_URL

# Create your models here.
import os
class SeuMaster(models.Model):
    name = models.CharField(max_length=250)
    sex = models.CharField(max_length=250)
    birth = models.CharField(max_length=250)
    home = models.CharField(max_length=250)
    first_college = models.CharField(max_length=250)
    second_college = models.CharField(max_length=250,null=True,default='seu')
    major = models.CharField(max_length=250)
    tutor = models.CharField(max_length=250)
    department = models.CharField(max_length=250)
    grade = models.CharField(max_length=250)

    # def __str__(self):
    #     return  str(self.id) + '-' + self.name

    def __unicode__(self):
        return str(self.id) + '-' + self.name


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % ('user', instance.user.id, ext)
    return os.path.join('user_uploads', filename)
class UserDetail(models.Model):
    GENDER_CHOICES = (
        (u'M', u'男生'),
        (u'F', u'女生'),
    )

    XINGZUO_CHOICES = ((u'Vir', u'处女座'),
         (u'Agr', u'宝瓶座'),
         (u'Ari', u'白羊座'),
         (u'Cnc', u'巨蟹座'),
         (u'Cap', u'摩羯座'),
         (u'Gem', u'双子座'),
         (u'Leo', u'狮子座'),
         (u'Lib', u'天秤座'),
         (u'Psc', u'双鱼座'),
         (u'Sco', u'天蝎座'),
         (u'Tau', u'金牛座'),
         (u'Sgr', u'射手座'),)

    GRADE_CHOICES =   ((u'D1', u'大一'),
                       (u'D2', u'大二'),
                       (u'D3', u'大三'),
                       (u'D4', u'大四'),
                       (u'Y1', u'研一'),
                       (u'Y2', u'研二'),
                       (u'Y3', u'研三'),
                       (u'B1', u'博一'),
                       (u'B2', u'博二'),
                       (u'B3', u'博三'),)


    user = models.OneToOneField(User,related_name="profile")

    name = models.CharField(max_length=200,null=True)
    sex = models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=True)
    college = models.CharField(max_length=200,null=True,blank=True)
    major = models.CharField(max_length=200,null=True)
    age = models.CharField(max_length=200,null=True)
    hometown = models.CharField(max_length=200,null=True)
    xingzuo = models.CharField(max_length=200,null=True,blank=True,choices=XINGZUO_CHOICES)
    hobbie = models.CharField(max_length=200,null=True,blank=True)
    we_chat = models.CharField(max_length=200,null=True)

    grade = models.CharField(max_length=250,choices=GRADE_CHOICES,null=True)

    head_pic = models.FileField(default='head-girl.png',blank=True,upload_to=content_file_name)

    role = models.CharField(max_length=20,blank=True,null=True,default='invalid')
  

    # belike
    # be_liked = models.IntegerField()
    def get_absolute_url(self):
        return  reverse('detail',kwargs={'slug':self.user_id})
        # return  reverse('detail',kwargs={'pk':self.pk})

    def __unicode__(self):
        return unicode(self.name) + '-' + unicode(self.college) + '-' + unicode(self.major)






#signal

def user_detail_is_created(sender,instance,created,**kwargs):
    if created:
        userDetail,created = UserDetail.objects.get_or_create(user=instance)

from  django.db.models.signals import post_save
post_save.connect(user_detail_is_created,sender=User)




class  RelationShip(models.Model):
    user = models.ForeignKey(User)
    likeID  = models.IntegerField()
    class Meta:
        unique_together = ("user", "likeID")

    def __unicode__(self):
        return unicode(self.user.id) + '-' + unicode(self.likeID)



class WeiXinAccountLog(models.Model):
    user = models.ForeignKey(User)
    # accout = models.CharField(max_length=200,null=True)
    passwd = models.CharField(max_length=200,null=True)

    def __unicode__(self):
        return unicode(self.user_id) + '-' + unicode(self.user) + '-' + unicode(self.passwd)



