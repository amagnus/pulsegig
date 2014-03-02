from datetime import datetime
from django.contrib import messages
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Guy, Alert, Band, AlertLog
from .forms import SignUpForm, AddBandForm, LoginForm
from app import songkick
from app import toolbox
from app import sendtwilio
from app import crawlImgs


def home(request):
    if request.user.is_authenticated():
        return redirect('app.views.myalerts')
    else:
        return render(request, 'blog.html')


def auth(request):
    if request.user.is_authenticated():
        return redirect('app.views.myalerts')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('app.views.myalerts')
                else:
                    return render(request, 'login.html')

    return render(request, 'login.html', {
        'form': LoginForm(),
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            if User.objects.filter(email=request.POST['email']).exists():
                return redirect('app.views.signup')

            else:
                clientip = toolbox.get_client_ip(request)
                location = songkick.find_metroareaID(clientip)

                kmetroID = ''
                vmetroname = ''
                for k,v in location.items():
                    kmetroID = k
                    vmetroname = v
                    break

                new_user = User.objects.create_user(
                    username=request.POST['email'],
                    email=request.POST['email'],
                    password=request.POST['password'])
                new_guy = Guy(
                    user=new_user,
                    cell=request.POST['cell'],
                    metroareaID=kmetroID,
                    metroarea_name=vmetroname)
                new_guy.save()

                clientip = toolbox.get_client_ip(request)
                areas = songkick.find_metroareaID(clientip)

                sendtwilio.send_text(request.POST['cell'], 'Hey, welcome to Pulse Gig!')

                user = authenticate(username=request.POST['email'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('app.views.myalerts')
                    else:
                        return redirect('app.views.auth')

    if request.user.is_authenticated():
        return redirect('app.views.myalerts')
    else:
        return render(request, 'signup.html', {
            'form': SignUpForm(),
        })


def logout_view(request):
    logout(request)
    return redirect('app.views.auth')


@login_required
def myalerts(request):
    clientip = toolbox.get_client_ip(request)
    new_locations = songkick.find_metroareaID(clientip)

    return render(request, 'myalerts.html', {
         'alerts_subscribed': Alert.objects.filter(user=request.user, disabled=0),
         'alerts_quantity': Alert.objects.filter(user=request.user).count(),
         'location': Guy.objects.filter(user=request.user).values('metroarea_name'),
         'form': AddBandForm(),
         'new_locations': new_locations,
         'plans': AlertLog.objects.filter(user=request.user, has_sent=1, showDate__gte=datetime.now()).order_by('showDate'),
    })


def add_alert(request):
    if request.method == 'POST':
        new_band, created = Band.objects.get_or_create(skID=request.POST['skID'],
            defaults={'name': request.POST['band_name']})

        # if alert does not exist
        if len(Alert.objects.filter(user=request.user, band=new_band)) == 0:
            curr_alert = Alert(user=request.user, band=new_band)
            curr_alert.save()
            return redirect('app.views.myalerts')

        # if alert exists with disabled=1
        if Alert.objects.filter(user=request.user, band=new_band, disabled=1):
            curr_alert = Alert.objects.get(user=request.user, band=new_band, disabled=1)
            curr_alert.disabled = 0
            curr_alert.save()
            return redirect('app.views.myalerts')

        # if alert exists with disabled=0
        if Alert.objects.filter(user=request.user, band=new_band, disabled=0):
            return redirect('app.views.myalerts')

    else:
        return redirect('app.views.myalerts')


@login_required
def delete_alert(request):
    if request.method == 'POST':
        curr_alert = Alert.objects.get(user=request.user, id=request.POST['alertID'])
        curr_alert.disabled = 1
        curr_alert.save()
        return redirect('app.views.myalerts')

    else:
        return redirect('app.views.myalerts')


@login_required
def new_location(request):
    if request.method == 'POST':
        current_user = Guy.objects.get(user=request.user)
        current_user.metroarea_name = request.POST['metroarea_name']
        current_user.metroareaID = request.POST['metroareaID']
        current_user.save()
        return redirect('app.views.myalerts')

    else:
        return redirect('app.views.myalerts')


@login_required
def new_alert(request):
    if request.method == 'POST':
        form = AddBandForm(request.POST)

        if form.is_valid():
            result = songkick.artist_search(request.POST['band'])

            if result == 0:
                return redirect('app.views.myalerts')

            return render(request, 'new_alert.html', {
                'stuff': result,
            })
            
        else:
            return redirect('app.views.myalerts')


def get_band_detail(request):
    if request.is_ajax():
        band_input = request.GET['q']
        band_name = Band.objects.get(id=request.GET['q'])
        band_name_query = str(band_name)

        return render(request, 'band_detail.html', {
            'band_detail': Band.objects.filter(id=band_input),
            'img_url': crawlImgs.searchImage(band_name_query.strip()),
        })

