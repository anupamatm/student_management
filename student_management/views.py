from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserRegistrationForm, StudentProfileForm, TeacherProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user_type == 'teacher':
            return reverse_lazy('teacher_dashboard')
        elif user_type == 'student':
            return reverse_lazy('student_dashboard')
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

# views.py
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # student_form = StudentProfileForm(request.POST)
        teacher_form = TeacherProfileForm(request.POST)

        if user_form.is_valid():
            user = None  # Initialize user as None
            try:
                user = user_form.save(commit=False)
                # user.phone = user_form.cleaned_data.get('phone')  # Set phone field
                user.save()  # Save the user first

                user_type = user_form.cleaned_data.get('user_type')

                # if user_type == 'student':
                #     if student_form.is_valid():
                #         student = student_form.save(commit=False)
                #         student.user = user
                #         student.save()
                #     else:
                #         if user:
                #             user.delete()
                #         messages.error(request, f'Student form errors: {student_form.errors}')
                #         return render(request, 'registration/register.html', {
                #             'form': user_form,
                #             'student_form': student_form,
                #             'teacher_form': TeacherProfileForm()
                #         })

                if user_type == 'teacher':
                    if teacher_form.is_valid():
                        teacher = teacher_form.save(commit=False)
                        teacher.user = user
                        teacher.save()
                    else:
                        if user:
                            user.delete()
                        messages.error(request, f'Teacher form errors: {teacher_form.errors}')
                        return render(request, 'registration/register.html', {
                            'form': user_form,
                            'student_form': StudentProfileForm(),
                            'teacher_form': teacher_form
                        })

                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('home')

            except Exception as e:
                if user and user.id:
                    user.delete()
                messages.error(request, f'Registration error: {str(e)}')
        else:
            messages.error(request, f'User form errors: {user_form.errors}')
    else:
        user_form = UserRegistrationForm()
        # student_form = StudentProfileForm()
        teacher_form = TeacherProfileForm()

    return render(request, 'registration/register.html', {
        'form': user_form,
        # 'student_form': student_form,
        'teacher_form': teacher_form
    })

def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to the home page or any other desired page
# Decorator functions for role-based access
def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def is_teacher(user):
    return user.is_authenticated and user.user_type == 'teacher'

def is_student(user):
    return user.is_authenticated and user.user_type == 'student'

# Example protected views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher.html')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    return render(request, 'dashboard/student.html')