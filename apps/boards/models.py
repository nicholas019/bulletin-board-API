from django.db import models


class Board(models.Model):
    title      = models.CharField(max_length=20)
    content    = models.CharField(max_length=200)
    writer     = models.CharField(max_length=30)
    password   = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "boards"