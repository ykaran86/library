from django.db import models

class Dialog(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    user1 = models.CharField(max_length=200, default = "Client")
    user2 = models.CharField(max_length=200, default= "toComputer")
    query = models.CharField(max_length=300, null=True)
    
    def __unicode__(self):
        return self.query
    
    def __str__(self):
        return self.query
