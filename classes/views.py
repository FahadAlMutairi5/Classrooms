from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  SignupForm, SigninForm, ClassroomForm, StudentForms
from .models import Classroom, Student
from django.contrib.auth import login, authenticate, logout


def classroom_list(request):
    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    items = classroom.students.all().order_by('name' , '-exam_grade')
    context = {
        "classroom": classroom,
        "items":items
    }
    return render(request, 'classroom_detail.html', context)

def student_create(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    form = StudentForms()
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == "POST":
        form = StudentForms(request.POST)
        if form.is_valid():
            Student_obj = form.save(commit=False)
            Student_obj.classroom = classroom
            Student_obj.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-detail', classroom_id)
        print (form.errors)
    context = {
    "form": form,
    "classroom_obj":classroom
    }
    return render(request, 'create_setudent.html', context)


def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            classroom_obj = form.save(commit=False)
            classroom_obj.teacher = request.user
            classroom_obj.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)

def student_update(request, student_id, classroom_id):
    student = Student.objects.get(id=student_id)
    form = StudentForms(instance=student)
    if request.method == "POST":
        form = StudentForms(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-detail', classroom_id)
        print (form.errors)
    context = {
    "form": form,
    "Student": student,
    "classroom_id": classroom_id
    }
    return render(request, 'update_student.html', context)


def student_delete(request, student_id, classroom_id):
    Student.objects.get(id=student_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail', classroom_id)

def classroom_delete(request, classroom_id):
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)
def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")
