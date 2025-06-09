from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Cliente, Categoria, Produto, Pedido, Pagamento
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Autenticação
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('produtos')  # redireciona para a lista de produtos, por exemplo
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        email = request.POST['email']
        User.objects.create_user(username=username, password=senha, email=email)
        return redirect('login')
    return render(request, 'cadastro.html')


# Clientes
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def cliente_detalhe(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    return render(request, 'cliente_detalhe.html', {'cliente': cliente})

# Categorias
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})

def categoria_detalhe(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    return render(request, 'categoria_detalhe.html', {'categoria': categoria})

# Produtos
def produtos(request):
    produtos = Produto.objects.select_related('categoria').all()
    return render(request, 'produtos.html', {'produtos': produtos})

def produto_detalhe(request, id_produto):
    produto = get_object_or_404(Produto, id_produto=id_produto)
    return render(request, 'produto_detalhe.html', {'produto': produto})


# Pedidos
def pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').all()
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def pedido_detalhe(request, id_pedido):
    pedido = get_object_or_404(Pedido, id=id_pedido)
    return render(request, 'pedido_detalhe.html', {'pedido': pedido})


# Pagamentos
def pagamentos(request):
    pagamentos = Pagamento.objects.select_related('pedido').all()
    return render(request, 'pagamentos.html', {'pagamentos': pagamentos})

def pagamento_detalhe(request, id_pagamento):
    pagamento = get_object_or_404(Pagamento, id=id_pagamento)
    return render(request, 'pagamento_detalhe.html', {'pagamento': pagamento})
