from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from kinoSamochodowe.models import *

def index(request):
    tickets = Ticket.objects.filter(user = request.user)
    return render(request, "user/tickets.html", {"tickets": tickets})

def show(request, pk):
    ticket = Ticket.objects.select_related("screening__film", "screening__venue",  "user").get(id=pk)
    if ticket.user_id is not None and (ticket.user_id == request.user.id or request.user.is_staff):
        data_qr = ticket.data_qr()
        return render(request, "ticket/show.html", {"ticket": ticket, "data_qr": data_qr})
    else:
        return redirect("index")



def destroy(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if ticket.user_id == request.user.id:
        ticket.user_id = None
        ticket.created_at = None
        ticket.save()
        message ="Bilet został usunięty.\nŚrodki zostaną zwrócone na konto w przeciągu 7 dni,\nna dane które podałeś przy zakupie biletu."
        messages.success(request, message)
        return redirect("tickets_index")
    else:
        return redirect("index")

