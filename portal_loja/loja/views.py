from django.http import HttpResponse
from django.template import loader
from .models import Produto

def produtos(request):
    produtos = Produto.objects.select_related('categoria').all()
    template = loader.get_template('produtos.html')  # novo template
    context = {
        'produtos': produtos,
    }
    return HttpResponse(template.render(context, request))