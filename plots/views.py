from django.shortcuts import render
from plotly.offline import plot
from .models import expenses
from .forms import CreateNewExpense
from datetime import datetime
import re
from django.http import HttpResponse, HttpResponseRedirect
from plotly.graph_objs import Scatter
from django.utils import timezone


# Create your views here.

def plotting(response):

    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')],
                    output_type='div')
    all_expenses = response.user.expenses.values_list('month','amount')
    months = set(response.user.expenses.values_list('month'))
    months = list(months)
    # r = re.compile("'(.*?)'")
    # months = list(filter(r.match, str(months)))
    #final_expenses=[]
    print(months)
    for month in months:
        print(month)
        # for item in all_expenses:
        #     for element in item:
        #         print(element)
                # if element == month:
                #     final_expenses[month]= final_expenses[month]+(element+1)

    # print(final_expenses[0])

    #print(all_expenses)
    last_ten_expenses = response.user.expenses.all().order_by('-id')[:10]
    if response.method == "POST":
        form = CreateNewExpense(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            a = form.cleaned_data["amount"]
            m = form.cleaned_data["month"]
            date_ = datetime.now()
            e = expenses(name=n, amount=a, month=m, added_date= date_)
            e.save()
            response.user.expenses.add(e)
            form = CreateNewExpense()
            last_ten_expenses = response.user.expenses.all().order_by('-id')[:10]
            # print(last_ten_expenses)
            return render(response, "plots/plotting.html",{"form": form,
                                                    'plot_div': plot_div,
                                                    'last_ten_expenses': last_ten_expenses
                                                    })
    else:
        form = CreateNewExpense()


    # print(last_ten_expenses)
    return render(response, "plots/plotting.html", {'form': form,
                                                    'plot_div': plot_div,
                                                    'last_ten_expenses': last_ten_expenses})







