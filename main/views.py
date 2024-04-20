from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, CustomerProfileForm, ContractorProfileForm
from .models import CustomerFormStatus, ContractorFormStatus, Contractor, Customer


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
    user_form_status, created = CustomerFormStatus.objects.get_or_create(user=request.user)  # получаем статус формы для юзера
    customer = None
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)  # создали объект, но не сохранили
            customer.user = request.user  # присвоили объекту атрибут user
            customer.save()
            user_form_status.form_submitted = True  # поменяли для юзера статус, что он создал форму
            user_form_status.save()
            return redirect('customer_profile')
        else:
            error = 'Форма содержит ошибки:'
    else:
        if user_form_status.form_submitted:  # если юзер уже создавал форму
            customer = Customer.objects.get(user=request.user)  # получаем его данные
            form = None
        else:
            form = CustomerProfileForm()

    context = {
        'form': form,
        'error': error,
        'customer': customer if user_form_status.form_submitted else None  # проверяем еще раз статус формы
    }
    return render(request, 'main/customer_profile.html', context)


@login_required(login_url="login")
def contractor_profile(request):  # комментарии соответствуют функции выше
    error = ''
    user_form_status, created = ContractorFormStatus.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ContractorProfileForm(request.POST)
        if form.is_valid():
            contractor = form.save(commit=False)
            contractor.user = request.user
            contractor.save()
            user_form_status.form_submitted = True
            user_form_status.save()
            return redirect('contractor_profile')
        else:
            error = 'Форма содержит ошибки:'
    else:
        if user_form_status.form_submitted:
            contractor = Contractor.objects.get(user=request.user)
            form = None
        else:
            form = ContractorProfileForm()

    context = {
        'form': form,
        'error': error,
        'contractor': contractor if user_form_status.form_submitted else None
    }
    return render(request, 'main/contractor_profile.html', context)


@login_required(login_url="login")
def customer_profile_update(request):
    customer, created = Customer.objects.get_or_create(user=request.user)  # получаем данные для текущего юзера
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)  # подсовываем старые данные и меняем их через форму
        if form.is_valid():
            form.save()
            return redirect('customer_profile')
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'main/customer_update.html', {'form': form})


@login_required(login_url="login")
def contractor_profile_update(request):  # комментарии соответсвуют функции выше
    contractor, created = Contractor.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ContractorProfileForm(request.POST, instance=contractor)
        if form.is_valid():
            form.save()
            return redirect('contractor_profile')
    else:
        form = ContractorProfileForm(instance=contractor)
    return render(request, 'main/contractor_update.html', {'form': form})
