

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Material



class MaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Material
    form_class = BlogForm
    permission_required = 'blog.add_material'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.author = self.request.user
            self.object.save()
        return super().form_valid(form)

class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Material
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_material'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('blog:view', args=[self.kwargs.get('pk')])

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True, )
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)
        return queryset


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object



class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('blog:list')


def toggle_activity(request, pk):
    blog_item = get_object_or_404(Material, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()

    return redirect(reverse('blog:list'))

