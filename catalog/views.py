from django.shortcuts import render

# Create your views here.

from .models import Book, BookCopy

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookCopy.objects.all().count()

    # Available books (status = 1)
    num_instances_available = BookCopy.objects.filter(status=1).count()

    # The 'all()' is implied by default.

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
