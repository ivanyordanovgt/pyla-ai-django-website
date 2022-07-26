from django.shortcuts import render
import django.views.generic as views

# Create your views here.
from django.urls import reverse_lazy



# class TodosListView(views.ListView):
#     model = Todo
#     template_name = 'testing/listview.html'
#     ordering = ('category__title',)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # add custom context
#         context['test'] = 'test'
#
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         title_filter = self.request.GET.get('filter', None)
#         if title_filter:
#             queryset = queryset.filter(title__contains=title_filter)
#
#         return queryset
#
#
# class TodoDetailsView(views.DetailView):
#     template_name = 'testing/detailview.html'
#     model = Todo
#
#
# class TodoCreateView(views.CreateView):
#     template_name = 'testing/create-todo.html'
#     model = Todo
#     success_url = reverse_lazy('list view')
#     fields = ('title', 'description', 'category')
#
#
# class TodoEditView(views.UpdateView):
#     template_name = 'testing/edit-todo.html'
#     model = Todo
#     success_url = reverse_lazy('list view')
#     fields = '__all__'
#
#
# class TodoDeleteView(views.DeleteView):
#     model = Todo
