from django.shortcuts import render, redirect, get_object_or_404
from .models import Post  # Assuming Post model is in faculty.models
from .forms import PostForm  # Assuming PostForm is in faculty.forms
from django.core.mail import send_mail
def facultyhomepage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_post')
    else:
        form = PostForm()
    posts = Post.objects.all()
    return render(request, 'facultyapp/blogPost.html', {'form': form, 'posts': posts})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('add_post')


from .forms import AddCourseForm
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:FacultyHomePage')
    else:
        form = AddCourseForm()
    return render(request, 'facultyapp/add_course.html', {'form': form})


from .models import AddCourse
from adminapp.models import StudentList

def view_student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    student_courses = AddCourse.objects.all()
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)
    students = StudentList.objects.filter(id__in=student_courses.values('student_id'))
    course_choices = AddCourse.COURSE_CHOICES
    section_choices = AddCourse.SECTION_CHOICES
    context = {
        'students': students,
        'course_choices': course_choices,
        'section_choices': section_choices,
        'selected_course': course,
        'selected_section': section,
    }
    return render(request, 'facultyapp/view_student_list.html', context)
from .forms import MarksForm

def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            marks_instance.save()

            # Retrieve the User email based on the student in the form
            student = marks_instance.student
            student_user = student.user
            user_email = student_user.email

            subject = 'Marks Entered'
            message = f'Hello, {student_user.first_name}  marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
            from_email = 'deepak@gmail.com'
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'facultyapp/marks_success.html')
    else:
        form = MarksForm()
    return render(request, 'facultyapp/post_marks.html', {'form': form})


# contacts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm, SearchForm


def contact_list(request):
    search_form = SearchForm(request.GET or None)
    contacts = Contact.objects.all()
    if search_form.is_valid():
        query = search_form.cleaned_data['search_query']
        contacts = contacts.filter(name__icontains=query) | contacts.filter(email__icontains=query)

    return render(request, 'contacts/contact_list.html', {'contacts': contacts, 'search_form': search_form})


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send email after creating a contact (optional)
            if request.POST.get('send_email'):
                send_mail(
                    subject='New Business Contact Created',
                    message=f"Contact Details:\nName: {contact.name}\nEmail: {contact.email}\n"
                            f"Phone: {contact.phone_number}\nAddress: {contact.address}",
                    from_email='your-email@example.com',
                    recipient_list=[request.POST.get('email_to')],
                )
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'contacts/add_contact.html', {'form': form})


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('contact_list')