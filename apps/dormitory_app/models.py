from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.db.models import Sum, Count, Q
import uuid
from datetime import date


class Fakultet(models.Model):
    """Fakultet modeli"""
    nomi = models.CharField(max_length=200, verbose_name="Fakultet nomi", unique=True)
    qisqartma = models.CharField(max_length=20, verbose_name="Qisqartma", blank=True)
    tavsif = models.TextField(verbose_name="Tavsif", blank=True)
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"
        ordering = ['nomi']
    
    def __str__(self):
        return self.nomi
    
    def get_arizalar_soni(self):
        """Fakultetga berilgan arizalar soni"""
        return self.arizalar.count()


class Kurs(models.Model):
    """Kurs modeli"""
    raqam = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Kurs raqami",
        unique=True
    )
    
    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ['raqam']
    
    def __str__(self):
        return f"{self.raqam}-kurs"


class Viloyat(models.Model):
    """Viloyatlar"""
    nomi = models.CharField(max_length=100, verbose_name="Viloyat nomi", unique=True)
    
    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ['nomi']
    
    def __str__(self):
        return self.nomi


class YotoqxonaBino(models.Model):
    """Yotoqxona binosi"""
    BINO_TURI = [
        ('erkak', '🚹 Erkaklar binosi'),
        ('ayol', '🚺 Ayollar binosi'),
    ]
    
    raqam = models.IntegerField(verbose_name="Bino raqami", unique=True)
    nomi = models.CharField(max_length=100, verbose_name="Bino nomi")
    turi = models.CharField(max_length=10, choices=BINO_TURI, verbose_name="Bino turi")
    manzil = models.TextField(verbose_name="Manzil")
    qavatlar_soni = models.IntegerField(
        verbose_name="Qavatlar soni",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    har_qavatda_xonalar = models.IntegerField(verbose_name="Har qavatdagi xonalar soni")
    
    # Qulayliklar
    wifi = models.BooleanField(default=True, verbose_name="Wi-Fi")
    oshxona = models.BooleanField(default=True, verbose_name="Oshxona")
    kir_yuvish = models.BooleanField(default=True, verbose_name="Kir yuvish xonasi")
    issiq_suv = models.BooleanField(default=True, verbose_name="Issiq suv")
    
    faol = models.BooleanField(default=True, verbose_name="Faol")
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Yotoqxona binosi"
        verbose_name_plural = "Yotoqxona binolari"
        ordering = ['raqam']
    
    def __str__(self):
        return f"{self.raqam}-bino: {self.nomi}"
    
    @property
    def umumiy_xonalar(self):
        """Umumiy xonalar soni"""
        return self.qavatlar_soni * self.har_qavatda_xonalar
    
    @property
    def band_xonalar(self):
        """Band xonalar soni"""
        return self.xonalar.filter(band_orinlar__gt=0).count()
    
    @property
    def bosh_xonalar(self):
        """To'liq bo'sh xonalar soni"""
        return self.xonalar.filter(band_orinlar=0).count()


class Xona(models.Model):
    """Yotoqxona xonasi"""
    XONA_TURI = [
        (2, '2 kishilik'),
        (3, '3 kishilik'),
        (4, '4 kishilik'),
        (5, '5 kishilik'),
        (6, '6 kishilik'),
    ]
    
    bino = models.ForeignKey(YotoqxonaBino, on_delete=models.CASCADE, related_name='xonalar')
    raqam = models.CharField(max_length=10, verbose_name="Xona raqami")
    qavat = models.IntegerField(verbose_name="Qavat")
    sig_imi = models.IntegerField(choices=XONA_TURI, verbose_name="Sig'imi")
    band_orinlar = models.IntegerField(default=0, verbose_name="Band o'rinlar")
    
    # Qulayliklar
    konditsioner = models.BooleanField(default=False, verbose_name="Konditsioner")
    muzlatgich = models.BooleanField(default=False, verbose_name="Muzlatgich")
    
    narxi = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Oylik to'lov",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        unique_together = ['bino', 'raqam']
        ordering = ['bino', 'qavat', 'raqam']
    
    def __str__(self):
        return f"{self.bino.raqam}-bino, {self.raqam}-xona"
    
    @property
    def bosh_orinlar(self):
        """Bo'sh o'rinlar soni"""
        return self.sig_imi - self.band_orinlar
    
    @property
    def toliq_bandmi(self):
        """Xona to'liq bandmi"""
        return self.band_orinlar >= self.sig_imi
    
    def get_holat_rangi(self):
        """Xona holati rangi"""
        if self.band_orinlar == 0:
            return "success"  # Yashil - bo'sh
        elif self.band_orinlar < self.sig_imi:
            return "warning"  # Sariq - qisman band
        else:
            return "danger"  # Qizil - to'liq


class YotoqxonaAriza(models.Model):
    """Yotoqxona arizasi - yangi talabalar uchun"""
    HOLAT_TANLOV = [
        ('yangi', '📝 Yangi'),
        ('korilmoqda', '👀 Ko\'rib chiqilmoqda'),
        ('imtixon', '📋 Imtixon kutilmoqda'),
        ('tasdiqlandi', '✅ Tasdiqlandi'),
        ('rad_etildi', '❌ Rad etildi'),
        ('bekor', '🚫 Bekor qilindi'),
    ]
    
    JINSI = [
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    ]
    
    IMTIYOZ_TURI = [
        ('yoq', 'Imtiyoz yo\'q'),
        ('1_guruh_nogironlik', '1-guruh nogironlik'),
        ('2_guruh_nogironlik', '2-guruh nogironlik'),
        ('3_guruh_nogironlik', '3-guruh nogironlik'),
        ('yetim', 'Yetim'),
        ('bir_ota_ona', 'Bir ota-ona tarbiyasida'),
        ('kam_taminlangan', 'Kam ta\'minlangan oila'),
        ('kop_bolali', 'Ko\'p bolali oila (4+ farzand)'),
        ('temir_daftar', 'Temir daftar'),
        ('ayollar_daftari', 'Ayollar daftari'),
        ('yoshlar_daftari', 'Yoshlar daftari'),
    ]
    
    # Ariza raqami (unique)
    ariza_raqami = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Ariza raqami",
        editable=False
    )
    
    # Shaxsiy ma'lumotlar
    fish = models.CharField(max_length=300, verbose_name="To'liq ism familiya")
    jinsi = models.CharField(max_length=10, choices=JINSI, verbose_name="Jinsi")
    tugilgan_sana = models.DateField(verbose_name="Tug'ilgan sana")
    pasport = models.CharField(
        max_length=9, 
        verbose_name="Pasport seriya raqami",
        validators=[RegexValidator(r'^[A-Z]{2}\d{7}$', 'Format: AA1234567')]
    )
    
    # Kontakt
    telefon = models.CharField(
        max_length=13,
        verbose_name="Telefon raqami",
        validators=[RegexValidator(r'^\+998\d{9}$', 'Format: +998901234567')]
    )
    telefon_qoshimcha = models.CharField(
        max_length=13,
        verbose_name="Qo'shimcha telefon (ota-ona)",
        blank=True
    )
    
    # Manzil
    viloyat = models.ForeignKey(Viloyat, on_delete=models.PROTECT, verbose_name="Viloyat")
    tuman = models.CharField(max_length=100, verbose_name="Tuman/Shahar")
    manzil = models.TextField(verbose_name="To'liq manzil")
    
    # Ta'lim ma'lumotlari
    fakultet = models.ForeignKey(
        Fakultet, 
        on_delete=models.PROTECT, 
        verbose_name="Fakultet",
        related_name='arizalar'
    )
    kurs = models.ForeignKey(
        Kurs, 
        on_delete=models.PROTECT, 
        verbose_name="Kurs",
        default=1  # Yangi talabalar uchun 1-kurs
    )
    
    # Oilaviy holat
    oila_azolari = models.IntegerField(
        verbose_name="Oila a'zolari soni",
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    
    # Imtiyozlar
    imtiyoz_turi = models.CharField(
        max_length=30,
        choices=IMTIYOZ_TURI,
        default='yoq',
        verbose_name="Imtiyoz turi"
    )
    imtiyoz_hujjat = models.FileField(
        upload_to='imtiyoz/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Imtiyoz hujjati (PDF/rasm)"
    )
    
    # Afzalliklar
    xona_turi_afzallik = models.IntegerField(
        choices=Xona.XONA_TURI,
        verbose_name="Afzal xona turi",
        null=True,
        blank=True
    )
    
    # Tizim ma'lumotlari
    ariza_sanasi = models.DateTimeField(auto_now_add=True, verbose_name="Ariza sanasi")
    oquv_yili = models.CharField(max_length=9, verbose_name="O'quv yili")
    holat = models.CharField(
        max_length=20,
        choices=HOLAT_TANLOV,
        default='yangi',
        verbose_name="Holat"
    )
    
    # Natija
    tayinlangan_xona = models.ForeignKey(
        Xona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tayinlangan xona"
    )
    tasdiqlangan_sana = models.DateTimeField(null=True, blank=True)
    rad_sababi = models.TextField(blank=True, verbose_name="Rad etish sababi")
    izoh = models.TextField(blank=True, verbose_name="Admin izohi")
    
    class Meta:
        verbose_name = "Yotoqxona arizasi"
        verbose_name_plural = "Yotoqxona arizalari"
        ordering = ['-ariza_sanasi']
        indexes = [
            models.Index(fields=['holat', 'ariza_sanasi']),
            models.Index(fields=['fakultet', 'kurs']),
        ]
    
    def __str__(self):
        return f"#{self.ariza_raqami} - {self.fish}"
    
    def save(self, *args, **kwargs):
        # Ariza raqami generatsiya
        if not self.ariza_raqami:
            yil = timezone.now().year
            self.ariza_raqami = f"YA-{yil}-{uuid.uuid4().hex[:6].upper()}"
        
        # O'quv yilini avtomatik belgilash
        if not self.oquv_yili:
            now = timezone.now()
            if now.month >= 9:
                self.oquv_yili = f"{now.year}-{now.year + 1}"
            else:
                self.oquv_yili = f"{now.year - 1}-{now.year}"
        
        # Agar tasdiqlansa
        if self.holat == 'tasdiqlandi' and self.tayinlangan_xona:
            self.tasdiqlangan_sana = timezone.now()
            # Xona bandligini oshirish
            if self.tayinlangan_xona.band_orinlar < self.tayinlangan_xona.sig_imi:
                self.tayinlangan_xona.band_orinlar += 1
                self.tayinlangan_xona.save()
        
        super().save(*args, **kwargs)
    

    @property
    def yoshi(self):
        """Talabaning yoshi"""
        today = date.today()
        return today.year - self.tugilgan_sana.year - (
            (today.month, today.day) < (self.tugilgan_sana.month, self.tugilgan_sana.day)
        )
    
    @property
    def imtiyozli(self):
        """Imtiyozli talabami"""
        return self.imtiyoz_turi != 'yoq'


class ArizaIzohi(models.Model):
    """Ariza uchun admin izohlari"""
    ariza = models.ForeignKey(YotoqxonaAriza, on_delete=models.CASCADE, related_name='izohlar')
    matn = models.TextField(verbose_name="Izoh matni")
    sana = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ariza izohi"
        verbose_name_plural = "Ariza izohlari"
        ordering = ['-sana']
    
    def __str__(self):
        return f"{self.ariza.ariza_raqami} - izoh"
