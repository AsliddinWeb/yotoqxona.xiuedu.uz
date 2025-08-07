from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Q, Sum
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .models import (
    Fakultet, Kurs, Viloyat, YotoqxonaBino, 
    Xona, YotoqxonaAriza, ArizaIzohi
)


# Admin panel sarlavhalari
admin.site.site_header = "🏢 Talabalar Yotoqxonasi - Boshqaruv Paneli"
admin.site.site_title = "Yotoqxona Admin"
admin.site.index_title = "Boshqaruv Paneli"


# ================== FAKULTET ==================
@admin.register(Fakultet)
class FakultetAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'qisqartma', 'arizalar_soni_display', 'yaratilgan_sana']
    search_fields = ['nomi', 'qisqartma']
    list_filter = ['yaratilgan_sana']
    ordering = ['nomi']
    
    def arizalar_soni_display(self, obj):
        count = obj.arizalar.count()
        if count > 0:
            return format_html(
                '<span style="background: #3498db; color: white; padding: 3px 10px; border-radius: 15px;">{}</span>',
                count
            )
        return format_html('<span style="color: gray;">0</span>')
    arizalar_soni_display.short_description = "Arizalar soni"


# ================== KURS ==================
@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ['raqam', 'talabalar_soni']
    ordering = ['raqam']
    
    def talabalar_soni(self, obj):
        count = YotoqxonaAriza.objects.filter(kurs=obj).count()
        return format_html(
            '<span style="font-weight: bold; color: #27ae60;">{}</span>',
            count
        )
    talabalar_soni.short_description = "Arizalar"


# ================== VILOYAT ==================
@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'talabalar_soni']
    search_fields = ['nomi']
    ordering = ['nomi']
    
    def talabalar_soni(self, obj):
        count = YotoqxonaAriza.objects.filter(viloyat=obj).count()
        return count
    talabalar_soni.short_description = "Talabalar"


# ================== YOTOQXONA BINO ==================
@admin.register(YotoqxonaBino)
class YotoqxonaBinoAdmin(admin.ModelAdmin):
    list_display = [
        'raqam', 'nomi', 'turi_rangli', 'qavatlar_soni', 
        'xonalar_holati', 'qulayliklar', 'faol_holat'
    ]
    list_filter = ['turi', 'faol', 'wifi', 'oshxona', 'kir_yuvish', 'issiq_suv']
    search_fields = ['nomi', 'manzil']
    ordering = ['raqam']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('raqam', 'nomi', 'turi', 'faol')
        }),
        ('Manzil va tuzilma', {
            'fields': ('manzil', 'qavatlar_soni', 'har_qavatda_xonalar')
        }),
        ('Qulayliklar', {
            'fields': ('wifi', 'oshxona', 'kir_yuvish', 'issiq_suv'),
            'classes': ('collapse',)
        }),
    )
    
    def turi_rangli(self, obj):
        if obj.turi == 'erkak':
            return format_html(
                '<span style="background: #3498db; color: white; padding: 5px 10px; border-radius: 5px;">🚹 Erkaklar</span>'
            )
        return format_html(
            '<span style="background: #e91e63; color: white; padding: 5px 10px; border-radius: 5px;">🚺 Ayollar</span>'
        )
    turi_rangli.short_description = "Turi"
    
    def xonalar_holati(self, obj):
        total = obj.umumiy_xonalar
        band = obj.band_xonalar
        bosh = obj.bosh_xonalar
        
        return format_html(
            '<div style="display: flex; gap: 10px;">'
            '<span style="background: #27ae60; color: white; padding: 3px 8px; border-radius: 3px;">Bo\'sh: {}</span>'
            '<span style="background: #f39c12; color: white; padding: 3px 8px; border-radius: 3px;">Band: {}</span>'
            '<span style="background: #95a5a6; color: white; padding: 3px 8px; border-radius: 3px;">Jami: {}</span>'
            '</div>',
            bosh, band, total
        )
    xonalar_holati.short_description = "Xonalar"
    
    def qulayliklar(self, obj):
        icons = []
        if obj.wifi:
            icons.append('📶')
        if obj.oshxona:
            icons.append('🍳')
        if obj.kir_yuvish:
            icons.append('🧺')
        if obj.issiq_suv:
            icons.append('🚿')
        return ' '.join(icons) if icons else '❌'
    qulayliklar.short_description = "Qulayliklar"
    
    def faol_holat(self, obj):
        if obj.faol:
            return format_html('<span style="color: green; font-size: 20px;">✅</span>')
        return format_html('<span style="color: red; font-size: 20px;">❌</span>')
    faol_holat.short_description = "Faol"


# ================== XONA ==================
@admin.register(Xona)
class XonaAdmin(admin.ModelAdmin):
    list_display = [
        'xona_raqami', 'bino', 'qavat', 'sig_imi_display', 
        'bandlik_holati', 'qulayliklar_display', 'narxi_display'
    ]
    list_filter = ['bino', 'qavat', 'sig_imi', 'konditsioner', 'muzlatgich']
    search_fields = ['raqam', 'bino__nomi']
    ordering = ['bino', 'qavat', 'raqam']
    list_per_page = 50
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('bino', 'raqam', 'qavat', 'sig_imi')
        }),
        ('Bandlik', {
            'fields': ('band_orinlar',)
        }),
        ('Qulayliklar va narx', {
            'fields': ('konditsioner', 'muzlatgich', 'narxi')
        }),
    )
    
    def xona_raqami(self, obj):
        return format_html(
            '<span style="font-weight: bold; font-size: 14px;">{}</span>',
            obj.raqam
        )
    xona_raqami.short_description = "Xona"
    
    def sig_imi_display(self, obj):
        return f"{obj.sig_imi} kishilik"
    sig_imi_display.short_description = "Sig'imi"
    
    def bandlik_holati(self, obj):
        bosh = obj.bosh_orinlar
        band = obj.band_orinlar
        
        # Progress bar
        if obj.sig_imi > 0:
            foiz = (band / obj.sig_imi) * 100
        else:
            foiz = 0
        
        if foiz == 0:
            color = '#27ae60'  # Yashil
            status = 'Bo\'sh'
        elif foiz < 100:
            color = '#f39c12'  # Sariq
            status = f'{band}/{obj.sig_imi}'
        else:
            color = '#e74c3c'  # Qizil
            status = 'To\'liq'
        
        return format_html(
            '<div style="width: 100px; background: #ecf0f1; border-radius: 10px; overflow: hidden;">'
            '<div style="background: {}; width: {}%; padding: 3px; text-align: center; color: white;">{}</div>'
            '</div>',
            color, foiz if foiz > 0 else 100, status
        )
    bandlik_holati.short_description = "Bandlik"
    
    def qulayliklar_display(self, obj):
        icons = []
        if obj.konditsioner:
            icons.append('❄️')
        if obj.muzlatgich:
            icons.append('🧊')
        return ' '.join(icons) if icons else '-'
    qulayliklar_display.short_description = "Qulaylik"
    
    def narxi_display(self, obj):
        if obj.narxi:
            return format_html(
                '<span style="font-weight: bold; color: #2c3e50;">{:,.0f} so\'m</span>',
                obj.narxi
            )
        return '-'
    narxi_display.short_description = "Narx"
    
    actions = ['xonalarni_tozalash']
    
    def xonalarni_tozalash(self, request, queryset):
        queryset.update(band_orinlar=0)
        self.message_user(request, f"{queryset.count()} ta xona tozalandi.", messages.SUCCESS)
    xonalarni_tozalash.short_description = "Tanlangan xonalarni bo'shatish"


# ================== ARIZA IZOHI (Inline) ==================
class ArizaIzohiInline(admin.TabularInline):
    model = ArizaIzohi
    extra = 1
    fields = ['matn', 'sana']
    readonly_fields = ['sana']
    can_delete = False


# ================== YOTOQXONA ARIZA ==================
@admin.register(YotoqxonaAriza)
class YotoqxonaArizaAdmin(admin.ModelAdmin):
    list_display = [
        'ariza_raqami_display', 'fish_display', 'fakultet', 'kurs',
        'jinsi_display', 'viloyat', 'telefon_display', 
        'imtiyoz_display', 'holat_display', 'ariza_sanasi_display'
    ]
    
    list_filter = [
        'holat', 'jinsi', 'fakultet', 'kurs', 'viloyat', 
        'imtiyoz_turi', 'ariza_sanasi', 'xona_turi_afzallik'
    ]
    
    search_fields = ['ariza_raqami', 'fish', 'telefon', 'pasport']
    ordering = ['-ariza_sanasi']
    date_hierarchy = 'ariza_sanasi'
    list_per_page = 25
    
    readonly_fields = [
        'ariza_raqami', 'ariza_sanasi', 'oquv_yili', 
        'tasdiqlangan_sana', 'yoshi'
    ]
    
    fieldsets = (
        ('📋 Ariza ma\'lumotlari', {
            'fields': ('ariza_raqami', 'ariza_sanasi', 'oquv_yili', 'holat')
        }),
        ('👤 Shaxsiy ma\'lumotlar', {
            'fields': ('fish', 'jinsi', 'tugilgan_sana', 'yoshi', 'pasport')
        }),
        ('📞 Kontakt', {
            'fields': ('telefon', 'telefon_qoshimcha')
        }),
        ('📍 Manzil', {
            'fields': ('viloyat', 'tuman', 'manzil')
        }),
        ('🎓 Ta\'lim', {
            'fields': ('fakultet', 'kurs')
        }),
        ('👨‍👩‍👧‍👦 Oila', {
            'fields': ('oila_azolari',)
        }),
        ('🎖️ Imtiyozlar', {
            'fields': ('imtiyoz_turi', 'imtiyoz_hujjat')
        }),
        ('🏠 Xona afzalligi', {
            'fields': ('xona_turi_afzallik',)
        }),
        ('📝 Qaror', {
            'fields': ('tayinlangan_xona', 'tasdiqlangan_sana', 'rad_sababi', 'izoh'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ArizaIzohiInline]
    
    def ariza_raqami_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #2c3e50;">#{}</span>',
            obj.ariza_raqami
        )
    ariza_raqami_display.short_description = "Ariza №"
    
    def fish_display(self, obj):
        return format_html(
            '<div>'
            '<div style="font-weight: bold;">{}</div>'
            '<div style="font-size: 11px; color: gray;">{} yosh</div>'
            '</div>',
            obj.fish, obj.yoshi
        )
    fish_display.short_description = "F.I.SH"
    
    def jinsi_display(self, obj):
        if obj.jinsi == 'erkak':
            return format_html('<span style="color: #3498db;">👨 Erkak</span>')
        return format_html('<span style="color: #e91e63;">👩 Ayol</span>')
    jinsi_display.short_description = "Jinsi"
    
    def telefon_display(self, obj):
        return format_html(
            '<a href="tel:{}" style="text-decoration: none;">{}</a>',
            obj.telefon, obj.telefon
        )
    telefon_display.short_description = "Telefon"
    
    def imtiyoz_display(self, obj):
        if obj.imtiyoz_turi == 'yoq':
            return format_html('<span style="color: gray;">-</span>')
        
        colors = {
            '1_guruh_nogironlik': '#e74c3c',
            '2_guruh_nogironlik': '#e67e22',
            '3_guruh_nogironlik': '#f39c12',
            'yetim': '#9b59b6',
            'bir_ota_ona': '#3498db',
            'kam_taminlangan': '#1abc9c',
            'kop_bolali': '#2ecc71',
            'temir_daftar': '#34495e',
            'ayollar_daftari': '#e91e63',
            'yoshlar_daftari': '#00bcd4',
        }
        
        color = colors.get(obj.imtiyoz_turi, '#95a5a6')
        label = obj.get_imtiyoz_turi_display()
        
        if obj.imtiyoz_hujjat:
            return format_html(
                '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px;">📎 {}</span>',
                color, label
            )
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, label
        )
    imtiyoz_display.short_description = "Imtiyoz"
    
    def holat_display(self, obj):
        colors = {
            'yangi': '#3498db',
            'korilmoqda': '#f39c12',
            'imtixon': '#9b59b6',
            'tasdiqlandi': '#27ae60',
            'rad_etildi': '#e74c3c',
            'bekor': '#95a5a6',
        }
        
        icons = {
            'yangi': '📝',
            'korilmoqda': '👀',
            'imtixon': '📋',
            'tasdiqlandi': '✅',
            'rad_etildi': '❌',
            'bekor': '🚫',
        }
        
        color = colors.get(obj.holat, '#95a5a6')
        icon = icons.get(obj.holat, '')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 5px;">'
            '{} {}</span>',
            color, icon, obj.get_holat_display()
        )
    holat_display.short_description = "Holat"
    
    def ariza_sanasi_display(self, obj):
        return obj.ariza_sanasi.strftime("%d.%m.%Y %H:%M")
    ariza_sanasi_display.short_description = "Sana"
    
    # Actions
    actions = [
        'korib_chiqishga_olish',
        'tasdiqlash',
        'rad_etish',
        'export_csv',
        'statistika_korish'
    ]
    
    def korib_chiqishga_olish(self, request, queryset):
        updated = queryset.filter(holat='yangi').update(holat='korilmoqda')
        self.message_user(
            request, 
            f"{updated} ta ariza ko'rib chiqishga olindi.",
            messages.SUCCESS
        )
    korib_chiqishga_olish.short_description = "🔍 Ko'rib chiqishga olish"
    
    def tasdiqlash(self, request, queryset):
        for ariza in queryset.filter(holat__in=['korilmoqda', 'imtixon']):
            # Xona topish kerak
            if not ariza.tayinlangan_xona:
                self.message_user(
                    request,
                    f"❗ {ariza.fish} uchun xona tanlanmagan!",
                    messages.WARNING
                )
                continue
            
            ariza.holat = 'tasdiqlandi'
            ariza.tasdiqlangan_sana = timezone.now()
            ariza.save()
        
        self.message_user(request, "✅ Arizalar tasdiqlandi!", messages.SUCCESS)
    tasdiqlash.short_description = "✅ Tasdiqlash"
    
    def rad_etish(self, request, queryset):
        queryset.update(holat='rad_etildi')
        self.message_user(request, "❌ Arizalar rad etildi!", messages.WARNING)
    rad_etish.short_description = "❌ Rad etish"
    
    def export_csv(self, request, queryset):
        """CSV export"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="arizalar.csv"'
        response.write('\ufeff'.encode('utf8'))  # UTF-8 BOM
        
        writer = csv.writer(response)
        writer.writerow([
            'Ariza №', 'F.I.SH', 'Jinsi', 'Yoshi', 'Telefon',
            'Viloyat', 'Fakultet', 'Kurs', 'Imtiyoz', 'Holat', 'Sana'
        ])
        
        for ariza in queryset:
            writer.writerow([
                ariza.ariza_raqami,
                ariza.fish,
                ariza.get_jinsi_display(),
                ariza.yoshi,
                ariza.telefon,
                ariza.viloyat.nomi,
                ariza.fakultet.nomi,
                ariza.kurs.raqam,
                ariza.get_imtiyoz_turi_display(),
                ariza.get_holat_display(),
                ariza.ariza_sanasi.strftime("%d.%m.%Y")
            ])
        
        return response
    export_csv.short_description = "📥 CSV yuklash"
    
    def statistika_korish(self, request, queryset):
        """Statistika sahifasi"""
        stats = {
            'jami': queryset.count(),
            'erkak': queryset.filter(jinsi='erkak').count(),
            'ayol': queryset.filter(jinsi='ayol').count(),
            'imtiyozli': queryset.exclude(imtiyoz_turi='yoq').count(),
            'fakultetlar': {},
            'holatlar': {}
        }
        
        for fak in Fakultet.objects.all():
            stats['fakultetlar'][fak.nomi] = queryset.filter(fakultet=fak).count()
        
        for holat, label in YotoqxonaAriza.HOLAT_TANLOV:
            stats['holatlar'][label] = queryset.filter(holat=holat).count()
        
        self.message_user(
            request,
            f"📊 Statistika: Jami {stats['jami']} ta ariza | "
            f"Erkak: {stats['erkak']} | Ayol: {stats['ayol']} | "
            f"Imtiyozli: {stats['imtiyozli']}",
            messages.INFO
        )
    statistika_korish.short_description = "📊 Statistika"
    
    # Custom admin views
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='dormitory_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Dashboard sahifasi"""
        context = {
            'title': 'Yotoqxona Dashboard',
            'jami_arizalar': YotoqxonaAriza.objects.count(),
            'yangi': YotoqxonaAriza.objects.filter(holat='yangi').count(),
            'tasdiqlangan': YotoqxonaAriza.objects.filter(holat='tasdiqlandi').count(),
            'rad_etilgan': YotoqxonaAriza.objects.filter(holat='rad_etildi').count(),
        }
        return render(request, 'admin/dormitory/dashboard.html', context)
