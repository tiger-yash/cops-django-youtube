from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
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

def renew_book_librarian(request, pk):
    """View function for renewing a specific BookCopy by librarian."""
    book_instance = get_object_or_404(BookCopy, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

