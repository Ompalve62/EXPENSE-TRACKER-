from django.shortcuts import render,redirect
from django.db.models import Sum
from .models import Expense
import datetime
from .forms import ExpenseForm
# Create your views here.
def index(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))

    #Logic for calculating total 365 days of expense
    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gte=one_year_ago)
    yearly_sum = data.aggregate(Sum('amount'))['amount__sum'] or 0
    

    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gte=last_month)
    monthly_sum = data.aggregate(Sum('amount'))['amount__sum'] or 0
 
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gte=last_week)
    weekly_sum = data.aggregate(Sum('amount'))['amount__sum'] or 0
 
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    # print(daily_sums)
    
    categorical_sum = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    print(categorical_sum)


    expense_form = ExpenseForm()

    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses, 'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum,'categorical_sum':categorical_sum})

def edit(request,id):
    expense=Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method=='POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,"myapp/edit.html",{'expense_form':expense_form})

def delete(request,id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
        return redirect('index')