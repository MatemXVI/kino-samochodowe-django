from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import film_views, screening_views, ticket_views, venue_views, buy_ticket_views, user_views

urlpatterns = ([
    #main
    path("", film_views.index, name="index"),
    path("films/<int:pk>", film_views.show, name="films_show"),
    path("screenings", screening_views.index, name="screenings_index"),
    path("screenings/<int:pk>", screening_views.show, name="screenings_show"),
    path("venues/<int:pk>", venue_views.show, name="venues_show"),
    path("venues", venue_views.index, name="venues_index"),

    #ticket
    path("tickets/<int:pk>", ticket_views.show, name="tickets_show"),

    #buy ticket
    path("tickets/parking", buy_ticket_views.parking, name="tickets_parking"),
    path("tickets/selected", buy_ticket_views.selected, name="tickets_selected"),
    path("tickets/payment", buy_ticket_views.payment, name="tickets_payment"),
    path("tickets/summary", buy_ticket_views.summary, name="tickets_summary"),
    path("tickets/generated", buy_ticket_views.generate, name="tickets_generate"),

    path("login", user_views.login_user, name="login"),
    path("register", user_views.register_user, name="register"),
    path("logout", user_views.logout_user, name="logout"),

    # user
    path("user/dashboard", user_views.dashboard, name="user_dashboard"),
    path("user/edit", user_views.edit_user, name="user_edit"),
    path("user/tickets", ticket_views.index, name="tickets_index"),
    path("user/destroy/<int:pk>", ticket_views.destroy, name="tickets_destroy"),
])


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)