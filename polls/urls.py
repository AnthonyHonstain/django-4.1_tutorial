from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Two similar paths, to experiment with an async version '/adetail' against the normal synchronous version
    path('<int:question_id>/adetail', views.detail, name='adetail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]