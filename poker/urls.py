from django.urls import path
from . import views

urlpatterns = [
    path('slots/<int:machine_id>/',views.play_slots, name='slots_page' ),
    path("", views.home, name="home"),
    path ('durak/' , views.durak,
          name='durak/' )

]