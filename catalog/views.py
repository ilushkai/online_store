from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Version
from catalog.services import get_assortment_cache


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/home.html'
    extra_context = {
        # 'object_list': get_category_cache(),
        'title': 'Каталог',
    }


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()
        return context_data



class AssortmentListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {
        'title': 'Все товары',
        'assortment_list': get_assortment_cache(),
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        active_versions = Version.objects.filter(is_active=True)
        for i in queryset:
            i.active_version = active_versions.filter(product=i).last()
        return queryset


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        active_versions = Version.objects.filter(is_active=True)
        for i in queryset:
            i.active_version = active_versions.filter(product=i).last()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = category_item

        return context_data


##############
class VersionPurposeMixin:
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, VersionPurposeMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'

    def get_success_url(self):
        return reverse('catalog:products', args=[self.object.category.pk])


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, VersionPurposeMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'

    def get_success_url(self):
        return reverse('catalog:products', args=[self.object.category.pk])


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = 'catalog.view_product'


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:products', args=[self.object.category.pk])

    def test_func(self):
        return self.request.user.is_superuser


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/contact.html'
    extra_context = {
        'title': 'Контакты'
    }

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}({email}): {message}')
        return super().get_context_data(**kwargs)
