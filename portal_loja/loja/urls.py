from django.urls import path
from . import views

urlpatterns = [
    #Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    #landing page - produtos - preferencia com filtragem
    #pagina do produto
    #fluxo de pagamento simples sem integração com gateway de pagamento
    #página de conclusão/agradecimento da compra
    
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:id_cliente>/', views.cliente_detalhe, name='cliente_detalhe'),

    # Categorias de Produto
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:id_categoria>/', views.categoria_detalhe, name='categoria_detalhe'),

    # Produtos
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<int:id_produto>/', views.produto_detalhe, name='produto_detalhe'),

    # Pedidos
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/<int:id_pedido>/', views.pedido_detalhe, name='pedido_detalhe'),

    # Pagamentos
    path('pagamentos/', views.pagamentos, name='pagamentos'),
    path('pagamentos/<int:id_pagamento>/', views.pagamento_detalhe, name='pagamento_detalhe'),
]
