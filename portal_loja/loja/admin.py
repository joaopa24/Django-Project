from django.contrib import admin
from .models import Cliente, Categoria, Produto, Pedido, ItemPedido, Pagamento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone", "cpf")
    search_fields = ("nome", "email", "cpf")
    list_filter = ("telefone",)
    ordering = ("nome",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "marca", "estoque", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nome", "marca", "categoria__nome")
    ordering = ("nome",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id_pedido", "cliente", "data_pedido", "status", "valor_total")
    list_filter = ("status", "data_pedido")
    search_fields = ("cliente__nome", "status")
    ordering = ("-data_pedido",)


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade", "preco_unitario")
    search_fields = ("pedido__id_pedido", "produto__nome")
    list_filter = ("produto",)
    ordering = ("pedido",)


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("id_pagamento", "pedido", "tipo_pagamento", "data_pagamento", "valor")
    search_fields = ("pedido__id_pedido", "tipo_pagamento")
    list_filter = ("tipo_pagamento", "data_pagamento")
    ordering = ("-data_pagamento",)
