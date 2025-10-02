from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from kinoSamochodowe.models import Screening, Ticket


def parking(request):
    screening_id = request.GET.get("screening_id")
    screening = Screening.objects.get(id = screening_id)
    available_parking_spot_count = Ticket.objects.filter(user_id = None, screening_id = screening_id).count()
    parking_spot_count = Ticket.objects.filter(screening_id = screening_id).count()
    parking_spots = Ticket.objects.filter(screening_id=screening_id)
    rows = []
    total = len(parking_spots)
    for i, item in enumerate(parking_spots, start=1):
        page = (i + 9) // 10
        missing_cells = range((10 - (i % 10)) % 10)
        rows.append({
            "item": item,
            "counter": i,
            "page": page,
            "is_last": i == total,
            "missing_cells": missing_cells
        })
    return render(request, "buy_ticket\parking.html",
                  {"screening": screening, "available_parking_spot_count": available_parking_spot_count, "parking_spot_count": parking_spot_count, "parking_spots": parking_spots, "rows": rows })

def selected(request):
    if not request.user.is_authenticated:
        messages.error(request, "Musisz się zalogować, aby uzyskać dostęp.")
        return redirect("login")
    parking_spot_number =  request.GET.get("parking_spot_number")
    screening_id = request.GET.get("screening_id")
    if parking_spot_number and screening_id:
        ticket = get_object_or_404(Ticket.objects.filter(parking_spot_number = parking_spot_number, screening_id = screening_id, user_id = None))
        return render(request, "buy_ticket\selected.html", {"ticket": ticket,"parking_spot_number": parking_spot_number, "screening_id": screening_id})
    else:
        return redirect("tickets_parking")

def payment(request):
    if not request.user.is_authenticated:
        messages.error(request, "Musisz się zalogować, aby uzyskać dostęp.")
        return redirect("login")
    parking_spot_number =  request.POST.get("parking_spot_number")
    screening_id = request.POST.get("screening_id")
    return render(request, "buy_ticket\payment.html",{"parking_spot_number": parking_spot_number, "screening_id": screening_id})

def summary(request):
    if not request.user.is_authenticated:
        messages.error(request, "Musisz się zalogować, aby uzyskać dostęp.")
        return redirect("login")
    parking_spot_number =  request.POST.get("parking_spot_number")
    screening_id = request.POST.get("screening_id")
    payment_ = request.POST.get("payment")
    user = request.user
    ticket = get_object_or_404(Ticket.objects.filter(parking_spot_number=parking_spot_number, screening_id=screening_id, user_id=None))
    return render(request, "buy_ticket\summary.html", {"parking_spot_number": parking_spot_number, "payment":payment_, "user":user, "ticket": ticket, "screening_id": screening_id})

def generate(request):
    if not request.user.is_authenticated:
        messages.error(request, "Musisz się zalogować, aby uzyskać dostęp.")
        return redirect("login")
    parking_spot_number =  request.POST.get("parking_spot_number")
    screening_id = request.POST.get("screening_id")
    ticket = get_object_or_404(Ticket.objects.filter(parking_spot_number=parking_spot_number, screening_id=screening_id, user_id=None))
    ticket.user_id = request.user.id
    ticket.created_at = timezone.now()
    ticket.save()
    messages.success(request, "Bilet został zakupiony. Pamiętaj, że tylko z nim możesz wejść na seans.\n Zeskanuj kod QR przy wjeździe na parking.\n Życzymy miłego oglądania!")
    return redirect("tickets_show", ticket.id)

