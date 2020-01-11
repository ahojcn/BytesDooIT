from django.conf import settings
from rest_framework import serializers

from user.models import User, UserAuthority


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'email',
            'gender',
            'description',
            'phone_num',
            'reg_datetime',
            'avatar_path',
            'last_login_datetime',
            'level',
            'exp_val',
            'food_num',
            'is_mute',
            'is_active',
            'extra_data',
        )

    avatar_path = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.id

    def get_avatar_path(self, obj):
        return settings.BASE_WEB_URL + obj.avatar_path

    def get_gender(self, obj):
        return User.USER_GENDER_CHOICES[obj.gender][1]


class UserAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthority
        fields = (
            'video',
            'post',
            'resume',
            'live',
            'recruitment',
            'comment',
            'interview',
            'extra_data',
        )
