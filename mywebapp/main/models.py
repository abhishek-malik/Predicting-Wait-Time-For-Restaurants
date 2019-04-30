from django.db import models

# Create your models here.
class Restaurant(models.Model):
	restaurant_name = models.CharField(max_length=200)
	restaurant_distance = models.CharField(max_length=200)
	restaurant_rating = models.IntegerField()
	restaurant_wait = models.FloatField()
	restaurant_about = models.TextField(default="Nothing here to show.")
	restaurant_description = models.TextField(default="Nothing here to show.")
	restaurant_queue = models.IntegerField(default=0)
	restaurant_lat = models.FloatField(default=12.931641)
	restaurant_long = models.FloatField(default=79.136240)

	def __str__(self):
		return self.restaurant_name