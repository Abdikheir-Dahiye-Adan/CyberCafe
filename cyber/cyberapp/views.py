from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Payment, Usage_sessions
from .forms import StudentForm, PaymentForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

# ...existing code...
@login_required
def home(request):
    # load students and attach current active session (if any) to each student object
    students = list(Student.objects.all())  # convert to list so we can add attrs
    active_sessions = Usage_sessions.objects.filter(is_active=True, end_date__isnull=True).select_related('student')
    sess_map = {s.student.id: s for s in active_sessions}  # or use s.student.idnumber if you want to map by idnumber
    for st in students:
        st.active_session = sess_map.get(st.id)  # or sess_map.get(st.idnumber) if using idnumber
        st.last_session = Usage_sessions.objects.filter(student=st, is_active=False).order_by('-end_date').first()
    return render(request, 'home.html', {'students': students})
# ...existing code...

@login_required
def students_list(request):
    MONTHLY_FEE = 3000
    students = list(Student.objects.all())
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    for st in students:
        # Payments made this month
        payments_this_month = st.payments.filter(date__gte=month_start)
        st.amount_paid = sum(p.amount for p in payments_this_month)
        st.balance = MONTHLY_FEE - st.amount_paid if MONTHLY_FEE - st.amount_paid > 0 else 0
    return render(request, 'students_list.html', {'students': students})

@login_required
def student_detail(request, idnumber):
    student = Student.objects.get(id=idnumber)
    payments = student.payments.all()
    return render(request, 'student_detail.html', {'student': student, 'payments': payments})

def payment_list(request):
    MONTHLY_FEE = 3000
    payments = Payment.objects.all()

    # Get current month range
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Find students who have paid at least 3000 this month
    students = Student.objects.all()
    fully_paid_students = []
    for st in students:
        payments_this_month = st.payments.filter(date__gte=month_start)
        total_paid = sum(p.amount for p in payments_this_month)
        if total_paid >= MONTHLY_FEE:
            fully_paid_students.append(st)

    no_fully_paid_message = ""
    if not fully_paid_students:
        no_fully_paid_message = "No student has fully paid this month."

    return render(
        request,
        'payment_list.html',
        {
            'payments': payments,
            'fully_paid_students': fully_paid_students
            'no_fully_paid_message': no_fully_paid_message
        }
    )

def student_payments(request, idnumber):
    student = Student.objects.get(id=idnumber)
    payments = student.payments.all()
    return render(request, 'student_payments.html', {'student': student, 'payments': payments})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            idnumber = form.cleaned_data['idnumber']
            if not Student.objects.filter(idnumber=idnumber).exists():
                form.save()
                return redirect('students_list')
            else:
                form.add_error('idnumber', 'Student with this ID number already exists.')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

#delete student function
def delete_student(request, idnumber):
    student = get_object_or_404(Student, idnumber=idnumber)
    student.delete()
    return redirect('students_list')

def delete_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.delete()
    return redirect('payment_list')

def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form})

# update student function
@login_required
def update_student(request, idnumber):
    student = get_object_or_404(Student, idnumber=idnumber)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'update_student.html', {'form': form})

def active_sessions(request):
    students = Student.objects.all()
    for st in students:
        # Get the most recent session for this student
        recent_session = Usage_sessions.objects.filter(student=st).order_by('-start_date').first()
        st.active_session = recent_session if recent_session and recent_session.is_active and recent_session.end_date is None else None
    active_sessions = Usage_sessions.objects.filter(is_active=True, end_date__isnull=True).select_related('student')
    return render(request, 'active_sessions.html', {'active_sessions': active_sessions, 'students': students})

def start_session(request, idnumber):
    student = get_object_or_404(Student, idnumber=idnumber)
    session = Usage_sessions.objects.create(student=student,is_active=True)
    return redirect('home')

def end_session(request, idnumber):
    student = get_object_or_404(Student, idnumber=idnumber)
    session = Usage_sessions.objects.filter(student=student, is_active=True, end_date__isnull=True).first()

    if session:
        session.end_date = timezone.now()
        session.is_active = False
        session.save()
    return redirect('home')

def send_stk(request, idnumber):
    student = get_object_or_404(Student, idnumber=idnumber)
    # Logic to send STK push goes here
    # This could involve calling an external API or service

    # For now, we just redirect back to home
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Add authentication logic here
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html',{'message':'Login unsuccessful'})
        # For now, we just redirect to home
    return render(request, 'login.html')




