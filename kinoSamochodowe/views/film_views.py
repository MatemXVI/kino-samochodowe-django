from django.shortcuts import render, get_object_or_404
from kinoSamochodowe.models import Venue, Film, Screening, FilmImage
from datetime import date, timedelta

def index(request):
    today = date.today()
    days = [today + timedelta(days=i) for i in range(7)]

    venue_id = request.GET.get("venue")
    selected_date = request.GET.get("date")

    if venue_id:
        venues = Venue.objects.exclude(id=venue_id).order_by("city")
        selected_venue = Venue.objects.get(id=venue_id)
    else:
        venues = Venue.objects.order_by("city")
        selected_venue = None

    if not venue_id or selected_venue is None:
        if selected_date:
            films = Film.objects.filter(screenings__date=selected_date).distinct().order_by("screenings__date")
            for film in films:
                hours = Screening.objects.filter(film_id = film.id, date = selected_date).order_by("hour")
                film.hours = hours
        else:
            films = Film.objects.filter(screenings__isnull=False).distinct()
            for film in films:
                hours = Screening.objects.filter(film_id = film.id).order_by("hour")
                film.hours = hours

    else:
        if selected_date:
            films = Film.objects.filter(screenings__date=selected_date, screenings__venue_id = venue_id).distinct().order_by("screenings__date")
            for film in films:
                hours = Screening.objects.filter(film_id = film.id, venue_id = venue_id, date = selected_date).order_by("hour")
                film.hours = hours
        else:
            films = Film.objects.filter(screenings__venue_id = venue_id)
            for film in films:
                hours = Screening.objects.filter(film_id = film.id, venue_id = venue_id).order_by("hour")
                film.hours = hours

    return render(request, "main/film/index.html", {"venue_id": venue_id, "selected_venue": selected_venue, "films": films, "venues": venues, "days": days})


def show(request, pk):
    film = get_object_or_404(Film, pk=pk)
    screenings = Screening.objects.filter(film = film).order_by("date")
    images = FilmImage.objects.filter(film = film)
    return render(request, "main/film/show.html", {"film": film, "screenings": screenings, "images": images})