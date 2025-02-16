from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from frontend.models.customer import Customer
from django.utils.translation import gettext_lazy as _

@method_decorator(login_required, name='dispatch')
class AdminCustomerListView(ListView):
    model = Customer
    template_name = 'admin/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.none()

@method_decorator(login_required, name='dispatch')
class AdminCustomerDetailView(DetailView):
    model = Customer
    template_name = 'admin/customer_detail.html'
    context_object_name = 'customer'

    def get_object(self):
        if self.request.user.is_superuser:
            return super().get_object()
        return None

@method_decorator(login_required, name='dispatch')
class AdminCustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'admin/customer_confirm_delete.html'
    success_url = reverse_lazy('admin:customer_list')

    def get_object(self):
        if self.request.user.is_superuser:
            return super().get_object()
        return None
