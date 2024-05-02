from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, CustomerProfileForm, ContractorProfileForm
from .models import Contractor, Customer


def home(request):
    return render(request, 'main/home.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "you were logged in")
            return redirect('home')
        else:
            messages.error(request, "Username or password are invalid")
            return redirect('login')
    else:
        return render(request, 'main/login.html', {})


def register_user(request):
    form = CreateUserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'New profile was created for ' + user)
            return redirect('login')

    return render(request, 'main/register_user.html', {
        'form': form,
    })


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.success(request, "you were logged out")
    return redirect('home')


@login_required(login_url="login")
def customer_profile(request):
    error = ''
    if not Customer.objects.filter(user=request.user).exists(): # если форма никогда не заполнялась:
        if request.method == 'POST':
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                new_customer = form.save(commit=False) #задерживаем сохранение
                new_customer.user = request.user #назначаем конкретного юзера конкретному профилю
                new_customer.save()
                return redirect('customer_profile')
            else:
                error = 'Форма содержит ошибки:'
                context = {
                    'form': form,
                    'error': error,
                }
                return render(request, 'main/customer_profile.html', context)
        else:
            form = CustomerProfileForm()  # вернём страницу с формой при GET запросе или ошибке валидации формы
            context = {
                'form': form,
                'error': error,
            }
            return render(request, 'main/customer_profile.html', context)
    else:
        customer = Customer.objects.get(user=request.user)  # если форма существует, мы запрашиваем её по ключу user
        context = {
            'error': error,
            'customer': customer,
            }
        return render(request, 'main/customer_profile.html', context)


@login_required(login_url="login")
def contractor_profile(request): # комментарии соответсвуют функции выше
    error = ''
    if not Contractor.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            form = ContractorProfileForm(request.POST)
            if form.is_valid():
                new_contractor = form.save(commit=False)
                new_contractor.user = request.user
                new_contractor.save()
                return redirect('contractor_profile')
            else:
                error = 'Форма содержит ошибки:'
                context = {
                    'form': form,
                    'error': error,
                }
                return render(request, 'main/contractor_profile.html', context)
        else:
            form = ContractorProfileForm()
            context = {
                'form': form,
                'error': error,
            }
            return render(request, 'main/contractor_profile.html', context)
    else:
        contractor = Contractor.objects.get(user=request.user)
        context = {
            'error': error,
            'contractor': contractor,
            }
        return render(request, 'main/contractor_profile.html', context)


@login_required(login_url="login")
def customer_profile_update(request):
    customer = Customer.objects.get(user=request.user)  # получаем объект с данными для конкретного юзера по ключу user
    form = CustomerProfileForm(request.POST or None, instance=customer)  # подсовываем в форму эти данные
    if form.is_valid():
        form.save()
        return redirect('customer_profile')
    return render(request, 'main/customer_update.html', {'form': form})


@login_required(login_url="login")
def contractor_profile_update(request):  # комментарии соответсвуют функции выше
    contractor = Contractor.objects.get(user=request.user)
    form = ContractorProfileForm(request.POST or None, instance=contractor)
    if form.is_valid():
        form.save()
        return redirect('contractor_profile')
    return render(request, 'main/contractor_update.html', {'form': form})
