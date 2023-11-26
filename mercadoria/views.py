from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView

from mercadoria.forms import CategoriaForm, ProdutoForm
from mercadoria.models import Categoria, Configuracoes, Produto


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
        context['nome_pagina'] = "Criar Categoria"
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
        context['nome_pagina'] = "Criar Produto"
        return context


class ListProduto(ConfiguracoesMixin, ListView):
    model = Produto
    template_name = 'listarObjetos.html'
    queryset = Produto.objects.all()
    context_object_name = 'elementos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = []
        for campo in Produto._meta.fields:
            if campo.name != 'id':
                if campo.name == 'quantidade_estoque':
                    context['campos_objeto'].append('Qtd.')
                else:
                    context['campos_objeto'].append(campo.name.title())

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
