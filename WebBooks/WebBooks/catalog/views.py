from django.shortcuts import render
from django.http import  HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import *
from .forms import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

# Create your views here.

def index(request):
   # return HttpResponse("Главная страница сайта Мир книг!")
   #Генерация количеств
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
   #Доступные книги
    num_instance_avaiable = BookInstance.objects.filter(status__exact=2).count()
    #Авторы
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

   #Отрисовка шаблона
    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instance': num_instance,
                           'num_instance_avaiable': num_instance_avaiable,
                           'num_authors': num_authors,
                           'num_visits': num_visits,})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by=1

# class AuthorDetailView(generic.DetailView):
 #    model = Author`

class LoanedBooksByUserListView (LoginRequiredMixin,generic.ListView):
    ''' Универсальный класс представления списка книг, находящихся в заказе у текущнго пользователя'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)
        filter(status__exact='2').order_by('due_back')

#получение данных БД и загрузка шаблона
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html",
                  {"form": authorsform, "author": author})

def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")

def delete(request,id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExit:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")

def edit1(request,id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request,"edit1.html",{"author":author})

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')