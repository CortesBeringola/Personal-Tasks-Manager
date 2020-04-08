from django.db import models
from django.contrib.auth.models import User


MONTH_CHOICES = (('Jan','Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'),
                 ('Jul', 'Jul'),('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec'))

class expenses(models.Model):
    # 'related_name': the way we access from user to todolist is with that specified string
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses", null=True)
    name = models.CharField(max_length=200)
    amount = models.FloatField(default=0)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    added_date = models.DateField()

    def __str__(self):
        return self.name