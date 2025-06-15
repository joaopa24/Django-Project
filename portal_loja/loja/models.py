from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=255, blank=True, null=True)
    estoque = models.IntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='produtos',
        db_column='id_categoria'
    )

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pedidos',
        db_column='id_cliente'
    )
    data_pedido = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nome}"


class ItemPedido(models.Model):
    id_item = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
        db_column='id_pedido'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='itens_pedido',
        db_column='id_produto'
    )
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.preco_unitario is None:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)

class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pagamento',
        db_column='id_pedido'
    )
    tipo_pagamento = models.CharField(max_length=50)
    data_pagamento = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pagamento #{self.id_pagamento} - Pedido #{self.pedido.id_pedido}"
