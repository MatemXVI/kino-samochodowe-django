from kinoSamochodowe.models import Venue, VenueImage, Screening
from django.shortcuts import render, get_object_or_404

def index(request):
    venues = Venue.objects.order_by("city")
    pk = None
    return render(request, "main/venue/show.html", {"id": pk, "venues": venues})

def show(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    venues = Venue.objects.exclude(id=pk).order_by("city")
    images = VenueImage.objects.filter(venue = venue)
    screenings = Screening.objects.filter(venue = venue).order_by("date")
    return render(request, "main/venue/show.html", {"id": pk, "venue": venue, "venues": venues, "images": images, "screenings": screenings})