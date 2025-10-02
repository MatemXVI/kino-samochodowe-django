from datetime import date, timedelta
from kinoSamochodowe.models import Venue, Film, Screening
from django.shortcuts import render, get_object_or_404

def index(request):
    today = date.today()
    days = [today + timedelta(days=i) for i in range(7)]

    film_id = request.GET.get("film")
    venue_id = request.GET.get("venue")
    selected_date = request.GET.get("date")

    if film_id:
        films = Film.objects.exclude(id = film_id).order_by("title")
        selected_film = Film.objects.get(id = film_id)
    else:
        films = Film.objects.order_by("title")
        selected_film = None

    if venue_id:
        venues = Venue.objects.exclude(id=venue_id).order_by("city")
        selected_venue = Venue.objects.get(id=venue_id)
    else:
        venues = Venue.objects.order_by("city")
        selected_venue = None

    if not venue_id or selected_venue is None:
        if not film_id or selected_film is None: #wszystkie miejsca i wszystkie filmy
            if selected_date:
                screenings = Screening.objects.filter(date = selected_date).order_by("date")
            else:
                screenings = Screening.objects.order_by("date")
        else: #wszystkie miejsca i jeden film
            if selected_date:
                screenings = Screening.objects.filter(date = selected_date, film_id=film_id).order_by("date")
            else:
                screenings = Screening.objects.filter(film_id = film_id).order_by("date")
    else:
        if not film_id or selected_film is None: #jedno miejsce i wszystkie filmy
            if selected_date:
                screenings = Screening.objects.filter(date = selected_date, venue_id = venue_id).order_by("date")
            else:
                screenings = Screening.objects.filter(venue_id = venue_id).order_by("date")
        else: #jedno miejsce i jeden film
            if selected_date:
                screenings = Screening.objects.filter(date = selected_date, venue_id = venue_id, film_id=film_id).order_by("date")
            else:
                screenings = Screening.objects.filter(venue_id = venue_id, film_id=film_id).order_by("date")

    return render(request, "main/screening/index.html", {"film_id": film_id, "venue_id": venue_id, "selected_venue": selected_venue, "selected_film": selected_film, "films": films, "screenings": screenings, "venues": venues, "days": days})


def show(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    return render(request, "main/screening/show.html", {"screening": screening})