from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proposal_entries/', views.proposal_entries, name='proposal_entries'),
    path('midTermNotice/', views.midTermNotice, name='midTermNotice'),
    path('proposalNotice/', views.proposalNotice, name='proposalNotice'),
    path('finalNotice/', views.finalNotice, name='finalNotice'),
    path('students/', views.students, name='students'),
    # path('supervisor/', views.supervisor, name='supervisor'),
    # path('examiner/', views.examiner, name='examiner'),
    path('midterm_entries/', views.midterm_entries, name='midterm_entries'),
    path('final_entries/', views.final_entries, name='final_entries'),
    path('mid_term_thesis_defense_list', views.midtermthesislist, name='mid_term_thesis_defense_list'),
    path('final_thesis_defense_list', views.finalthesislist, name='final_thesis_defense_list'),
    path('results', views.results, name='results'),
    # path('admin_setting', views.admin, name='admin_setting'),
    # path('budget', views.budget, name='budget'),
    path('invalid', views.invalid, name='invalid'),

]
