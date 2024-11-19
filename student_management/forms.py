# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Teacher  # Import User from models

class UserRegistrationForm(UserCreationForm):
    # phone = forms.CharField(required=True, max_length=15)  # Add phone field
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any custom field requirements
        self.fields['email'].required = True
        self.fields['user_type'].required = True

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id', 'grade')

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('teacher_id', 'subject')