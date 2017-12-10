#coding=utf-8
from django.utils.translation import ugettext_lazy as _
from  django.contrib.auth.models import User
from  models import UserDetail

from django import  forms


class UserForm(forms.ModelForm):
      password = forms.CharField(label=_("密码"),
                                widget=forms.PasswordInput)

      class Meta:
           model = User
           fields =['username','email',]

           labels = {
              'username': _('用户名'),
              'email': _('邮箱'),


           }


class UserDetailForm(forms.ModelForm):


    class Meta:
        model = UserDetail
        # exclude = ['user']
        fields = [ 'name','sex','college','major','age','hometown','xingzuo','hobbie','we_chat','grade','head_pic']
        labels = {
            'name': _('姓名'),
            'sex': _('性别'),
            'college':_('学校'),
            'grade':_('所在年级'),
            'major':_('专业'),
            'age':_('年龄'),
            'hometown':_('籍贯'),
            'xingzuo':_('星座'),
            'hobbie':_('爱好'),
            'we_chat':_('微信'),
            'head_pic':_('头像'),
        }