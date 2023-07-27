from django.contrib.auth.decorators import login_required
from django.urls import path, include

from SU_Transportation.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, DetailsUserView, \
    EditUserView, DeleteUserView, UserLoadsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', login_required(DetailsUserView.as_view()), name='profile details'),
        path('edit/', login_required(EditUserView.as_view()), name='profile edit'),
        path('delete/', login_required(DeleteUserView.as_view()), name='profile delete'),
        path('my_loads/', login_required(UserLoadsView.as_view()), name='profile loads'),
    ])),
]