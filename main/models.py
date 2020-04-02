from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# To do list class.

class ToDoList(models.Model):
    # 'related_name': the way we access from user to todolist is with that specified string
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Item class. Every item that is created belongs to a ToDoList (We are going to have items as a part of a todolist).
# That is what we are doing with 'models.ForeignKey'. We are creating a Todolist object inside the Class item.
# On delete says that when a ToDoList is deleted, all items that belong to it will also be deleted
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text