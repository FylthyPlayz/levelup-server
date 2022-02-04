from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, EventGamer, Gamer

class EventView(ViewSet):
    def retrieve(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            serializer = CreateEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(organizer=gamer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = CreateEventSerializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 1

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time']