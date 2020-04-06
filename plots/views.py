from django.shortcuts import render
from plotly.offline import plot
from .models import expenses
from .forms import CreateNewExpense
from datetime import datetime
import re
from django.http import HttpResponse, HttpResponseRedirect
from plotly.graph_objs import Bar
from django.utils import timezone


# Create your views here.

def make_a_list(response):
    all_expenses = response.user.expenses.values_list('month', 'amount')
    months = set(response.user.expenses.values_list('month'))
    months = list(months)

    new_months = []

    for month in months:
        new_months.append(re.search("'(.*?)'", str(month)).group(1))

    final_expenses = []

    for index, month in enumerate(new_months):
        final_expenses.append([])
        for j in range(2):
            if j == 0:
                final_expenses[index].append(month)
            else:
                final_expenses[index].append(0)

    for index, month in enumerate(new_months):
        for item in all_expenses:
            for idx, element in enumerate(item):
                if element == month:
                    final_expenses[index][1] += item[idx + 1]

    return final_expenses


def plotting(final_expenses):

    x_data, y_data = map(list, zip(*final_expenses))

    plot_div = plot([Bar(x=x_data, y=y_data, marker_color ="#f2722c", hovertext=['27% market share', '24% market share', '19% market share'])],
                    output_type='div')

    return plot_div

def finance(response):


    final_expenses = make_a_list(response)
    plot_div = plotting(final_expenses)


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
            final_expenses = make_a_list(response)
            plot_div = plotting(final_expenses)
            return render(response, "plots/plotting.html", {"form": form,
                                                            'plot_div': plot_div,
                                                            'last_ten_expenses': last_ten_expenses})
    else:
        form = CreateNewExpense()
    return render(response, "plots/plotting.html", {'form': form,
                                                    'plot_div': plot_div,
                                                    'last_ten_expenses': last_ten_expenses})








