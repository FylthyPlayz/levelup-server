from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import DjangoModelPermissions
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    permission_classes = [ DjangoModelPermissions ]
    queryset = Game.objects.none()
    def retrieve(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            serializer = CreateGameSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(gamer=gamer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = CreateGameSerializer(game, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']