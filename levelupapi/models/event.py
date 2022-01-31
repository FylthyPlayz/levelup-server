from django.db import models

class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(auto_now_add=False, auto_now=False)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)