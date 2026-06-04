from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
import base64

from django.core.files.base import ContentFile
@login_required(login_url='login')
def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        'students/student_list.html',
        {'students': students}
    )


@login_required(login_url='login')
def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            student = form.save(commit=False)

            captured_image = request.POST.get(
                'captured_image'
            )

            if captured_image:

                format, imgstr = captured_image.split(';base64,')

                ext = format.split('/')[-1]

                student.photo.save(
                    f"{student.student_id}.{ext}",
                    ContentFile(
                        base64.b64decode(imgstr)
                    ),
                    save=False
                )

            student.save()

            return redirect(
                'students:student_list'
            )

    else:

        form = StudentForm()

    return render(
        request,
        'students/add_student.html',
        {'form': form}
    )

@login_required(login_url='login')
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect('students:student_list')

    else:
        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'students/edit_student.html',
        {
            'form': form,
            'student': student
        }
    )

@login_required(login_url='login')
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    return redirect('students:student_list')

@login_required(login_url='login')
def student_profile(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    return render(
        request,
        'students/student_profile.html',
        {'student': student}
    )