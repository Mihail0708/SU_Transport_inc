from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView

from SU_Transportation.common.forms import DriverApplicationForm, ApplicationAddressForm
from SU_Transportation.common.models import ApplicationAddress, ContactUsModel


class IndexView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = ContactUsModel.objects.filter(is_red=False)

        context.update({
            'messages': messages
        })

        return context


def driver_application_view(request):
    driver_info_form = DriverApplicationForm()
    driver_address_form = ApplicationAddressForm()

    if request.method == 'POST':
        driver_info_form = DriverApplicationForm(request.POST)
        driver_address_form = ApplicationAddressForm(request.POST)

        if driver_info_form.is_valid() and driver_address_form.is_valid():
            driver_address_form.save()
            driver_appl = driver_info_form.save(commit=False)
            driver_appl.address = ApplicationAddress.objects.last()
            driver_appl.save()
            return redirect('home page')

    context = {
        'driver_info_form': driver_info_form,
        'driver_address_form': driver_address_form
    }
    return render(request, 'apply_page.html', context=context)


class ContactUsView(CreateView):
    model = ContactUsModel
    fields = ('Name', 'Email', 'Phone', 'Message')
    template_name = 'contact_us_page.html'
    success_url = reverse_lazy('home page')


class MessageView(ListView):
    paginate_by = 5
    model = ContactUsModel
    template_name = 'message_page.html'


class ReadView(DetailView):
    model = ContactUsModel
    template_name = 'read_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.is_red = True
        self.object.save()

        return context


class DeleteMessageView(DeleteView):
    model = ContactUsModel
    template_name = 'delete_message_page.html'
    success_url = reverse_lazy('messages')