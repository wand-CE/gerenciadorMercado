from django.urls import path

from mercadoria import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('changeConfig/', views.SalvarConfiguracoes.as_view(), name='configuracoes'),

    path('criarCategoria/', views.CreateCategory.as_view(), name='criarCategoria'),
    path('listarCategorias/', views.ListCategory.as_view(), name='listarCategorias'),
    path('editarCategoria/<pk>', views.EditCategory.as_view(), name='editarCategoria'),
    path('excluirCategoria/<pk>', views.ExcludeCategory.as_view(), name='excluirCategoria'),

    path('criarProduto/', views.CreateProduto.as_view(), name='criarProduto'),
    path('listarProdutos/', views.ListProduto.as_view(), name='listarProdutos'),
    path('editarProduto/<pk>', views.EditProduto.as_view(), name='editarProduto'),
    path('excluirProduto/<pk>', views.ExcludeProduto.as_view(), name='excluirProduto'),
]
