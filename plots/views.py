from django.shortcuts import render
from idna import unicode
from plotly.offline import plot
from .models import expenses
from .forms import CreateNewExpense
import datetime
import re
from django.http import HttpResponse, HttpResponseRedirect
from plotly.graph_objs import Bar
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from .utils import render_to_pdf




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

    final_expenses_v02 = order_by_month(final_expenses)

    return final_expenses_v02

def order_by_month(final_expenses):
    final_expenses_v02 = [['Jan', 0.00], ['Feb', 0.00], ['Mar', 0.00], ['Apr', 0.00], ['May', 0.00], ['Jun', 0.00],
                 ['Jul', 0.00], ['Aug', 0.00], ['Sep', 0.00], ['Oct', 0.00], ['Nov', 0.00], ['Dec', 0.00]]
    for index0, item0 in enumerate(final_expenses_v02):
        for index1, item1 in enumerate(item0):
            for index2, item2 in enumerate(final_expenses):
                for index3, item3 in enumerate(item2):
                    if item1 == item3:
                        final_expenses_v02[index0][1] = final_expenses[index2][1]
    return final_expenses_v02



def plotting(response, final_expenses_v02):
    if len(response.user.expenses.values_list('amount')) == 0:
        plot_div = []
        return plot_div
    else:
        x_data, y_data = map(list, zip(*final_expenses_v02))
        plot_div = plot([Bar(x=x_data, y=y_data, marker_color ="#f2722c", hovertext=['27% market share', '24% market share', '19% market share'])],
                        output_type='div')
        return plot_div

def finance(response):
    # If user is anonymous show everything empty
    if response.user.is_anonymous:
        form = CreateNewExpense()
        final_expenses_v02 = [['Month', 0.00]]
        return render(response, "plots/plotting.html", {'form': form,
                                                        })
    else:
        id_month = response.GET.get('id_month')
        id2_month = response.GET.get('id2_month')
        final_expenses_v02 = make_a_list(response)
        plot_div = plotting(response, final_expenses_v02)
        form = CreateNewExpense()
        user_id = response.user.id
        report_info_data = report_info(response, plot_div)
        last_ten_expenses = response.user.expenses.all()
        # Check if filter field is empty or not
        if id_month != '' and id_month is not None:
            last_ten_expenses = last_ten_expenses.filter(month__icontains=id_month).order_by('-id')[:20]
        elif id2_month != '' and id2_month is not None:
            last_ten_expenses = last_ten_expenses.filter(month__icontains=id2_month).order_by('-id')[:20]
        else:
            last_ten_expenses = response.user.expenses.all().order_by('-id')[:20]

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
                return HttpResponseRedirect('/plotting/')

        return render(response, "plots/plotting.html", {'form': form,
                                                        'plot_div': plot_div,
                                                        'last_ten_expenses': last_ten_expenses,
                                                        'report_info_data': report_info_data,

                                                        })

def report_info(response,plot_div):

    report_info_data = {
        'report_user': response.user.id,
        'report_username': response.user,
        'report_useremail': response.user.email,
        'report_year': int(datetime.datetime.today().year),
        'report_month': int(datetime.datetime.today().month),
        'report_date': int(datetime.datetime.today().day),
        'report_hour': int(datetime.datetime.today().hour),
        'report_minute': int(datetime.datetime.today().minute),
        'last_ten_expenses': response.user.expenses.all().order_by('-id')[:10],
        'plot_div': plot_div,
    }

    return report_info_data


class ChartData(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, response, format=None):
        user = unicode(response.user.id)
        final_expenses_v02 = make_a_list(response)
        x_data, y_data = map(list, zip(*final_expenses_v02))
        data = {
            "labels": x_data,
            "chartdata": y_data,
        }
        return Response(data)

class GeneratePdf(View):
    def get(self, response, *args,**kwargs):
        final_expenses_v02 = make_a_list(response)
        plot_div = plotting(response, final_expenses_v02)
        report_info_data = report_info(response,plot_div)
        pdf = render_to_pdf('plots/reports.html', report_info_data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Hi"
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
