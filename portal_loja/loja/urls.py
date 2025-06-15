from django.urls import path
from . import views

urlpatterns = [
    # Página principal (home)
    path('', views.index, name='index'),
    path('principal/', views.index, name='principal'),  # rota adicional para principal

    # Autenticação
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/cadastro/', views.cadastro, name='cadastro'),

    # Categorias de Produto
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:id_categoria>/', views.categoria_detalhe, name='categoria_detalhe'),

    # Produtos
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<int:id_produto>/', views.produto_detalhe, name='produto_detalhe'),

    # Compras
    path('compra/<int:id_produto>/', views.compra, name='compra'),
    path('finalizar_compra/<int:id_produto>/', views.finalizar_compra, name='finalizar_compra'),

    # Pedidos
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/<int:id_pedido>/', views.pedido_detalhe, name='pedido_detalhe'),

    # Clientes (páginas administrativas)
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:id_cliente>/', views.cliente_detalhe, name='cliente_detalhe'),

    # Pagamentos (páginas administrativas)
    path('pagamentos/', views.pagamentos, name='pagamentos'),
    path('pagamentos/<int:id_pagamento>/', views.pagamento_detalhe, name='pagamento_detalhe'),
]
