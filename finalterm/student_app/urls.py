from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('delete_student_from_subject/<int:subject_id>/', views.delete_student_from_subject, name='delete_student_from_subject'),  # 이 라인 확인
    path('update_score/<int:score_id>/', views.update_score, name='update_score'),  # 여기에 추가
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),  # 학생 수정
     path('delete_score/<int:score_id>/', views.delete_score, name='delete_score'),
      path('add_subject/', views.add_subject, name='add_subject'),
    path('subject_list/', views.subject_list, name='subject_list'),  # subject_list URL 패턴 추가
]
