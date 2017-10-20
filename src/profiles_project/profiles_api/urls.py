from django.conf.urls import urls
from django.conf.urls import include

from rest_framework.routers import DefaultRouters

from . import views

router = DefaultRouters()
router.register("hello-viewset", views.HelloViewset, base_name='hello-viewset')
router.register("profile", views.UserProfileViewSet)
router.register("login", views.LoginViewSet, base_name='login')
router.register("feed", views.UserProfileFeedViewSet)

urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'', include(router.urls))
]
