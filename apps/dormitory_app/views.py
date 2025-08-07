from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .forms import YotoqxonaArizaForm
from .models import YotoqxonaAriza


def home_view(request):
    """Asosiy sahifa - Ariza formasi"""
    if request.method == 'POST':
        form = YotoqxonaArizaForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Arizani saqlash
                    ariza = form.save(commit=False)
                    
                    # O'quv yilini aniqlash
                    now = timezone.now()
                    if now.month >= 9:
                        ariza.oquv_yili = f"{now.year}-{now.year + 1}"
                    else:
                        ariza.oquv_yili = f"{now.year - 1}-{now.year}"
                    
                    # Holat yangi
                    ariza.holat = 'yangi'
                    
                    # Saqlash
                    ariza.save()
                    
                    # Success message
                    messages.success(
                        request,
                        f"Hurmatli {ariza.fish}! Sizning arizangiz muvaffaqiyatli qabul qilindi."
                    )
                    
                    # Success sahifaga o'tish
                    return redirect('dormitory:success', ariza_raqami=ariza.ariza_raqami)
                    
            except Exception as e:
                messages.error(
                    request,
                    f"Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
                )
                print(f"Xatolik: {str(e)}")  # Debug uchun
    else:
        form = YotoqxonaArizaForm()
    
    context = {
        'form': form,
        'title': 'Yotoqxonaga Ariza Berish'
    }
    
    return render(request, 'home.html', context)


def success_view(request, ariza_raqami):
    """Ariza muvaffaqiyatli yuborilgandan keyingi sahifa"""
    try:
        ariza = YotoqxonaAriza.objects.get(ariza_raqami=ariza_raqami)
        context = {
            'ariza_raqami': ariza.ariza_raqami,
            'ariza': ariza
        }
        return render(request, 'success.html', context)
    except YotoqxonaAriza.DoesNotExist:
        messages.error(request, "Ariza topilmadi")
        return redirect('dormitory:home')


def ariza_status_view(request):
    """Ariza holatini tekshirish"""
    if request.method == 'POST':
        ariza_raqami = request.POST.get('ariza_raqami')
        telefon = request.POST.get('telefon')
        
        try:
            ariza = YotoqxonaAriza.objects.get(
                ariza_raqami=ariza_raqami,
                telefon=telefon
            )
            
            context = {
                'ariza': ariza,
                'found': True
            }
            
        except YotoqxonaAriza.DoesNotExist:
            messages.error(
                request,
                "Ariza topilmadi. Iltimos, ma'lumotlarni tekshirib qaytadan kiriting."
            )
            context = {'found': False}
    else:
        context = {'found': None}
    
    return render(request, 'status.html', context)


def info_view(request):
    """Ma'lumot sahifasi"""
    return render(request, 'info.html')