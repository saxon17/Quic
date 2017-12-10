#coding=utf-8
import json
from collections import Counter

import simplejson as simplejson
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import  os
from  django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from .models import SeuMaster, UserDetail,RelationShip,WeiXinAccountLog
from  django.db.models import  Count
from  Quic import  settings
from  django.views import generic
from  django.http import Http404
from  django.views.generic.edit import  CreateView,UpdateView,DeleteView

from django.shortcuts import  render,redirect,get_object_or_404
from  django.contrib.auth import  authenticate,login,logout, get_user_model
from  django.contrib.auth.decorators import  login_required


from  django.views.generic import  View
from  .forms import  UserForm,UserDetailForm



from django.views.decorators.csrf import csrf_exempt
from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  .serializers import  UserDetail_Serializer,Weixin_UserDetail_Serializer,UserSerializer,WexinAccountSerializer


from  rest_framework.generics import  (
UpdateAPIView,
CreateAPIView)



from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

class ValidUserMixin(object):


    def dispatch(self,request,*args,**kwargs):
        cur_user_info_tuple = UserDetail.objects.values_list('name','college','hometown','head_pic').get(user=request.user)
        print '数据',cur_user_info_tuple,cur_user_info_tuple[-1]
        if None in  cur_user_info_tuple:
            print '测试试试!!!!', '用户填写资料不完整'
            messages.warning(request, '请填写有效信息,真诚交友,拒绝套路! NS将在5小时内帮您审核')
            return redirect('userdetail-update', request.user.id)
        if 'head' in cur_user_info_tuple[-1]:
            print '未上传本人真实头像'

            messages.warning(request, '请上传本人生活照,真诚交友,拒绝套路! NS将在5小时内帮您审核')



        if UserDetail.objects.get(user=request.user).role == "invalid":
            messages.warning(request, '请填写有效信息及上传本人生活照,真诚交友,拒绝套路! NS将在5小时内帮您审核')
            return redirect('userdetail-update' ,request.user.id)
         # if request.user.is_active == False:
         #     raise Http404("你由于没有填写真实信息,不能访问本网页,请及时修改您的资料,我们会抓紧审核。")


         # if request.user.id != self.get_object().user_id:
         #
         #     print '检测权限',request.user.id,  self.get_object().user_id
         #     print  '类型',type(request.user.id),type(self.get_object().user_id)
         #
         #     raise  PermissionDenied

        return  super(ValidUserMixin,self).dispatch(request,*args,**kwargs)


class FellowView(generic.ListView):
    template_name = 'fellow.html'
    context_object_name = 'fellow_list'

    paginate_by = 10

    # def get_queryset(self):
    #     return SeuMaster.objects.all()

    def get_queryset(self):
        city_search =  self.request.GET.get('q')
        print city_search
        if city_search:
            return SeuMaster.objects.filter(home__contains=city_search)
            # return  HttpResponse("hello")
        else:
            return SeuMaster.objects.filter()


class Boy_Girl_ListView(ValidUserMixin,generic.ListView):
    template_name = 'nsns.html'
    # context_object_name = 'all_user_list'

    def get_queryset(self):


            sex_from_query = self.request.GET.get('s')
            print sex_from_query
            if sex_from_query:

                # return UserDetail.objects.filter(sex=sex_from_query).exclude(name__isnull=True).exclude(name='0').exclude(name='1')
                return UserDetail.objects.filter(sex=sex_from_query).filter(user__is_active=True).exclude(head_pic="head-girl.png").exclude(role='invalid').order_by('-id')

                # return  HttpResponse("hello")
            else:

                # return UserDetail.objects.exclude(name__isnull=True).exclude(name='0').exclude(name='1').exclude(head_pic="head-girl.png")
                return   UserDetail.objects.filter(user__is_active=True).exclude(head_pic="head-girl.png").exclude(role='invalid').order_by('-id')




class UserAuthorMixin(object):


    def dispatch(self,request,*args,**kwargs):



         # if request.user.is_active == False:
         #     raise Http404("你由于没有填写真实信息,不能访问本网页,请及时修改您的资料,我们会抓紧审核。")


         if request.user.id != self.get_object().user_id:

             print '检测权限',request.user.id,  self.get_object().user_id
             print  '类型',type(request.user.id),type(self.get_object().user_id)

             raise  PermissionDenied

         return  super(UserAuthorMixin,self).dispatch(request,*args,**kwargs)
















class UserDetailView(generic.DetailView):
    template_name = 'detail.html'
    model = UserDetail
    # a small trick  let django consider the user_id(foreign key) as a slug_field
    slug_field =  "user_id"


    def dispatch(self,request,*args,**kwargs):

         if request.user.id != self.get_object().user_id:

            self.template_name = 'recommend.html'

         return super(UserDetailView, self).dispatch(request, *args, **kwargs)


def stuDetail(request, fellow_id):
    # try:
    #     stu = SeuMaster.objects.get(pk=fellow_id)
    # except SeuMaster.DoesNotExist:
    #     raise Http404("User does not exist")
    stu = get_object_or_404(SeuMaster, pk=fellow_id)
    return render(request, 'detail.html', {'stu': stu})

    # def detail(request,fellow_id):
    #     return HttpResponse("<h2>details"+str(fellow_id)+ " to be like</h2> for fellow" )





def Community(request):
    # user = get_object_or_404(UserDetail, pk=user_id)
    return render(request, 'Community.html')


def Edit_user_info(request):
    if request.method == 'GET':

        res_json = {'isExist':'False'}
        try:
            userID = request.GET.get('userID')
            userexist = UserDetail.objects.get(user=userID)
            res_json['isExist'] = 'True'
            return JsonResponse(res_json)
        except UserDetail.DoesNotExist:
            return JsonResponse(res_json)
        # userID=request.GET.get('userID')
        # user = get_object_or_404(UserDetail,)







class UserDetailCreate(CreateView):
    model =  UserDetail
    fields = ['name','college','major','age',
              'hometown','xingzuo','hobbie','we_chat','head_pic']



class UserDetailUpdate(UserAuthorMixin,UpdateView):
    slug_field = 'user_id'

    form_class =  UserDetailForm
    # this is the arg catched in the url
    slug_url_kwarg = 'user_id'
    model =  UserDetail
    # fields = ['name','college','major','age',
    #           'hometown','xingzuo','hobbie','we_chat','head_pic']

    template_name = 'WeiXinFormTemplate.html'

class WeiXin_UserDetailUpdate(UpdateView):
    # slug_field = 'user_id'

    form_class =  UserDetailForm
    # this is the arg catched in the url
    # slug_url_kwarg = 'user_id'
    model =  UserDetail
    template_name = 'WeiXinFormTemplate.html'
    success_url = '/weixin-success'
    def get_object(self):
        try:
            token = Token.objects.get(key=self.kwargs['token'])

        except Token.DoesNotExist:
            raise Http404("您没有权限访问")

        # print UserDetail.objects.get(user_id=token.user_id)
        return UserDetail.objects.get(user_id=token.user_id)


    # def dispatch(self, request, *args, **kwargs):
    #         try:
    #             token = Token.objects.get(key=self.kwargs['token'])
    #             slug_url_kwarg = token.user_id
    #             return super(WeiXin_UserDetailUpdate, self).dispatch(request, *args, **kwargs)
    #         except Token.DoesNotExist:
    #             raise Http404("您没有权限访问")
    #         else:
    #             raise  PermissionDenied








class UserFormView(View):
     from_class = UserForm
     template_name = 'registration_form.html'

     #display blank form
     def  get(self,request):
         form = self.from_class(None)
         return render(request,self.template_name,{'form':form})

     #process form data
     def post(self,request):
         form = self.from_class(request.POST)

         if  form.is_valid():
             # block it  to memory not to database
             user = form.save(commit=False)

             #cleaned (normalized) data

             username = form.cleaned_data['username']
             password = form.cleaned_data['password']
             user.set_password(password)

             user.save()

             #return User Objects if credentials are correct
             user = authenticate(username= username,password=password)

             if  user is  not None:

                 if  user.is_active:

                     login(request,user)
                     return  redirect('userdetail-update',user.id)

         return render(request, self.template_name, {'form': form})



# all-ns-ns/
class UserDetailList(APIView):

    def get(self,request):

        q_sex = request.GET.get('s')

        UserDetails = UserDetail.objects.filter(sex=q_sex).filter(user__is_active=True).exclude(head_pic="head-girl.png").exclude(role='invalid')
        serializer = UserDetail_Serializer(UserDetails,many=True)

        return Response(serializer.data)

class UserDetailWeiXin(UpdateAPIView):
    queryset =  UserDetail.objects.all()
    lookup_url_kwarg = 'update_userid'
    serializer_class = Weixin_UserDetail_Serializer

    lookup_field = 'user_id'


    # def dispatch(self, request, *args, **kwargs):
    #         token = Token.objects.get(key=self.kwargs['token'])
    #         if token:
    #
    #             return super(UserDetailView, self).dispatch(request, *args, **kwargs)
    #         else:
    #             raise  PermissionDenied
    # def get(self,request):

    #
    #     q_sex = request.GET.get('s')
    #
    #     UserDetails = UserDetail.objects.filter(sex=q_sex)
    #     serializer = UserDetail_Serializer(UserDetails,many=True)
    #
    #     return Response(serializer.data)


def check_Activate(request):
        json_response = {'active_status': 'False'}

        if request.method == 'GET':



            try:
                check_id = request.GET.get('check_id')
                user = User.objects.get(id=int(check_id))

                print user,"激活否:",user.is_active

                json_response['active_status'] = user.is_active
                return  JsonResponse(json_response)



            except  User.DoesNotExist:
                raise Http404("您查找的用户不存在")











def Login(request):
    # if value of next does exist return the varible in the url('next =?')
    # else return next=/home

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('nsns'))


    next_page_url = request.GET.get('next','/nsns/')
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)

                # 登陆后直接 跳转到下一条的地址
                return  HttpResponseRedirect(next_page_url)
            else:
                HttpResponse("Inactive user.")
        else:
            return  HttpResponseRedirect(settings.LOGIN_URL)



    return  render(request,"login.html",{'redirect_to':next_page_url})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


def Home(request):
    Basedir = settings.BASE_DIR
    Tempdir = os.path.join(settings.BASE_DIR, 'NS/templates')
    return  render(request,"home.html",{'Basedir':Basedir,'Temp':Tempdir})

def Blog(request):
    TT = request
    TT2 = request.path
    # TT3 = request.body
    request_path =  request.path
    return  render(request,"Blog.html",{'request_path':request_path})



@login_required
@csrf_exempt
def like_some(request):

    want_to_like = None
    if request.method == 'POST':
        she_id = request.POST['want_to_like']
        print request.user.id,she_id


    # islikes = 0

    relationSet= RelationShip.objects.filter(user=request.user).filter(likeID=she_id)
    print relationSet
    if len(relationSet)>0:
        # print relationSet
        print   '关系存在'
        relationSet.delete()

    else:
        # print '数据集',len(relationSet),relationSet
        print  '开始插入数据'
        newObj = RelationShip(user=request.user,likeID=she_id)
        newObj.save()

        relationSet = {"status":'ok'}
        # if cat:
        #     likes = cat.likes + 1
        #     cat.likes =  likes
        #     cat.save()

    return HttpResponse(relationSet)




@login_required
def get_all_user_like_count(request):
    res_json = {}
    want_to_like = None
    if request.method == 'GET':
       all_id_count =  RelationShip.objects.all().values('likeID').annotate(total = Count('likeID')).order_by('likeID')

       for item in all_id_count:
           res_json['userID_'+str(item['likeID'])] = item['total']
       # print all_id_count
    # islikes = 0


    return JsonResponse(res_json)




@login_required
def getLoginUserLove(request):
    res_json = {}

    if request.method == 'GET':
       all_id_he_love =  RelationShip.objects.filter(user=request.user)
       print 'ak',all_id_he_love
       for ix,item in enumerate(all_id_he_love):
            res_json['current_user_loves_'+str(ix)] = item.likeID




    return JsonResponse(res_json)




@login_required
def getWhoLoveUser(request):
    res_json = {}

    if request.method == 'GET':

       PLoveUser =  RelationShip.objects.filter(likeID=request.user.id)
       print 'PeopleLoveUser:',PLoveUser
       if len(PLoveUser)>0:
           for ix,item in enumerate(PLoveUser):
                print 'item',item.user.id
                ploveUser =  UserDetail.objects.filter(user = item.user)
                print ploveUser
                print "xingming",ploveUser[0].name
                res_json[ploveUser[0].user.id]  = [ploveUser[0].name,ploveUser[0].major,ploveUser[0].hometown,ploveUser[0].head_pic.url]




    return JsonResponse(res_json)



@login_required
def getUserLoveDetail(request):
    res_json = {}

    if request.method == 'GET':
       all_id_he_love =  RelationShip.objects.filter(user=request.user)
       # print 'ak',all_id_he_love
       for ix,item in enumerate(all_id_he_love):
           UserLoverWho =  UserDetail.objects.filter(user = item.likeID)

           # print "你喜欢的是",UserLoverWho[0].name
           if UserLoverWho:
                res_json[UserLoverWho[0].user.id]  = [UserLoverWho[0].name,
                                                 UserLoverWho[0].major,UserLoverWho[0].hometown,
                                                 UserLoverWho[0].head_pic.url]



    return JsonResponse(res_json)




@login_required
def getLoverMatched(request):
    res_json = {}

    if request.method == 'GET':
       all_id_he_love =  RelationShip.objects.filter(user=request.user)
       PLoveUser = RelationShip.objects.filter(likeID=request.user.id)
       PLoveUserReverse_Lst = []
       UserLoveP_Lst = []
       for p in all_id_he_love:
           UserLoveP_Lst.append(str(p.user.id)+'->'+str(p.likeID))

       for P in PLoveUser:
         PLoveUserReverse_Lst.append(str(P.likeID)+'->'+str(P.user.id))

       match_lover_id_lst = []
       for match in set(UserLoveP_Lst)&set(PLoveUserReverse_Lst):
           match_lover_id_lst.append(int(match.split('->')[1]))

       # json_dict = {}
       # json_dict["matched_id"] = match_lover_id_lst



       for ix,item in enumerate(match_lover_id_lst):
           match_p =  UserDetail.objects.filter(user = item)


           res_json[match_p[0].user.id]  = [match_p[0].name,
                                            match_p[0].we_chat,
                                            match_p[0].head_pic.url]
       # for ix,item in enumerate(all_id_he_love):
       #     UserLoverWho =  UserDetail.objects.filter(user = item.likeID)
       #
       #     print "你喜欢的是",UserLoverWho[0].name
       #     res_json[UserLoverWho[0].user.id]  = [UserLoverWho[0].name,UserLoverWho[0].major,UserLoverWho[0].hometown,UserLoverWho[0].head_pic.url]



    return JsonResponse(res_json)




class WeixinUpdatePageView(TemplateView):
    template_name = "weixin_update.html"

    def get_context_data(self, **kwargs):
        context = super(WeixinUpdatePageView, self).get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        context['user_token']  = self.kwargs['token']
        try:
            token = Token.objects.get(key=self.kwargs['token'])

        except Token.DoesNotExist:
            raise Http404("您没有权限访问")

        # if not token:
        #     raise  PermissionDenied

        context['UserID'] = token.user_id
        return context

    # def dispatch(self, request, *args, **kwargs):
    #         token = Token.objects.get(key=self.kwargs['token'])
    #         if token:
    #
    #             return super(UserDetailView, self).dispatch(request, *args, **kwargs)
    #         else:
    #             raise  PermissionDenied







    # def get(self, request):
    #     token = request.GET.get('token')
    #     print token
    #     user = Token.objects.get(token=token)
    #     print user
    #     user.backend = 'django.contrib.auth.backends.ModelBackend'
    #     login(request, user)



class SuccessView(TemplateView):
    template_name = "weixin_success.html"




class CreateUserView(CreateAPIView):
     model = get_user_model()
     # permission_classes = AllowAny
     serializer_class =  UserSerializer

     def dispatch(self, request, *args, **kwargs):

         if self.kwargs['superToken']  != '7788':
             raise Http404("您没有权限访问")

         else:
            return super(CreateUserView, self).dispatch(request, *args, **kwargs)


class WechatAccountLogView(CreateAPIView):
    model =  WeiXinAccountLog
    # permission_classes = AllowAny
    serializer_class =  WexinAccountSerializer

    def dispatch(self, request, *args, **kwargs):

        if self.kwargs['superToken'] != '7788':
            raise Http404("您没有权限访问")

        else:
            return super(WechatAccountLogView, self).dispatch(request, *args, **kwargs)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})








def weixin_superuserToken_get_id(request):
    res_json = {}
    want_to_like = None
    if request.method == 'GET':
       Query_Token = request.GET.get('superToken')
       Query_id = request.GET.get('wchat_uid')

       if Query_Token == Token.objects.get(user=1).key:
           res_json = {'real_uid':Token.objects.get(user_id=Query_id).key}
           return JsonResponse(res_json)
       else:
           raise Http404("您没有权限访问,超级Token错误")
    # islikes = 0



def  province_data_vitualiazation(request):
        import  collections
        # province_as_json = serializers.serialize('json', UserDetail.objects.values_list('hometown'))
        province_vlist = UserDetail.objects.values_list('hometown')

        provinceDict = []

        # [{name:  count:}]
        single_obj = []
        for P in province_vlist:
            if P[0] not in [None,'1','0']:
                # print P[0].decode('utf8')[:2]
                provinceDict.append(P[0].decode('utf8')[:2])

        cnt = Counter(provinceDict)


        for k,v in cnt.items():
            single_obj.append( {'name':k,'value':v})


        return HttpResponse( simplejson.dumps(single_obj), content_type='application/json')


        # return HttpResponse(province_as_json, content_type='json')

class MapPageView(TemplateView):
    template_name = "map.html"



