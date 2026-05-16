from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import PatientProfile
from django.contrib.auth.decorators import login_required



# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "PATIENT"
            user.save()

            PatientProfile.objects.create(
                user=user,
                full_name=user.username
            )

            return redirect("login")

        else:
            print(form.errors)  # terminal er debug korar jonno deya

    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ei system email ke username hisebe ney ei karone
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # ke login korteche oita dekha r jonno
            if user.role == "DOCTOR":
                return redirect("doctor_profile")
            elif user.role == "PATIENT":
                return redirect("patient_profile")
            elif user.role == "ADMIN":
                return redirect("/")  # django er admin panel a jabe
            else:
                return redirect("home")

        else:
            return render(request, "login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "login.html")


@login_required
def patient_profile(request):

    profile = request.user.patientprofile
    edit_mode = request.GET.get('edit') == 'true'

    if request.method == "POST":

        profile.full_name = request.POST.get('full_name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.gender = request.POST.get('gender')
        profile.date_of_birth = request.POST.get('date_of_birth')

        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')

        profile.save()
        return redirect('patient_profile')

    context = {
        'profile': profile,
        'edit_mode': edit_mode,
    }

    return render(request, 'patient_profile.html', context )


@login_required
def doctor_profile(request):

    profile = request.user.doctorprofile
    edit_mode = request.GET.get('edit') == 'true'

    if request.method == "POST":

        profile.name = request.POST.get('name')
        profile.speciality = request.POST.get('speciality')
        profile.experience = request.POST.get('experience')
        profile.address = request.POST.get('address')
        profile.fees = request.POST.get('fees')
        profile.about = request.POST.get('about')
        profile.is_available = request.POST.get('is_available') == 'True'

        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')

        profile.save()

        return redirect('doctor_profile')

    context = {
        'profile': profile,
        'edit_mode': edit_mode,
    }

    return render(request, 'doctor_profile.html', context)


def logout_view(request):

    logout(request)
    return redirect('home')