#coding=utf-8
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse

from .models import SeuMaster, UserDetail,RelationShip,WeiXinAccountLog
def getUserLoveDetail(request):
    res_json = {}

    if request.method == 'GET':


       s_token = request.GET.get('super_password')

       if s_token!= '7788':
           raise Http404("您没有权限访问,超级Token错误")
       else:
           q_uid = request.GET.get('query_id')
           all_id_he_love =  RelationShip.objects.filter(user=q_uid)
           # print 'ak',all_id_he_love
           for ix,item in enumerate(all_id_he_love):
               UserLoverWho =  UserDetail.objects.filter(user = item.likeID)

               # print "你喜欢的是",UserLoverWho[0].name
               if UserLoverWho:
                    res_json[UserLoverWho[0].user.id]  = [UserLoverWho[0].name,
                                                     UserLoverWho[0].major,UserLoverWho[0].hometown,
                                                     UserLoverWho[0].head_pic.url]



    return JsonResponse(res_json)




def getWhoLoveUser(request):
    res_json = {}


    if request.method == 'GET':
        print '已在查谁喜欢本ID'

        s_token = request.GET.get('super_password')

        if s_token != '7788':
            raise Http404("您没有权限访问,超级Token错误")


        else:
           q_uid = request.GET.get('query_id')

           PLoveUser =  RelationShip.objects.filter(likeID=q_uid)
           print 'PeopleLoveUser:',PLoveUser
           if len(PLoveUser)>0:
               for ix,item in enumerate(PLoveUser):
                    print 'item',item.user.id
                    ploveUser =  UserDetail.objects.filter(user = item.user)
                    print ploveUser
                    print "xingming",ploveUser[0].name
                    res_json[ploveUser[0].user.id]  = [ploveUser[0].name,ploveUser[0].major,ploveUser[0].hometown,ploveUser[0].head_pic.url]




    return JsonResponse(res_json)









def getLoverMatched(request):
       res_json = {}


       if request.method == 'GET':
        print '开始查询ID的匹配对象'

        s_token = request.GET.get('super_password')

        if s_token != '7788':
            print s_token
            raise Http404("您没有权限访问,超级密码错误")
        else:
           q_uid = request.GET.get('query_id')


           all_id_he_love =  RelationShip.objects.filter(user=q_uid)
           PLoveUser = RelationShip.objects.filter(likeID=q_uid)
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



       return JsonResponse(res_json)





def like_some(request):
    res_json = {"status": 'fail'}

    if request.method == 'GET':



        s_token = request.GET.get('super_password')

        if s_token!='7788':
            raise Http404("您没有权限访问,超级Token错误")
        else:

            she_id = request.GET.get('want_to_like')
            u_id = request.GET.get('alias_id')

            relationSet= RelationShip.objects.filter(user_id=u_id).filter(likeID=she_id)
            print relationSet
            if len(relationSet)>0:
                # print relationSet
                print   '关系存在,正在删除'
                relationSet.delete()
                res_json["status"] = 'delet'

            else:
                # print '数据集',len(relationSet),relationSet
                print  '开始插入数据'
                newObj = RelationShip(user_id=u_id,likeID=she_id)
                newObj.save()

                res_json["status"] ='create'
                # if cat:
                #     likes = cat.likes + 1
                #     cat.likes =  likes
                #     cat.save()

    return JsonResponse(res_json)

