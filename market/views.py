# market/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import MarketDataForm, MarketDataSearchForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import MarketData, HistoricalMarketData, Alert, Category, CustomUser
from django.utils import timezone
from taggit.models import Tag
from django.contrib import messages
from django.contrib.auth import logout
from .forms import CustomUserCreationForm

from .dash_apps import dash_plot
from django.core.paginator import Paginator
from io import BytesIO
from xhtml2pdf import pisa


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'market/login.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_regular_user(user):
    return user.groups.filter(name='Regular User').exists()

def home(request):
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    return render(request, 'market/index.html', {'is_admin': is_admin})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created! You are now logged in.')
            return redirect('market_data_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'market/register.html', {'form': form})


@login_required
def market_data_list(request):
    form = MarketDataSearchForm(request.GET or None)
    
    # Check if the user is an admin
    is_admin = request.user.groups.filter(name='Admin').exists()

    market_data = MarketData.objects.all()  # All users can see all market data
    
    if form.is_valid():
        product_name = form.cleaned_data.get('product_name')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        category = form.cleaned_data.get('category')

        if product_name:
            market_data = market_data.filter(product_name__icontains=product_name)
        if min_price is not None:
            market_data = market_data.filter(price__gte=min_price)
        if max_price is not None:
            market_data = market_data.filter(price__lte=max_price)
        if category:
            market_data = market_data.filter(category=category)

    paginator = Paginator(market_data, 6)  # Show 10 market data items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'market/market_data_list.html', {
        'market_data': page_obj,
        'form': form,
        'is_admin': is_admin,
    })

def market_data_create(request):
    if request.method == 'POST':
        form = MarketDataForm(request.POST, request.FILES)
        if form.is_valid():
            market_data = form.save(commit=False)
            market_data.created_by = request.user
            market_data.save()
            form.save_m2m()  # Save tags
            return redirect('market_data_list')
    else:
        form = MarketDataForm()
    return render(request, 'market/market_data_form.html', {'form': form})


@login_required
def market_data_edit(request, pk):
    # Check if the user is an admin
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'You do not have permission to edit this data.')
        return redirect('market_data_list')

    market_data = MarketData.objects.get(pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = MarketDataForm(request.POST, request.FILES, instance=market_data)
        if form.is_valid():
            form.save()
            return redirect('market_data_list')
    else:
        form = MarketDataForm(instance=market_data)
    return render(request, 'market/market_data_form.html', {'form': form})


@login_required
def market_data_delete(request, pk):
    # Check if the user is an admin
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'You do not have permission to delete this data.')
        return redirect('market_data_list')

    market_data = MarketData.objects.get(pk=pk, created_by=request.user)
    market_data.delete()
    return redirect('market_data_list')

def generate_report(request):
    market_data = MarketData.objects.filter(created_by=request.user)
    html_string = render_to_string('market/report.html', {'market_data': market_data, 'request': request})
    
    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="market_data_report.pdf"'
    
    # Create a BytesIO buffer to receive the PDF content
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    pisa_status = pisa.CreatePDF(html_string, dest=buffer)
    
    # If there was an error, show what happened
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

