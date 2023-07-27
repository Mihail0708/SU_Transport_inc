from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from SU_Transportation.accounts.forms import SuUserCreateForm, SuUserEditForm
from SU_Transportation.common.models import ContactUsModel

user_model = get_user_model()


class RegisterUserView(CreateView):
    model = user_model
    form_class = SuUserCreateForm
    template_name = 'register-page.html'
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    template_name = 'login-user.html'
    next_page = reverse_lazy('home page')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home page')


class DetailsUserView(DetailView):
    model = user_model
    template_name = 'details-user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user
        messages = ContactUsModel.objects.filter(is_red=False)

        context.update({
            'employee': employee,
            'messages': messages
        })

        return context


class EditUserView(UpdateView):
    model = user_model
    form_class = SuUserEditForm
    template_name = 'edit-user.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class DeleteUserView(DeleteView):
    model = user_model
    template_name = 'delete-user.html'
    success_url = reverse_lazy('home page')


class UserLoadsView(DetailView):
    model = user_model
    template_name = 'loads-user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_loads = self.object.loadcreatemodel_set.all()
        paginator = Paginator(driver_loads, 5)
        page_number = self.request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)

        context.update({
            'driver_loads': driver_loads,
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj
        })
        return context

