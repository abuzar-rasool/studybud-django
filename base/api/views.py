from rest_framework.authtoken.models import Token
from rest_framework import serializers, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Message, User
from .serializers import RoomSerializer, MessageSerializer, UserSearializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class RoomMessagesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers_class = MessageSerializer


    def get_serializer(self, *args, **kwargs):
        return MessageSerializer(*args, **kwargs)

    def get_queryset(self):
        room = Room.objects.get(id=self.kwargs['pk'])
        return Message.objects.filter(room=room)

    def list(self, request, pk):
        room = Room.objects.get(id=pk)
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        room = Room.objects.get(id=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, room=room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Room.objects.all()
        else:
            return Room.objects.filter(participants=user)

    def perform_update(self, serializer):
        serializer.save(host=self.request.user)

    def perform_destroy(self, instance):
        instance.participants.clear()
        delete_messages = Message.objects.filter(room=instance)
        delete_messages.delete()
        instance.delete()


#create user viewset and get current logged in  user details
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSearializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

    def get_user(self, request):
        user = request.user
        serializer = UserSearializer(user, many=False)
        return Response(serializer.data)