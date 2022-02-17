from django.urls import path
from rest_framework.routers import DefaultRouter

from villagers import views
from villagers.views import CreateVillagerView

villager_router = DefaultRouter(trailing_slash=False)
villager_router.register("imports", views.CreateVillagerView)

villager_router._urls = [
    r
    for r in villager_router.urls
    if not any([r.name.endswith(bad) for bad in ["detail"]])
]

urlpatterns = [
    path("imports", CreateVillagerView.as_view({"post": "create"})),
]

urlpatterns += villager_router.urls
