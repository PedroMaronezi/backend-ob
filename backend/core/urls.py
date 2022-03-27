from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('api/auth/access', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/create', views.AccountCreationView.as_view(), name='account_creation_view'),
    path('api/user/get', views.ManageAccountView.as_view(), name='account_get_view'),
    path('api/user/put', views.ManageAccountView.as_view(), name='account_update_view'),
    path('api/user/changepassword', views.ChangePasswordView.as_view(), name='change_password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/exemple', views.ExempleView.as_view(), name='exemple_view'),
    path('api/user/data/transactions', views.TransactionsView.as_view(), name='transactions_view'),
    path('api/user/data/balance', views.BalanceView.as_view(), name='balance_view'),
    path('api/user/data/consent', views.ConsentView.as_view(), name='consent_view'),
    path('api/resources/category', views.CategoriesView.as_view(), name='categories_view')
]

