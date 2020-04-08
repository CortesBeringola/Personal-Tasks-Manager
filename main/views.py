from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from plots.views import make_a_list, plotting
from plots.models import expenses
from django.db.models import Sum
import re
import datetime



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
    if response.user.is_anonymous:
        return render(response, "main/home.html", {"active_todos": 0,
                                                   "current_month": "April",
                                                   "current_expense": 0,
                                                   "total_expense": 0})
    else:
        active_todos = response.user.todolist.count()
        current_finance = make_a_list(response)
        current_month = current_finance[int(datetime.datetime.now().strftime("%m"))-1][0]
        current_expense = current_finance[int(datetime.datetime.now().strftime("%m"))-1][1]
        total_expense = response.user.expenses.all().aggregate(Sum('amount'))
        total_expense = re.search(":(.*?)}", str(total_expense)).group(1)
        plot_div = plotting(response,current_finance)
        x_data, y_data = map(list, zip(*current_finance))
        return render(response, "main/home.html",  {"active_todos": active_todos,
                                                    "current_month": current_month,
                                                    "current_expense": current_expense,
                                                    "total_expense": total_expense,
                                                    'plot_div': plot_div,
                                                    'x_data': x_data,
                                                    'y_data': y_data})



def create(response):
    # Simple forms
    if response.method == "POST":
        if response.user.is_anonymous:
            return HttpResponseRedirect("/view")
        else:
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
