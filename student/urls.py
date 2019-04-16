from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^library/', views.library),
    url(r'^grade/', views.grade),
    url(r'^internet/', views.internet),
    url(r'^cartoon/', views.cartoon),
    url(r'^fp_growth/',views.fp_growth),
    url(r'^update11/', views.update11),
    url(r'^update12/', views.update12),
    url(r'^update13/', views.update13),
    url(r'^update14/', views.update14),
    url(r'^update15/', views.update15),

    url(r'^update21/', views.update21),
    url(r'^update22/', views.update22),

    #插入假数据函数
    url(r'^student_info_insert/', views.student_info_insert),
    url(r'^library_insert/', views.library_insert),
    url(r'^grade_insert/', views.grade_insert),
    url(r'^internet_insert/', views.internet_insert),
    url(r'^cartoon_insert/', views.cartoon_insert),
    url(r'^award_insert/', views.award_insert),


]