from django.urls import path
from . import views

urlpatterns = [
    path("addc/",views.AddCategoryView.as_view()),
    path("addp/",views.AddProductView.as_view()),
    path("dltprod/",views.DltProductView.as_view()),
    path("dltcat/",views.DltcategoryView.as_view()),
    path("update/",views.UpdateProductView.as_view()),
    path("get/<int:pk>/",views.RetrieveView.as_view()),
    path("allprods/",views.CatelogWiseData.as_view()),
    path("testdata/",views.CategoryRelatedView.as_view())
    ]

    