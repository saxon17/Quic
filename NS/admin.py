#coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User

from .models import  SeuMaster,UserDetail,RelationShip,WeiXinAccountLog
# Register your models here.
from django.contrib.auth.admin import  UserAdmin
from django.contrib.auth import  get_user_model

admin.site.register(RelationShip)
admin.site.register(SeuMaster)

admin.site.register(WeiXinAccountLog)
class UserDetailInline(admin.StackedInline):
    model =  UserDetail
    # can_delete =  False


class UserDtailAdmin(UserAdmin):
    inlines =  (UserDetailInline,)



class UserDetailSearchAdmin(admin.ModelAdmin):
    # list_display = ('name', 'age')
    search_fields = ('name','grade','sex')

    list_display = ( 'name', 'grade', 'sex','get_user_id','is_active','get_user_name','role','image_img','head_pic')
    #foreign key special function
    def get_user_id(self, obj):

        edit_link = "/admin/auth/user/%s/change/" %obj.user.id

        return u'<a href="%s">%s</a>' % (edit_link,obj.user.id)

    def image_img(self,obj):

            return u'<img src="http://www.nextsecond.cn/media/%s" / style="height:17px">' % obj.head_pic


    image_img.short_description = 'Thumb'
    image_img.allow_tags = True





    def get_user_name(self, obj):

        # edit_link = "/admin/auth/user/%s/change/" %obj.user
        user_name = str(obj.user)
        if 'weixin' in user_name:
            return "<div style='background-color:greenyellow;'>微信用户</div>"
        else:
            return  "网站用户"


    def is_active(self, obj):
        status = obj.user.is_active

        if status == True:

            return u"正常"
        else:
            return u"信息不全,被禁用"

    get_user_id.allow_tags = True
    get_user_name.allow_tags = True










UserAdmin.list_display = ('id','email', 'is_active', 'date_joined', 'is_staff')

admin.site.unregister(get_user_model())


admin.site.register(get_user_model(),UserDtailAdmin)

admin.site.register(UserDetail,UserDetailSearchAdmin)




def deactivate_selected(modeladmin, request, queryset):
    rows_updated = 0
    for details in queryset :
        user_model =  User.objects.filter(username=details.user)
        user_model.update(is_active=False)
        # user_model.save()
        rows_updated +=1
    # rows_updated = queryset.update(active=0)
    # for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 item was'
    else:
        message_bit = '%s items were' % rows_updated
    modeladmin.message_user(request, '%s successfully deactivated.' % message_bit)
deactivate_selected.short_description = "Deactivate selected items"




def ACTIVE_selected(modeladmin, request, queryset):
    rows_updated = 0
    for details in queryset :
        user_model =  User.objects.filter(username=details.user)
        user_model.update(is_active=True)
        # user_model.save()
        rows_updated +=1
    # rows_updated = queryset.update(active=0)
    # for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 个选项'
    else:
        message_bit = '%s 个选项' % rows_updated
    modeladmin.message_user(request, '%s 被成功激活.' % message_bit)
ACTIVE_selected.short_description = "批量激活选项"







def invalid_selected(modeladmin, request, queryset):
    rows_updated = 0
    # for details in queryset :
    #     user_model =  User.objects.filter(username=details.user)
    #     user_model.update(is_active=False)
    #     # user_model.save()
    #     rows_updated +=1
    rows_updated = queryset.update(role='invalid')
    for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 item was'
    else:
        message_bit = '%s items were' % rows_updated
    modeladmin.message_user(request, '%s 成功置为无效用户.' % message_bit)
invalid_selected.short_description = "置为无效用户"







def valid_selected(modeladmin, request, queryset):
    rows_updated = 0
    # for details in queryset :
    #     user_model =  User.objects.filter(username=details.user)
    #     user_model.update(is_active=False)
    #     # user_model.save()
    #     rows_updated +=1
    rows_updated = queryset.update(role='')
    for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 item was'
    else:
        message_bit = '%s items were' % rows_updated
    modeladmin.message_user(request, '%s 成功置为有效用户.' % message_bit)
valid_selected.short_description = "置为有效用户"







## add deactivates
admin.site.add_action(deactivate_selected)
admin.site.add_action(invalid_selected)
admin.site.add_action(valid_selected)
admin.site.add_action(ACTIVE_selected)