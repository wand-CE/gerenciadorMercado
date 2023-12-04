from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView

from mercadoria.forms import CategoriaForm, ProdutoForm, ClienteForm, VendedorForm, CompraForm
from mercadoria.models import Categoria, Configuracoes, Produto, Cliente, Vendedor, Compra


class ConfiguracoesMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = Configuracoes.objects.first().temaEscuro
        return context


class SalvarConfiguracoes(View):

    def get(self, request):
        tema = request.GET.get('tema', None)
        if tema:
            configuracoes = Configuracoes.objects.first()
            configuracoes.temaEscuro = tema == 'true'
            configuracoes.save()

        return HttpResponse('')


class Home(ConfiguracoesMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = Configuracoes.objects.first().temaEscuro

        return context


class CreateCategory(ConfiguracoesMixin, CreateView):
    model = Categoria
    template_name = 'criarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Categoria"
        return context


class ListCategory(ConfiguracoesMixin, ListView):
    model = Categoria
    template_name = 'listarObjetos.html'
    queryset = Categoria.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Categoria._meta.fields if campo.name != 'id']

        context['nome_pagina'] = "Categorias"
        return context


class EditCategory(ConfiguracoesMixin, UpdateView):
    model = Categoria
    template_name = 'editarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        return context


class ExcludeCategory(ConfiguracoesMixin, DeleteView):
    model = Categoria
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'categoria'
        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateProduto(ConfiguracoesMixin, CreateView):
    model = Produto
    template_name = 'criarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Produto"
        return context


class ListProduto(ConfiguracoesMixin, ListView):
    model = Produto
    template_name = 'listarObjetos.html'
    queryset = Produto.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = ['Nome', 'Preço', 'Qtd.', 'Categoria']
        context['nome_pagina'] = "Produtos"
        return context


class EditProduto(ConfiguracoesMixin, UpdateView):
    model = Produto
    template_name = 'editarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        return context


class ExcludeProduto(ConfiguracoesMixin, DeleteView):
    model = Produto
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'produto'
        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateCliente(ConfiguracoesMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'criarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Cliente"
        return context


class ListCliente(ConfiguracoesMixin, ListView):
    model = Cliente
    template_name = 'listarObjetos.html'
    queryset = Cliente.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Cliente._meta.fields if campo.name != 'id']
        context['nome_pagina'] = "Clientes"
        return context


class EditCliente(ConfiguracoesMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar cliente {context['object'].nome}"
        return context


class ExcludeCliente(ConfiguracoesMixin, DeleteView):
    model = Cliente
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'cliente'
        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateVendedor(ConfiguracoesMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'criarObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Vendedor"
        return context


class ListVendedor(ConfiguracoesMixin, ListView):
    model = Vendedor
    template_name = 'listarObjetos.html'
    queryset = Vendedor.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Vendedor._meta.fields if campo.name != 'id']
        context['nome_pagina'] = "Vendedores"
        return context


class EditVendedor(ConfiguracoesMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar vendedor {context['object'].nome}"
        return context


class ExcludeVendedor(ConfiguracoesMixin, DeleteView):
    model = Vendedor
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'vendedor'
        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateCompra(ConfiguracoesMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'criarCompra.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar compra"
        context['cliente_form'] = ClienteForm
        return context


class ListCompra(ConfiguracoesMixin, ListView):
    model = Compra
    template_name = 'listarObjetos.html'
    queryset = Compra.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Compra._meta.fields if campo.name != 'id']
        context['nome_pagina'] = "Compras"
        return context


class EditCompra(ConfiguracoesMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object']}"
        return context


class ExcludeCompra(ConfiguracoesMixin, DeleteView):
    model = Compra
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'compra'
        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateClienteJson(View):
    def post(self, *args, **kwargs):
        form = ClienteForm(self.request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'nome': f'{cliente}', 'cliente_id': cliente.id})
        else:
            return JsonResponse({'errors': form.errors})
