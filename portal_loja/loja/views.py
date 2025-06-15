from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import Cliente, Categoria, Produto, Pedido, Pagamento
from decimal import Decimal
from datetime import datetime

# Página principal
def index(request):
    """View para a página principal"""
    produtos_destaque = Produto.objects.filter(estoque__gt=0)[:6]  # Produtos em destaque
    return render(request, 'principal.html', {'produtos_destaque': produtos_destaque})

# Autenticação
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index')  # redireciona para a página principal do site
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['user']
        senha = request.POST['senha']
        email = request.POST['email']
        nome = request.POST['user']
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        cpf = request.POST['cpf']

        # Verificar duplicações
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'erro': 'Nome de usuário já existe'})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro.html', {'erro': 'Email já cadastrado'})

        if Cliente.objects.filter(cpf=cpf).exists():
            return render(request, 'cadastro.html', {'erro': 'CPF já cadastrado'})

        # Criar usuário
        user = User.objects.create_user(username=username, password=senha, email=email)

        # Criar cliente vinculado ao user
        Cliente.objects.create(
            user=user,
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco,
            cpf=cpf
        )

        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
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
    produtos = Produto.objects.select_related('categoria').filter(estoque__gt=0)
    return render(request, 'produtos.html', {'produtos': produtos})

def produto_detalhe(request, id_produto):
    produto = get_object_or_404(Produto, id_produto=id_produto)
    return render(request, 'produto_detalhe.html', {'produto': produto})

# Compras
@login_required
def compra(request, id_produto):
    """View para exibir a página de compra de um produto"""
    produto = get_object_or_404(Produto, id_produto=id_produto)

    # Verificar se há estoque
    if produto.estoque <= 0:
        messages.error(request, 'Produto sem estoque disponível.')
        return redirect('produto_detalhe', id_produto=id_produto)

    return render(request, 'compra.html', {'produto': produto})

from django.db.models import F
from django.utils.timezone import now

@login_required
def finalizar_compra(request, id_produto):
    """View para processar a finalização da compra"""
    print("View finalizar_compra foi chamada.")  # ✅ início da view

    if request.method == 'POST':
        print("Método POST recebido.")  # ✅ confirmação do método POST

        produto = get_object_or_404(Produto, id_produto=id_produto)
        print(f"Produto carregado: {produto.nome}, estoque atual: {produto.estoque}")  # ✅ produto carregado

        quantidade = int(request.POST.get('quantidade', 1))
        print(f"Quantidade solicitada: {quantidade}")  # ✅ quantidade recebida

        tipo_pagamento = request.POST.get('tipo_pagamento')
        print(f"Tipo de pagamento selecionado: {tipo_pagamento}")  # ✅ pagamento

        # Validações
        if quantidade <= 0:
            print("Erro: Quantidade menor ou igual a zero.")
            messages.error(request, 'Quantidade deve ser maior que zero.')
            return redirect('compra', id_produto=id_produto)

        if quantidade > produto.estoque:
            print(f"Erro: Quantidade {quantidade} maior que estoque {produto.estoque}.")
            messages.error(request, 'Quantidade solicitada maior que o estoque disponível.')
            return redirect('compra', id_produto=id_produto)

        if not tipo_pagamento:
            print("Erro: Nenhuma forma de pagamento selecionada.")
            messages.error(request, 'Selecione uma forma de pagamento.')
            return redirect('compra', id_produto=id_produto)

        # Obter cliente
        try:
            cliente = request.user.cliente
            print(f"Cliente encontrado: {cliente.nome}")
        except Cliente.DoesNotExist:
            print("Erro: Cliente não encontrado.")
            messages.error(request, 'Você não possui um cadastro de cliente. Entre em contato com o suporte.')
            return redirect('compra', id_produto=id_produto)

        valor_total = produto.preco * quantidade
        print(f"Valor total da compra: {valor_total}")  # ✅ valor calculado

        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    data_pedido=now(),
                    valor_total=valor_total
                )
                print(f"Pedido criado: ID #{pedido.id_pedido}")  # ✅ pedido criado

                updated_rows = Produto.objects.filter(id_produto=id_produto).update(
                    estoque=F('estoque') - quantidade
                )
                print(f"Linhas de produto atualizadas: {updated_rows}")  # ✅ update aplicado

                produto.refresh_from_db()
                print(f"Estoque após update: {produto.estoque}")  # ✅ novo valor do estoque

                Pagamento.objects.create(
                    pedido=pedido,
                    tipo_pagamento=tipo_pagamento,
                    valor=valor_total
                )
                print("Pagamento criado com sucesso.")  # ✅ pagamento criado

                messages.success(request, f'Compra realizada com sucesso! Pedido #{pedido.id_pedido}')
                return redirect('pedido_detalhe', id_pedido=pedido.id_pedido)

        except Exception as e:
            import traceback
            traceback.print_exc()  # mostra o erro completo no terminal
            messages.error(request, f'Erro ao processar a compra: {str(e)}')
            return redirect('compra', id_produto=id_produto)

    print("Requisição não é POST, redirecionando para produtos.")
    return redirect('produtos')

# Pedidos
@login_required
def pedidos(request):
    """View para listar pedidos do usuário logado"""
    try:
        cliente = Cliente.objects.get(email=request.user.email)
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-data_pedido')
    except Cliente.DoesNotExist:
        pedidos = []

    return render(request, 'pedidos.html', {'pedidos': pedidos})

def pedido_detalhe(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)

    # Verificar se o usuário tem permissão para ver este pedido
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(email=request.user.email)
            if pedido.cliente != cliente and not request.user.is_staff:
                messages.error(request, 'Você não tem permissão para ver este pedido.')
                return redirect('pedidos')
        except Cliente.DoesNotExist:
            if not request.user.is_staff:
                messages.error(request, 'Você não tem permissão para ver este pedido.')
                return redirect('produtos')

    return render(request, 'pedido_detalhe.html', {'pedido': pedido})

# Pagamentos
def pagamentos(request):
    pagamentos = Pagamento.objects.select_related('pedido').all()
    return render(request, 'pagamentos.html', {'pagamentos': pagamentos})

def pagamento_detalhe(request, id_pagamento):
    pagamento = get_object_or_404(Pagamento, id=id_pagamento)
    return render(request, 'pagamento_detalhe.html', {'pagamento': pagamento})
