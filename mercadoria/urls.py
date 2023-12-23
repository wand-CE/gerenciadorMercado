from django.contrib.auth import views as auth_views
from django.urls import path

from mercadoria import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('accounts/login/', views.LoginUserView.as_view(), name='loginVendedor'),
    path('logout/', auth_views.LogoutView.as_view(), name='logoutVendedor'),

    path('changeConfig/', views.SalvarConfiguracoes.as_view(), name='configuracoes'),
    path('changeUserData/', views.ChangeUserData.as_view(), name='changeUserData'),

    path('criarCategoria/', views.CreateCategory.as_view(), name='criarCategoria'),
    path('listarCategorias/', views.ListCategory.as_view(), name='listarCategorias'),
    path('editarCategoria/<pk>', views.EditCategory.as_view(), name='editarCategoria'),
    path('excluirCategoria/<pk>', views.ExcludeCategory.as_view(), name='excluirCategoria'),

    path('criarProduto/', views.CreateProduto.as_view(), name='criarProduto'),
    path('listarProdutos/', views.ListProduto.as_view(), name='listarProdutos'),
    path('editarProduto/<pk>', views.EditProduto.as_view(), name='editarProduto'),
    path('excluirProduto/<pk>', views.ExcludeProduto.as_view(), name='excluirProduto'),

    path('criarCliente/', views.CreateCliente.as_view(), name='criarCliente'),
    path('listarClientes/', views.ListCliente.as_view(), name='listarClientes'),
    path('editarCliente/<pk>', views.EditCliente.as_view(), name='editarCliente'),
    path('excluirCliente/<pk>', views.ExcludeCliente.as_view(), name='excluirCliente'),

    path('criarCompra/', views.CreateCompra.as_view(), name='criarCompra'),
    path('listarCompras/', views.ListCompra.as_view(), name='listarCompras'),
    path('detalhesCompra/<pk>', views.DetailCompra.as_view(), name='detalharCompra'),
    path('excluirCompra/<pk>', views.ExcludeCompra.as_view(), name='excluirCompra'),

    path('criarClienteJson/', views.CreateClienteJson.as_view(), name='clienteByJson'),
    path('searchProducts/', views.SearchProducts.as_view(), name='searchProducts'),
    path('registrarCompra/', views.CreateCompra.as_view(), name='registrarCompra'),

    path('reports/', views.ReportsView.as_view(), name='reportsPage'),
    path('reportsJson/', views.GenerateReportsView.as_view(), name='reportsJson'),

]
