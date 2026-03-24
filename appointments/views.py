from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Doctor, Appointment
from .forms import UserRegisterForm, AppointmentForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('my_appointments')
    else:
        form = AppointmentForm(initial={'doctor': doctor})
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    return render(request, 'my_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, patient=request.user)
    if appointment:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
    return redirect('my_appointments')
