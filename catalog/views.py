from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from .models import *

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookCopy.objects.all().count()

    # Available books (status = 1)
    num_instances_available = BookCopy.objects.filter(status=1).count()

    # The 'all()' is implied by default.

    # Number of visits to this view,as counted in session variable
    num_visits = request.session.get('num_visit',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class LoanedBooksByUserListView (LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books to loan to current user"""
    model = BookCopy
    template_name = "catalog/bookcopy_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        """Return the books on loan to the current user"""
        return BookCopy.objects.filter(borrower=self.request.user).filter(status__exact=1).order_by('borrow_date')
        
