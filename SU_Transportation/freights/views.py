from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView

from SU_Transportation.common.models import ContactUsModel
from SU_Transportation.freights.forms import LoadCreateForm, CompleteLoadForm
from SU_Transportation.freights.models import LoadCreateModel


class DetailsLoadsView(ListView):
    paginate_by = 5
    model = LoadCreateModel
    template_name = 'loads_details_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = ContactUsModel.objects.filter(is_red=False)

        context.update({
            'messages': messages,
        })

        return context


class CreateLoadView(CreateView):
    model = LoadCreateModel
    form_class = LoadCreateForm
    template_name = 'load_create_page.html'
    success_url = reverse_lazy('details load')


class DeleteLoadView(DeleteView):
    model = LoadCreateModel
    template_name = 'load_delete_page.html'
    success_url = reverse_lazy('details load')


class InfoLoadView(DetailView):
    model = LoadCreateModel
    template_name = 'load_info_page.html'


class CompleteLoadView(UpdateView):
    model = LoadCreateModel
    form_class = CompleteLoadForm
    template_name = 'load_complete_page.html'

    def form_valid(self, form):
        self.object.user = None
        self.object.is_completed = True
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile loads', kwargs={'pk': self.request.user.pk})


@login_required
def get_load_view(request, pk):
    load = LoadCreateModel.objects.filter(pk=pk).get()
    load.user = request.user
    load.save()

    return redirect('details load')


@login_required
def return_load_view(request, pk):
    load = LoadCreateModel.objects.filter(pk=pk).get()
    load.user = None
    load.save()

    return redirect('profile loads', pk=request.user.pk)

