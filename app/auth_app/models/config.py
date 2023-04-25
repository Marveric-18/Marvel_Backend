from djongo import models

config_choices = [
    ("APP", "APP"),
    ("USER", "USER")
]

class U_Config(models.Model):
    id = models.AutoField(primary_key= True)
    config_name = models.CharField(max_length=100, verbose_name = 'Config Name')
    config_value = models.CharField(max_length=100, verbose_name = 'Config Value')
    config_type = models.CharField(max_length=100, verbose_name = 'Config Type')
    description = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, choices= config_choices, default="APP")
    is_active = models.BooleanField(default=True)
    valid_till = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.config_name
    
    class Meta:
        verbose_name = "U_Config"