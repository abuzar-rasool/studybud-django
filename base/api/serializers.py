from rest_framework.serializers import ModelSerializer
from base.models import Room, Topic, User, Message


class UserSearializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']

    



class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'





class MessageSerializer(ModelSerializer):
    user = UserSearializer()

    class Meta:
        model = Message
        fields = ['id', 'message', 'created_at', 'user']
        kwargs = {'user': {'required': False, 'read_only': True}}

   


class RoomSerializer(ModelSerializer):
    participants = UserSearializer(many=True)
    host = UserSearializer()
    topic = TopicSerializer()

    class Meta:
        model = Room
        fields = '__all__'
