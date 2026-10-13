from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, CourseForm, AcademicGroupForm
from .models import AcademicGroup, Course, Department


def is_methodist(user):
    return user.groups.filter(
        name='Методист'
    ).exists()


@login_required
def profile(request):
    departments = Department.objects.all()

    chart_data = {
        'labels': [d.name for d in departments],
        'courses': [d.courses.count() for d in departments],
        'groups': [d.groups.count() for d in departments],
    }

    return render(
        request,
        'profile.html',
        {
            'is_methodist': is_methodist(
                request.user
            ),
            'departments_count': departments.count(),
            'groups_count': AcademicGroup.objects.count(),
            'courses_count': Course.objects.count(),
            'chart_data': chart_data,
        }
    )


@login_required
def department_list(request):
    departments = Department.objects.all()

    return render(
        request,
        'department_list.html',
        {
            'departments': departments,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_create(request):

    if request.method == 'POST':
        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Факультет добавлен.')

            return redirect(
                'department_list'
            )

    else:
        form = DepartmentForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление факультета',
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_update(
        request,
        pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Факультет изменён.')
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm(
            instance=department
        )
    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение факультета',
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_delete(
        request,
        pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Факультет удалён.')
        return redirect(
            'department_list'
        )
    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': department,
            'title': 'Удаление факультета',
        }
    )


@login_required
def course_list(request):
    courses = Course.objects.select_related(
        'department'
    )

    department_id = request.GET.get('department', '')
    current_department = int(department_id) if department_id.isdigit() else None
    if current_department:
        courses = courses.filter(department_id=current_department)

    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'departments': Department.objects.all(),
            'current_department': current_department,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
def academic_group_list(request):
    groups = AcademicGroup.objects.select_related(
        'department'
    )

    department_id = request.GET.get('department', '')
    current_department = int(department_id) if department_id.isdigit() else None
    if current_department:
        groups = groups.filter(department_id=current_department)

    return render(
        request,
        'group_list.html',
        {
            'groups': groups,
            'departments': Department.objects.all(),
            'current_department': current_department,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):

    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Группа добавлена.')

            return redirect(
                'academic_group_list'
            )

    else:
        form = AcademicGroupForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_update(
        request,
        pk
):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )
    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST,
            instance=group
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Группа изменена.')
            return redirect(
                'academic_group_list'
            )
    else:
        form = AcademicGroupForm(
            instance=group
        )
    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_delete(
        request,
        pk
):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Группа удалена.')
        return redirect(
            'academic_group_list'
        )
    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': group,
            'title': 'Удаление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_create(request):

    if request.method == 'POST':
        form = CourseForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Курс добавлен.')

            return redirect(
                'course_list'
            )

    else:
        form = CourseForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_update(
        request,
        pk
):
    course = get_object_or_404(
        Course,
        pk=pk
    )
    if request.method == 'POST':
        form = CourseForm(
            request.POST,
            instance=course
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс изменён.')
            return redirect(
                'course_list'
            )
    else:
        form = CourseForm(
            instance=course
        )
    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_delete(
        request,
        pk
):
    course = get_object_or_404(
        Course,
        pk=pk
    )
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс удалён.')
        return redirect(
            'course_list'
        )
    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': course,
            'title': 'Удаление курса',
        }
    )
