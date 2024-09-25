from django.db import models

# Create your models here.
class TrafficLight(models.Model):
    # id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField()
    preset_condition = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Traffic Light {self.ip_address} - Preset: {self.preset_condition}"
    


