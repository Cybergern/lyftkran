from django.views.generic.list import ListView
from django.views.generic import DetailView

from .models import Lifter
from .models import License

# Create your views here.
class LifterList(ListView):
    model = Lifter
    queryset = Lifter.objects.order_by('family_name')
    context_object_name = 'lifters'
    paginate_by = 20

class LifterDetail(DetailView):
    model = Lifter
    template_name = 'lifter_detail.html'