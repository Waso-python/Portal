from django.db import models
from django.contrib.auth.models import User


class ProfileUserModel(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    keys = models.JSONField()

    def get_format(self):
        form_value = self.keys
        for elem in form_value:
            if isinstance(type(form_value[elem]), type([])):
                form_value[elem] = ', '.join(form_value[elem])
        return form_value
