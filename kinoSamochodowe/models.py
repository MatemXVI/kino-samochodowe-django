# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class Film(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField("tytuł",max_length=255)
    director = models.CharField("reżyseria",max_length=255, blank=True, null=True)
    cast = models.CharField("obsada",max_length=255, blank=True, null=True)
    screenplay = models.CharField("scenariusz",max_length=255, blank=True, null=True)
    genre = models.CharField("gatunek",max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField("czas trwania",blank=True, null=True)
    country = models.CharField("kraj",max_length=255, blank=True, null=True)
    production_year = models.IntegerField("rok produkcji",blank=True, null=True)
    description = models.TextField("opis",blank=True, null=True)
    poster_filename = models.ImageField("nazwa plakatu",upload_to="films/poster", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="dodał")
    created_at = models.DateTimeField("data dodania",auto_now_add=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='films_editor_set', blank=True, null=True, verbose_name="edytował:")
    updated_at = models.DateTimeField(verbose_name="data ostatniej edycji",auto_now=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"


    def __str__(self):
        return self.title


class FilmImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_filename = models.ImageField("nazwa pliku",upload_to="films/images/", blank=True, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image_filename)


class Venue(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.CharField("miejscowość",max_length=255)
    street = models.CharField("ulica",max_length=255)
    place_type = models.CharField("rodzaj miejsca",max_length=255)
    parking_spot_count = models.IntegerField("ilość miejsc parkingowych")
    additional_info = models.TextField("dodatkowe informacje",blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_venues')
    created_at = models.DateTimeField("data dodania",auto_now_add=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='editor_venues', blank=True, null=True)
    updated_at = models.DateTimeField("data ostatniej edycji",auto_now=True)

    def __str__(self):
        return f"{self.city}, {self.street}"

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"


class VenueImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_filename = models.ImageField("nazwa pliku",upload_to="venues/images/", blank=True, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image_filename)


class Screening(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField("nazwa",max_length=255)
    date = models.DateField("data")
    hour = models.TimeField("godzina")
    price = models.DecimalField("cena",max_digits=10, decimal_places=2)
    film = models.ForeignKey(Film, on_delete=models.SET_NULL, blank=True, null=True, related_name="screenings")
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, blank=True, null=True, related_name="screenings")
    poster_filename = models.ImageField("nazwa plakatu",upload_to="screenings/poster", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="user_screenings")
    created_at = models.DateTimeField("data dodania",auto_now_add=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="editor_screenings")
    updated_at = models.DateTimeField("data ostatniej edycji",auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Seans"
        verbose_name_plural = "Seanse"


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField("data rezerwacji",auto_now_add=True, null=True)
    parking_spot_number = models.IntegerField("numer miejsca parkingowego",blank=True, null=True)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="tickets")

    def data_qr(self) -> str:
        return " ".join([
            str(self.id),
            str(self.screening_id),
            str(self.parking_spot_number),
            str(self.user_id)
        ])

    def __str__(self):
        return str(self.id)

