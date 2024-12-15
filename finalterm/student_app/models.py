from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    grade = models.CharField(max_length=2)
    student_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    textbook = models.CharField(max_length=100)
    class_time = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()


    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"
