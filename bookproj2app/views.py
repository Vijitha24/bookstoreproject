from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from .forms  import Authorform,Bookform
from  .models import Book,Author

# Create your views here.


def Createbook(request):
    books=Book.objects.all()
    if request.method=='POST':
        form=Bookform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:

        form=Bookform()

    return render(request,'admin/book.html',{'form':form,'books':books})


def Createauthor(request):
    if request.method=='POST':
        form=Authorform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=Authorform()

    return render(request, 'admin/author.html', {'form': form})


class Emptypage:
    pass


def listbook(request):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=Paginator.page(page_number.num_pages)


    return render(request,'admin/booklist.html',{'books':books,'page':page})
def detailsview(request, book_id):
    book=Book.objects.get(id=book_id)

    return render(request, 'admin/detailview.html', {'book': book})

def updatebook(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method == "POST":
        form=Bookform(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=Bookform(instance=book)
    return render(request, "admin/update.html", {'form': form})
def deleteview(request,book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('/')


    return render(request, 'admin/delete.html',{'book': book,})


def index(request):
    return render(request,'admin/base.html')


def search_book(request):
    query=None
    books=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains= query) | Q(author__name__icontains=query) )
    else:
        books=[]
    context={'books':books,'query':query}
    return render(request, 'admin/search.html',context)

