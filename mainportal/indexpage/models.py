from random import choices
from statistics import mode
from django.db import models

# Create your models here.
class Order(models.Model):
    ACTUAL_ANSWER = (
		(0, 'не актуально'),
  		( 1,'актуально')
	)
    num_proc = models.CharField(max_length=10,null=False)
    link_proc = models.CharField(max_length=500, null=False)
    partner = models.CharField(max_length=512, null=False)
    summ_proc = models.IntegerField(null=False)
    count_order = models.IntegerField(null=False)
    subj_proc = models.CharField(max_length=512)
    actual_for_me = models.IntegerField(choices = ACTUAL_ANSWER)
    end_date = models.DateTimeField()
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.subj_proc} until {self.end_date}'
    