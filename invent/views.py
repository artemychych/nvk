from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404

from .forms import *
from .models import *


def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена")


menu = [{'title': "Invent", 'url_name': 'home'},
        {'title': "Ремонт", 'url_name': 'repair'},
        {'title': "Отделы", 'url_name': 'dep'},
        {'title': "Кабинеты", 'url_name': 'loc'},
        {'title': "Обратная связь", 'url_name': 'contact'}
        ]


# HOME PAGE
# ------------------------------------------------------------------------------


def invent_home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = InvForm(request.POST)
            if form.is_valid():
                invent = form.save(commit=False)
                invent.save()
                return redirect('home')
        else:
            form = InvForm()

        search_query = request.GET.get('q')
        selected_query = request.GET.get('s')

        if search_query:
            if selected_query == "0":
                inv = Inventory.objects.filter(Q(name__icontains=search_query))
            elif selected_query == "1":
                inv = Inventory.objects.filter(Q(tech_id__icontains=search_query))
            elif selected_query == "2":
                inv = Inventory.objects.filter(Q(invent_id__icontains=search_query))
            else:
                inv = Inventory.objects.filter(Q(room__room__icontains=search_query))
        else:
            inv = Inventory.objects.all()

        filter_select_floor = request.GET.get('filter-select-floor')
        filter_select_room = request.GET.get('filter-select-room')
        filter_checkbox = request.GET.getlist('filter-checkbox')

        if filter_select_room:
            if filter_select_room != "0":
                inv = inv.filter(room__room=filter_select_room)
            else:
                if filter_select_floor:
                    if filter_select_floor != "0":
                        if filter_select_floor == "1":
                            inv = inv.filter(room__room__regex=r'^1[0-9]*$')
                        elif filter_select_floor == "2":
                            inv = inv.filter(room__room__regex=r'^2[0-9]*$')
                        elif filter_select_floor == "3":
                            inv = inv.filter(room__room__regex=r'^3[0-9]*$')
                        elif filter_select_floor == "4":
                            inv = inv.filter(room__room__regex=r'^4[0-9]*$')
                        else:
                            inv = inv.filter(room__room__regex=r'^5[0-9]*$')
        if filter_checkbox:
            inv_clear = None
            for i in filter_checkbox:
                if inv_clear is None:
                    inv_clear = inv.filter(department__name=i)
                else:
                    inv_clear = inv.filter(department__name=i) | inv_clear
            inv = inv_clear

        rooms = Location.objects.all()
        deps = Department.objects.all()
    else:
        return redirect('auth')

    return render(request, 'invent/home.html', {
        'rooms': rooms,
        'deps': deps,
        'inv': inv,
        'title': "Оборудование",
        'menu': menu,
        'selected': 0,
        'form': form
    })


# class InventHome(ListView):
#     model = Inventory
#     template_name = 'invent/home.html'
#     context_object_name = 'inv'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['title'] = 'Оборудование'
#         context['selected'] = 0
#         context['form'] = SearchForm
#         return context
#
#     def get_queryset(self):
#         if request.GET.get('q'):
#             print()
#         return Inventory.objects.all()
#
#
# def inv_search(request):
#     form = SearchForm
#     asd = request.GET.get('q')
#     print(asd)
#
#     return render(request, 'invent/home.html', {
#         'title': 'Оборудование',
#         'form': form,
#     })

def choose_room(request):
    get_room = request.GET.get("select-room")
    if get_room:
        context = Inventory.objects.filter(room__room=get_room)
    else:
        raise Http404


def floor(request):
    get_floor = request.GET.get("filter-select-floor")

    if get_floor:
        if get_floor == "1":
            context = Location.objects.filter(room__regex=r'^1[0-9]*$')
        elif get_floor == "2":
            context = Location.objects.filter(room__regex=r'^2[0-9]*$')
        elif get_floor == "3":
            context = Location.objects.filter(room__regex=r'^3[0-9]*$')
        elif get_floor == "4":
            context = Location.objects.filter(room__regex=r'^4[0-9]*$')
        else:
            context = Location.objects.filter(room__regex=r'^5[0-9]*$')
    else:
        raise Http404

    l = []
    for i in context:
        l.append(i.room)

    return JsonResponse({"rooms": l})


def delete_inv(request):
    get_id = request.GET['id']

    if get_id:
        Inventory.objects.get(id=get_id).delete()
    else:
        raise Http404
    return JsonResponse({'Status': 'OK'})


def update_inv(request):
    if request.POST:
        inv_update = Inventory.objects.get(id=request.POST['id'])
        inv_update.name = request.POST['name']
        inv_update.invent_id = request.POST['invent_id']
        inv_update.tech_id = request.POST['tech_id']
        if request.POST['room'] != '0':
            inv_update.room = Location.objects.get(room=request.POST['room'])
        inv_update.description = request.POST['description']
        if request.POST['department'] != '0':
            inv_update.department = Department.objects.get(name=request.POST['department'])
        inv_update.comment = request.POST['comment']
        inv_update.save()
    else:
        raise Http404

    return JsonResponse({'response': 'OK'})


# AUTH PAGE
# ------------------------------------------------------------------------------

def auth(request):
    if not request.user.is_authenticated:
        is_active = 'true'
        wrong_info = 'false'
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    is_active = 'false'
            else:
                wrong_info = 'true'
    else:
        return redirect('home')
    return render(
        request, 'invent/auth.html', {'is_active': is_active, 'wrong_info': wrong_info}
    )


def log_out(request):
    logout(request)
    return redirect('auth')


# REPAIR PAGE
# ------------------------------------------------------------------------------


def repair(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            form = RepairForm(request.POST)
            if form.is_valid():
                invent = form.save(commit=False)
                invent.save()
                return redirect('repair')
        else:
            form = RepairForm()

        search_query = request.GET.get('q')
        selected_query = request.GET.get('s')

        if search_query:
            rep = Repair.objects.filter(Q(inv_id__invent_id__icontains=search_query))
        else:
            rep = Repair.objects.all()




    else:
        return redirect('auth')

    return render(request, 'invent/repair.html', {'rep': rep,
                                                  'form': form,
                                                  'title': "Ремонт",
                                                  'menu': menu,
                                                  })


def delete_repair(request):
    get_id = request.GET['id']

    if get_id:
        Repair.objects.get(id=get_id).delete()
    else:
        raise Http404
    return JsonResponse({'Status': 'OK'})


def update_repair(request):
    if request.POST:
        rep_update = Repair.objects.get(id=request.POST['id'])
        rep_update.comment = request.POST['comment']
        if request.POST['completed'] == '1':
            rep_update.completed = True
        else:
            rep_update.completed = False
        rep_update.save()
    else:
        raise Http404

    return JsonResponse({'response': 'OK'})


# DEPARTMENT PAGE
# ------------------------------------------------------------------------------

def department(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            form = DepForm(request.POST)
            if form.is_valid():
                invent = form.save(commit=False)
                invent.save()
                return redirect('department')
        else:
            form = DepForm()

        search_query = request.GET.get('q')

        if search_query:
            dep = Department.objects.filter(Q(name__icontains=search_query))
        else:
            dep = Department.objects.all()

    else:
        return redirect('auth')

    return render(request, 'invent/department.html', {'dep': dep,
                                                      'form': form,
                                                      'title': "Отделы",
                                                      'menu': menu})


def update_dep(request):
    if request.POST:
        dep_update = Department.objects.get(id=request.POST['id'])
        dep_update.name = request.POST['name']
        dep_update.save()
    else:
        raise Http404

    return JsonResponse({'response': 'OK'})


def delete_dep(request):
    get_id = request.GET['id']

    if get_id:
        Department.objects.get(id=get_id).delete()
    else:
        raise Http404
    return JsonResponse({'Status': 'OK'})


# LOCATION PAGE
# ------------------------------------------------------------------------------

def location(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = LocationForm(request.POST)
            if form.is_valid():
                invent = form.save(commit=False)
                invent.save()
                return redirect('location')
        else:
            form = LocationForm()

        search_query = request.GET.get('q')
        selected_query = request.GET.get('s')

        if search_query:
            if selected_query == "0":
                loc = Location.objects.filter(Q(room__icontains=search_query))
            elif selected_query == "1":
                loc = Location.objects.filter(Q(department__name__icontains=search_query))
        else:
            loc = Location.objects.all()

        deps = Department.objects.all()

    else:
        return redirect('auth')

    return render(request, 'invent/room.html', {'room': loc,
                                                'form': form,
                                                'title': "Кабинеты",
                                                'deps': deps,
                                                'menu': menu})


def delete_loc(request):
    get_id = request.GET['id']

    if get_id:
        Location.objects.get(id=get_id).delete()
    else:
        raise Http404
    return JsonResponse({'Status': 'OK'})


def update_loc(request):
    print(request.POST)
    if request.POST:
        loc_update = Location.objects.get(id=request.POST['id'])
        loc_update.room = request.POST['room']
        loc_update.comment = request.POST['comment']
        if request.POST['dep'] != '0':
            loc_update.department = Department.objects.get(name=request.POST['dep'])
        loc_update.save()
    else:
        raise Http404

    return JsonResponse({'response': 'OK'})
