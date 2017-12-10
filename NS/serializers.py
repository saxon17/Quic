from  rest_framework import serializers

from .models import UserDetail,WeiXinAccountLog
from  django.contrib.auth import  get_user_model

class UserDetail_Serializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()
    xingzuo =  serializers.SerializerMethodField()
    grade =  serializers.SerializerMethodField()
    class Meta:
        model = UserDetail

        # fields = ('')
        fields = '__all__'

    def get_sex(self, obj):
        return obj.get_sex_display()

    def get_xingzuo(self, obj):
        return obj.get_xingzuo_display()
    def get_grade(self, obj):
        return obj.get_grade_display()






class Weixin_UserDetail_Serializer(serializers.ModelSerializer):
    # sex = serializers.SerializerMethodField()
    # xingzuo =  serializers.SerializerMethodField()
    # grade =  serializers.SerializerMethodField()
    class Meta:
        model = UserDetail

        # fields = ('')
        fields = ('sex','xingzuo','grade','name','college','major',
                  'hometown','hobbie','we_chat','head_pic',
                  )



class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username =validated_data ['username']
        )


        user.set_password(validated_data['password'])

        user.save()
        return  user


    class Meta:

            model = get_user_model()
            fields = ('username','password')




class WexinAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeiXinAccountLog

        # fields = ('')
        fields = '__all__'