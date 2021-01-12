from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('login',view=LoginView.as_view(template_name="account/login.html", redirect_authenticated_user=True), name="login"),
	path('logout', view=LogoutView.as_view(), name="logout"),
]

