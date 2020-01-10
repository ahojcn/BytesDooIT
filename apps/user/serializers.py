from rest_framework import serializers

from user.models import User, UserAuthority


class UserSerializer(serializers.ModelSerializer):

    def get_username(self, obj):
        # print(obj)  # User obj
        return 1

    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_num',
            'gender',
            'description',
            'avatar_path',
            'level',
            'exp_val',
            'food_num',
        )


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
