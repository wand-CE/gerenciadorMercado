from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models


class Configuracoes(models.Model):
    temaEscuro = models.BooleanField(default=False, null=False)


class Categoria(models.Model):
    nome = models.CharField(max_length=40, null=False)
    descricao = models.TextField(null=False)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}


class Produto(models.Model):
    nome = models.CharField(max_length=100, null=False, unique=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True)
    quantidade_estoque = models.IntegerField(
        null=False, default=0, verbose_name='Quantidade em Estoque', validators=[MinValueValidator(0)])
    preco = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0.00,
                                validators=[MinValueValidator(0.00)])

    class Meta:
        unique_together = ('nome', 'categoria')
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}


class Pessoa(models.Model):
    cpf = models.CharField(null=False, unique=True,
                           validators=[MinLengthValidator(11), RegexValidator(r'^\d{11}$',
                                                                              'CPF inválido')],
                           verbose_name='CPF', max_length=11)
    nome = models.CharField(max_length=60, null=False)
    endereco = models.CharField(max_length=150, null=False)
    nascimento = models.DateField(null=False)

    class Meta:
        abstract = True


class Cliente(Pessoa):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome

    def get_fields_dict(self):
        dicionario = {}
        for field in self._meta.fields:
            if field.name != 'endereco':
                dicionario[field.name] = getattr(self, field.name)
        return dicionario


class Vendedor(User):
    cpf = models.CharField(null=False, unique=True,
                           validators=[MinLengthValidator(11), RegexValidator(r'^\d{11}$',
                                                                              'CPF inválido')],
                           verbose_name='CPF', max_length=11)
    endereco = models.CharField(max_length=150, null=False)
    nascimento = models.DateField(null=False)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

    def __str__(self):
        return self.username

    def get_fields_dict(self):
        dicionario = {}
        for field in self._meta.fields:
            if field.name != 'endereco':
                dicionario[field.name] = getattr(self, field.name)
        return dicionario


class Compra(models.Model):
    vendedor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    # depois sera mudado para adicionar vendedor automaticamente com base no vendedor conectado
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    horaCompra = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name='Hora da compra')

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'Compra de {self.cliente} com vendedor {self.vendedor}'

    def valor_total(self):
        items = self.item_compra.all()
        soma = Decimal('0.00')
        for item_compra in items:
            soma += item_compra.precoTotal
        return soma

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}


class ItemCompra(models.Model):
    compra = models.ForeignKey(
        Compra, related_name='item_compra', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, models.SET_NULL, null=True)
    quantidade = models.IntegerField(null=False)
    precoAtual = models.DecimalField(max_digits=5, decimal_places=2, null=False, validators=[MinValueValidator(0.00)],
                                     editable=False, verbose_name='Preço Atual')
    precoTotal = models.DecimalField(max_digits=7, decimal_places=2, null=False, validators=[MinValueValidator(0.00)],
                                     editable=False, verbose_name='Preço Total')

    class Meta:
        unique_together = ('compra', 'produto')
        verbose_name = 'Item da compra'
        verbose_name_plural = 'Itens da compra'

    def save(self, *args, **kwargs):
        self.precoAtual = self.produto.preco
        self.precoTotal = self.precoAtual * self.quantidade
        super().save(*args, **kwargs)
