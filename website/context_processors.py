from .forms import SearchForm
from .models import Subject

def search_form(request):
    return{
        'search_form': SearchForm()
    }

def subjects(request):
	return{
	'subjects': Subject.objects.all()
}
