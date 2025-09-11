
from django.db import models

class EU_Countries(models.Model):
    id = models.AutoField(primary_key=True)  # Ensure this matches your DB schema
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False  # This prevents Django from creating or modifying this table
        db_table = "EU_Countries"  # Exact table name in the database

class EU_Parties(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = "EU_Parties"

class EU_Parliament_Seats(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(EU_Countries, on_delete=models.CASCADE, db_column="country_id")
    party = models.ForeignKey(EU_Parties, on_delete=models.CASCADE, db_column="party_id")
    seats = models.IntegerField()

    class Meta:
        managed = False
        db_table = "EU_Parliament_Seats"

class Post(models.Model):
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    fake_news_technique = models.CharField(max_length=100)
    counter_fake_news_technique = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)