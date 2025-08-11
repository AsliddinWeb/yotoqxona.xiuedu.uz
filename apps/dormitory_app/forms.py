from django import forms
from django.core.validators import RegexValidator
from .models import YotoqxonaAriza, Fakultet, Kurs, Viloyat, Xona
from datetime import date


class YotoqxonaArizaForm(forms.ModelForm):
    """Yotoqxona ariza formasi - yangi talabalar uchun"""
    
    # Telefon validatori
    telefon_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam formati: +998901234567"
    )
    
    # Pasport validatori
    pasport_regex = RegexValidator(
        regex=r'^[A-Z]{2}\d{7}$',
        message="Pasport formati: AA1234567 (2 ta harf, 7 ta raqam)"
    )
    
    class Meta:
        model = YotoqxonaAriza
        fields = [
            'fish', 'jinsi', 'tugilgan_sana', 'pasport',
            'telefon', 'telefon_qoshimcha',
            'viloyat', 'tuman', 'manzil',
            'fakultet', 'kurs',
            'oila_azolari',
            'imtiyoz_turi', 'imtiyoz_hujjat',
        ]
        
        widgets = {
            # Shaxsiy ma'lumotlar
            'fish': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200',
                'placeholder': 'Masalan: Abdullayev Jasur Karimovich',
                'required': True
            }),
            
            'jinsi': forms.RadioSelect(attrs={
                'class': 'flex gap-6'
            }),
            
            'tugilgan_sana': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date',
                'max': date.today().strftime('%Y-%m-%d'),
                'min': '1990-01-01'
            }),
            
            'pasport': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent uppercase',
                'placeholder': 'AA1234567',
                'pattern': '[A-Z]{2}[0-9]{7}',
                'maxlength': '9',
                'style': 'text-transform: uppercase;'
            }),
            
            # Kontakt
            'telefon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '+998901234567',
                'pattern': r'\+998[0-9]{9}',
                'maxlength': '13'
            }),
            
            'telefon_qoshimcha': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': "+998901234567 (Ota-ona telefoni)",
                'pattern': r'\+998[0-9]{9}',
                'maxlength': '13'
            }),
            
            # Manzil
            'viloyat': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white'
            }),
            
            'tuman': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Masalan: Chilonzor tumani'
            }),
            
            'manzil': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none',
                'rows': '3',
                'placeholder': "Ko'cha, uy, kvartira raqami"
            }),
            
            # Ta'lim
            'fakultet': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white'
            }),
            
            'kurs': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white'
            }),
            
            # Oila
            'oila_azolari': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': '1',
                'max': '20',
                'placeholder': '5'
            }),
            
            # Imtiyoz
            'imtiyoz_turi': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white',
                'id': 'imtiyoz_turi_select'
            }),
            
            'imtiyoz_hujjat': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'id': 'imtiyoz_hujjat_input'
            }),
            
        }
        
        labels = {
            'fish': 'To\'liq ism-familiya',
            'jinsi': 'Jinsingiz',
            'tugilgan_sana': 'Tug\'ilgan sana',
            'pasport': 'Pasport seriya va raqami',
            'telefon': 'Telefon raqamingiz',
            'telefon_qoshimcha': 'Ota-ona telefoni (ixtiyoriy)',
            'viloyat': 'Viloyat',
            'tuman': 'Tuman/Shahar',
            'manzil': 'To\'liq manzil',
            'fakultet': 'Fakultet',
            'kurs': 'Kurs',
            'oila_azolari': 'Oilada necha kishi yashaydi?',
            'imtiyoz_turi': 'Imtiyozingiz bormi?',
            'imtiyoz_hujjat': 'Imtiyoz hujjati (agar bo\'lsa)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Kurs default 1 (yangi talabalar uchun)
        self.fields['kurs'].initial = Kurs.objects.filter(raqam=1).first()
        
        # Required fieldlar
        self.fields['fish'].required = True
        self.fields['jinsi'].required = True
        self.fields['tugilgan_sana'].required = True
        self.fields['pasport'].required = True
        self.fields['telefon'].required = True
        self.fields['viloyat'].required = True
        self.fields['tuman'].required = True
        self.fields['manzil'].required = True
        self.fields['fakultet'].required = True
        self.fields['oila_azolari'].required = True
        
        # Optional fieldlar
        self.fields['telefon_qoshimcha'].required = False
        self.fields['imtiyoz_hujjat'].required = False
        
        # Viloyat empty label
        self.fields['viloyat'].empty_label = "-- Viloyatni tanlang --"
        self.fields['fakultet'].empty_label = "-- Fakultetni tanlang --"
        
    def clean_fish(self):
        """FISh validatsiya - kamida 2 so'z"""
        fish = self.cleaned_data.get('fish')
        if fish:
            words = fish.strip().split()
            if len(words) < 2:
                raise forms.ValidationError("Iltimos, to'liq ism va familiyangizni kiriting")
            
            # Har bir so'z katta harf bilan boshlansin
            formatted_words = []
            for word in words:
                if word:
                    formatted_words.append(word.capitalize())
            
            return ' '.join(formatted_words)
        return fish
    
    def clean_pasport(self):
        """Pasport formati tekshirish"""
        pasport = self.cleaned_data.get('pasport')
        if pasport:
            pasport = pasport.upper()
            if len(pasport) != 9:
                raise forms.ValidationError("Pasport 9 ta belgidan iborat bo'lishi kerak")
            if not pasport[:2].isalpha():
                raise forms.ValidationError("Pasport 2 ta harf bilan boshlanishi kerak")
            if not pasport[2:].isdigit():
                raise forms.ValidationError("Pasportning oxirgi 7 belgisi raqam bo'lishi kerak")
        return pasport
    
    def clean_telefon(self):
        """Telefon formati tekshirish"""
        telefon = self.cleaned_data.get('telefon')
        if telefon:
            # Faqat raqamlar va + belgisi
            clean_tel = ''.join(filter(lambda x: x.isdigit() or x == '+', telefon))
            
            # Agar + belgisi yo'q bo'lsa qo'shish
            if not clean_tel.startswith('+'):
                clean_tel = '+' + clean_tel
            
            # Agar 998 bilan boshlanmasa qo'shish
            if not clean_tel.startswith('+998'):
                if clean_tel.startswith('+'):
                    clean_tel = '+998' + clean_tel[1:]
                else:
                    clean_tel = '+998' + clean_tel
            
            # Uzunlik tekshirish
            if len(clean_tel) != 13:
                raise forms.ValidationError("Telefon raqam formati noto'g'ri")
            
            return clean_tel
        return telefon
    
    def clean_telefon_qoshimcha(self):
        """Qo'shimcha telefon tekshirish"""
        telefon = self.cleaned_data.get('telefon_qoshimcha')
        if telefon:
            # Asosiy telefon bilan bir xil logika
            clean_tel = ''.join(filter(lambda x: x.isdigit() or x == '+', telefon))
            if clean_tel:
                if not clean_tel.startswith('+'):
                    clean_tel = '+' + clean_tel
                if not clean_tel.startswith('+998'):
                    clean_tel = '+998' + clean_tel[9:] if len(clean_tel) > 9 else '+998' + clean_tel
                
                if len(clean_tel) != 13:
                    raise forms.ValidationError("Telefon raqam formati noto'g'ri")
                
                return clean_tel
        return telefon
    
    def clean_tugilgan_sana(self):
        """Yosh tekshirish - kamida 16 yosh"""
        sana = self.cleaned_data.get('tugilgan_sana')
        if sana:
            bugun = date.today()
            yosh = bugun.year - sana.year - ((bugun.month, bugun.day) < (sana.month, sana.day))
            
            if yosh < 16:
                raise forms.ValidationError("Ariza berish uchun kamida 16 yoshda bo'lishingiz kerak")
            if yosh > 35:
                raise forms.ValidationError("Yosh chegarasi 35 yoshgacha")
        
        return sana
    
    def clean_imtiyoz_hujjat(self):
        """Imtiyoz hujjati validatsiya"""
        hujjat = self.cleaned_data.get('imtiyoz_hujjat')
        imtiyoz_turi = self.cleaned_data.get('imtiyoz_turi')
        
        if imtiyoz_turi and imtiyoz_turi != 'yoq' and not hujjat:
            raise forms.ValidationError("Imtiyoz tanlangan bo'lsa, hujjat yuklash majburiy")
        
        if hujjat:
            # Fayl hajmi tekshirish (5MB)
            if hujjat.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Fayl hajmi 5MB dan oshmasligi kerak")
            
            # Fayl formati
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            file_name = hujjat.name.lower()
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Faqat PDF, JPG, PNG formatlar qabul qilinadi")
        
        return hujjat
    
    def clean(self):
        """Umumiy validatsiya"""
        cleaned_data = super().clean()
        
        # Telefon raqamlar bir xil bo'lmasligi kerak
        tel1 = cleaned_data.get('telefon')
        tel2 = cleaned_data.get('telefon_qoshimcha')
        
        if tel1 and tel2 and tel1 == tel2:
            raise forms.ValidationError("Asosiy va qo'shimcha telefon raqamlar bir xil bo'lmasligi kerak")
        
        return cleaned_data