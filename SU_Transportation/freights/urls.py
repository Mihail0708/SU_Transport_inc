from django.contrib.auth.decorators import login_required
from django.urls import path, include

from SU_Transportation.freights import views
from SU_Transportation.freights.views import CreateLoadView, DetailsLoadsView, DeleteLoadView, InfoLoadView, CompleteLoadView

urlpatterns = [
    path('', login_required(DetailsLoadsView.as_view()), name='details load'),
    path('create-load/', login_required(CreateLoadView.as_view()), name='create load'),
    path('<int:pk>/', include([
        path('delete-load/', login_required(DeleteLoadView.as_view()), name='delete load'),
        path('info-load/', login_required(InfoLoadView.as_view()), name='info load'),
        path('get-load/', views.get_load_view, name='get load'),
        path('return-load/', views.return_load_view, name='return load'),
        path('complete-load/', login_required(CompleteLoadView.as_view()), name='complete load')
    ])),
]
