from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UserProfileForm, CreateUserForm
from .models import User, Subject, TeacherSubject


# ===============================
# LOGIN
# ===============================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request,
                                username=username,
                                password=password)

            if user:
                login(request, user)
                messages.success(
                    request,
                    f"Welcome {user.get_full_name() or user.username}"
                )
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid login details")

    else:
        form = LoginForm()

    return render(request,
                  'accounts/login.html',
                  {'form': form})


# ===============================
# LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/accounts/login/')


# ===============================
# PROFILE
# ===============================
@login_required
def profile_view(request):

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect('profile')

    else:
        form = UserProfileForm(instance=request.user)

    return render(request,
                  'accounts/profile.html',
                  {'form': form})


# ===============================
# MANAGE USERS (Principal only)
# ===============================
@login_required
def manage_users(request):

    if not request.user.is_principal:
        messages.error(request, "Access denied")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Staff added")
            return redirect('manage_users')
    else:
        form = CreateUserForm()

    users = User.objects.all().order_by('role')

    return render(request,
                  'accounts/manage_users.html',
                  {
                      'users': users,
                      'form': form
                  })


# ===============================
# SUBJECT PERMISSION HELPER
# ===============================
def teacher_has_subject_access(user, subject_id):

    if user.role == "principal":
        return True

    if user.role == "staff":
        return TeacherSubject.objects.filter(
            teacher=user,
            subject_id=subject_id
        ).exists()

    return False


# ===============================
# ASSIGN SUBJECT (Principal)
# ===============================
@login_required
def assign_subject(request):

    if request.user.role != "principal":
        messages.error(request, "Access denied")
        return redirect("dashboard")

    teachers = User.objects.filter(role="staff")
    subjects = Subject.objects.all()

    if request.method == "POST":

        teacher_id = request.POST.get("teacher")
        subject_id = request.POST.get("subject")

        TeacherSubject.objects.get_or_create(
            teacher_id=teacher_id,
            subject_id=subject_id
        )

        messages.success(request, "Subject assigned")
        return redirect("assign_subject")

    assignments = TeacherSubject.objects.select_related(
        "teacher",
        "subject"
    )

    return render(request,
                  "accounts/assign_subject.html",
                  {
                      "teachers": teachers,
                      "subjects": subjects,
                      "assignments": assignments
                  })


# ===============================
# TEACHER DASHBOARD
# ===============================
@login_required
def teacher_dashboard(request):

    if request.user.role == "staff":
        subjects = Subject.objects.filter(
            teachersubject__teacher=request.user
        )
    else:
        subjects = Subject.objects.all()

    return render(request,
                  "dashboard.html",
                  {
                      "subjects": subjects
                  })


# ===============================
# ATTENDANCE EXAMPLE VIEW
# ===============================
@login_required
def take_attendance(request, subject_id):

    if not teacher_has_subject_access(request.user,
                                      subject_id):
        messages.error(
            request,
            "You cannot access this subject"
        )
        return redirect("dashboard")

    subject = get_object_or_404(Subject,
                               id=subject_id)

    return render(request,
                  "attendance/take_attendance.html",
                  {
                      "subject": subject
                  })