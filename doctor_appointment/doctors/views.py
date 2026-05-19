from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import DoctorProfile,User
from django.db.models import Q


#doctors er list dekhabe all doctor a
def doctor_list(request):

    speciality = request.GET.get('speciality')
    doctors = DoctorProfile.objects.all()

    if speciality:
        doctors = doctors.filter(speciality__icontains=speciality)

    return render(request, 'doctor_list.html', {'doctors': doctors,'active_speciality': speciality})


# search bar a search korar jonno
def search_doctors(request):
    query = request.GET.get('q')
    doctors = DoctorProfile.objects.filter(
        Q(name__icontains=query) |
        Q(speciality__icontains=query)
    )
    return render(request, 'doctor_list.html', {'doctors': doctors})


#doctor list theke ekta doctor a click korle doctor er detail dekhabe
def doctor_detail(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    return render(request, "doctor_detail.html", context={'doctor':doctor})




#admin jodi doctor add korte chay
@login_required
def add_doctor(request):

    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role="DOCTOR"
        )

        DoctorProfile.objects.create(
            image=request.FILES.get("image"),
            user=user,
            name=request.POST.get("name"),
            speciality=request.POST.get("speciality"),
            experience=request.POST.get("experience"),
            address=request.POST.get("address"),
            fees=request.POST.get("fees"),
            about=request.POST.get("about"),
            is_available=True
        )

        return redirect("doctor_list")

    return render(request, "add_doctor.html")




def symptom_checker(request):

    doctors = None
    speciality = None
    selected_symptom = None

    if request.method == "POST":

        symptom = request.POST.get("symptom")
        selected_symptom = symptom


        if symptom in ["Fever", "Cold & Cough"]:
            speciality = "General Physician"
        elif symptom in ["Headache", "Dizziness"]:
            speciality = "Neurologist"
        elif symptom in ["Skin Rash", "Acne"]:
            speciality = "Dermatologist"
        elif symptom in ["Child Fever", "Child Cold"]:
            speciality = "Pediatrician"
        elif symptom == "Pregnancy Issues":
            speciality = "Gynocologist"
        elif symptom in ["Stomach Pain", "Vomiting"]:
            speciality = "Gastroenterologist"
        elif symptom in ["Bone Pain", "Joint Pain"]:
            speciality = "Orthopedic"
        elif symptom in ["Chest Pain", "Heart Problem"]:
            speciality = "Cardiologist"
        else:
            speciality = "General physician"

        doctors = DoctorProfile.objects.filter(
            speciality=speciality
        )

    return render(request, 'symptom_checker.html', {'doctors': doctors,'speciality': speciality,'selected_symptom': selected_symptom})