from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Score


def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    scores = Score.objects.filter(student=student)
    total_score = sum(score.score for score in scores)
    avg_score = round(total_score / scores.count(), 2) if scores else 0
    grade = 'A' if avg_score >= 80 else 'B' if avg_score >= 60 else 'C'
    return render(request, 'student_app/student_detail.html', {
        'student': student,
        'scores': scores,
        'avg_score': avg_score,
        'grade': grade
    })

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    scores = Score.objects.filter(subject=subject)
    students = Student.objects.all()

    # 성적 수정 처리
    if request.method == 'POST':
        if 'score_id' in request.POST and 'score_value' in request.POST:
            score_id = request.POST.get('score_id')
            new_score_value = request.POST.get('score_value')
            score = get_object_or_404(Score, id=score_id)
            score.score = new_score_value  # 점수 수정
            score.save()  # 수정된 점수 저장
            return redirect('subject_detail', subject_id=subject.id)

        elif 'delete_score_id' in request.POST:
            score_id = request.POST.get('delete_score_id')
            score = get_object_or_404(Score, id=score_id)
            score.delete()  # 점수 삭제
            return redirect('subject_detail', subject_id=subject.id)

    return render(request, 'student_app/subject_detail.html', {
        'subject': subject,
        'scores': scores,
        'students': students,
    })


def delete_student_from_subject(request, subject_id):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)

        # 해당 학생의 성적 삭제
        score = Score.objects.filter(student=student, subject=subject)
        score.delete()

        # 과목 상세 페이지로 리디렉션
        return redirect('subject_detail', subject_id=subject_id)

    return redirect('subject_detail', subject_id=subject_id)  # GET 요청 시에는 그냥 리디렉션


def update_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.method == 'POST':
        score_value = request.POST.get('score')
        if score_value:
            score.score = score_value
            score.save()
        return redirect('subject_detail', subject_id=score.subject.id)
    return render(request, 'student_app/update_score.html', {'score': score})


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.delete()
        return redirect('main_page')

    return render(request, 'student_app/confirm_delete.html', {'subject': subject})

def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        # 새로운 과목을 추가하는 코드
        Subject.objects.create(name=name, description=description)
        return redirect('main_page')  # 과목 추가 후 첫 페이지로 리디렉션
    return render(request, 'student_app/add_subject.html')  # 과목 추가 폼을 보여주는 템플릿

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        # POST 요청이 오면 삭제 수행
        subject.delete()
        return redirect('main_page')
    
    # GET 요청이 오면 삭제 확인 페이지 렌더링
    return render(request, 'student_app/confirm_delete.html', {'subject': subject})



def main_page(request):
    # 학생 정보와 과목 정보를 가져옵니다.
    students = Student.objects.all()
    subjects = Subject.objects.all()

    student_data = []
    
    # 학생별로 평균 점수와 grade를 계산합니다.
    for student in students:
        scores = student.scores.all()  # 학생의 성적을 가져옵니다.
        total_score = sum(score.score for score in scores) if scores else 0
        avg_score = round(total_score / len(scores), 2) if scores else 0
        grade = 'A' if avg_score >= 80 else 'B' if avg_score >= 60 else 'C'

        # 학생 정보를 딕셔너리로 저장합니다.
        student_data.append({
            'id': student.student_id,
            'name': student.name,
            'age': student.age,
            'avg_score': avg_score,
            'grade': grade
        })

    # 템플릿에 데이터 전달
    return render(request, 'student_app/home.html', {
        'students': student_data,
        'subjects': subjects
    })

def delete_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)  # 삭제할 점수 가져오기
    score.delete()  # 점수 삭제
    return redirect('student_detail', student_id=score.student.student_id)  # 학생 상세 페이지로 리디렉션

def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)  # 폼을 POST 데이터로 업데이트
        if form.is_valid():
            form.save()  # 수정된 학생 정보 저장
            return redirect('student_detail', student_id=student_id)  # 수정 후 학생 상세 페이지로 리디렉션
    else:
        form = StudentForm(instance=student)  # 기존 학생 정보를 폼에 로드
    
    return render(request, 'student_app/edit_student.html', {'form': form, 'student': student})


from django.shortcuts import render, redirect
from .forms import SubjectForm
from .models import Subject

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()  # 폼 데이터 저장
            return redirect('subject_list')  # subject_list로 리다이렉트
    else:
        form = SubjectForm()  # GET 요청일 때 폼 생성
    
    return render(request, 'add_subject.html', {'form': form})

# student_app/views.py

from django.shortcuts import render
from .models import Subject

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'student_app/subject_list.html', {'subjects': subjects})
