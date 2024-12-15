from django.contrib import admin
from django.urls import path, include  # include를 사용하여 다른 URLconf를 연결합니다.

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin 페이지를 위한 URL
    path('', include('student_app.urls')),  # 'student_app'의 URL 설정을 포함시킵니다.
]
