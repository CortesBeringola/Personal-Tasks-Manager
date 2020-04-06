from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList


# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    if ls in response.user.todolist.all():
        # Custom forms
        if response.method == "POST":
            # if they have clicked 'save' button 'response.POST method will return a dictionary will all the 'name'
            #  values as keys and 'values' as values of the dict
            # {'save': ["save"],
            #  'c1': ["clicked"]}
            # You can see it if you 'print(request.POST)'
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("Invalid")
        return render(response, "main/list.html", {"ls": ls})
    else:
        return render(response, "main/view.html", {})



def home(response):
    return render(response, "main/home.html",  {})



def create(response):
    # Simple forms
    if response.method == "POST":
        # grabs all the information submitted in the form wraps it, encrypts it and saves it in 'form'. No we can start
        # validating all this data or manipulating it.
        form = CreateNewList(response.POST)
        if form.is_valid():
            # '.cleaned_data' method gets the encrypted submitted info, decrypts it and leaves it clean and ready
            #  to use. You just need to specify which variable of the form you want have access to. Below I save
            # in 'n' the 'name' value of the submitted form which corresponds to the ToDoList name
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
            # After saving I'm redirecting so as to see the list
            return HttpResponseRedirect("/view")
    else:
        form = CreateNewList()
    return render(response, "main/view.html", {"form": form})
