from django.views.generic import ListView

from SU_Transportation.common.models import ContactUsModel
from SU_Transportation.our_services.models import ServicesModel


class ServicesView(ListView):
    model = ServicesModel
    template_name = 'services_details_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = ContactUsModel.objects.filter(is_red=False)

        context.update({
            'messages': messages
        })

        return context

