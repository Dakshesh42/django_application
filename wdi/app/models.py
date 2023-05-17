from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import Sum
from datetime import timedelta
# Create your models here.
#Custom User Manager:

COUNTRIES = (
    ('AF', 'Afghanistan'),
    ('AX', 'Åland Islands'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia (Plurinational State of)'),
    ('BQ', 'Bonaire, Sint Eustatius and Saba'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CV', 'Cabo Verde'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo (Democratic Republic of the)'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Côte d\'Ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CW', 'Curaçao'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
	('GA', 'Gabon'),
	('GM', 'Gambia'),
	('GE', 'Georgia'),
	('DE', 'Germany'),
	('GH', 'Ghana'),
	('GR', 'Greece'),
	('GL', 'Greenland'),
	('GD', 'Grenada'),
	('GT', 'Guatemala'),
	('GN', 'Guinea'),
	('GW', 'Guinea-Bissau'),
	('GY', 'Guyana'),
	('HT', 'Haiti'),
	('HN', 'Honduras'),
	('HU', 'Hungary'),
	('IS', 'Iceland'),
	('IN', 'India'),
	('ID', 'Indonesia'),
	('IR', 'Iran'),
	('IQ', 'Iraq'),
	('IE', 'Ireland'),
	('IL', 'Israel'),
	('IT', 'Italy'),
	('CI', 'Ivory Coast'),
	('JM', 'Jamaica'),
	('JP', 'Japan'),
	('JO', 'Jordan'),
	('KZ', 'Kazakhstan'),
	('KE', 'Kenya'),
	('KI', 'Kiribati'),
	('KW', 'Kuwait'),
	('KG', 'Kyrgyzstan'),
	('LA', 'Laos'),
	('LV', 'Latvia'),
	('LB', 'Lebanon'),
	('LS', 'Lesotho'),
	('LR', 'Liberia'),
	('LY', 'Libya'),
	('LI', 'Liechtenstein'),
	('LT', 'Lithuania'),
	('LU', 'Luxembourg'),
	('MG', 'Madagascar'),
	('MW', 'Malawi'),
	('MY', 'Malaysia'),
	('MV', 'Maldives'),
	('ML', 'Mali'),
	('MT', 'Malta'),
	('MH', 'Marshall Islands'),
	('MR', 'Mauritania'),
	('MU', 'Mauritius'),
	('MX', 'Mexico'),
	('FM', 'Micronesia'),
	('MD', 'Moldova'),
	('MC', 'Monaco'),
	('MN', 'Mongolia'),
	('ME', 'Montenegro'),
	('MA', 'Morocco'),
	('MZ', 'Mozambique'),
	('MM', 'Myanmar'),
	('NA', 'Namibia'),
	('NR', 'Nauru'),
	('NP', 'Nepal'),
	('NL', 'Netherlands'),
	('NZ', 'New Zealand'),
	('NI', 'Nicaragua'),
	('NE', 'Niger'),
	('NG', 'Nigeria'),
	('KP', 'North Korea'),
	('MK', 'North Macedonia'),
	('NO', 'Norway'),
	('OM', 'Oman'),
	('PK', 'Pakistan'),
	('PW', 'Palau'),
	('PA', 'Panama'),
	('PG', 'Papua New Guinea'),
	('PY', 'Paraguay'),
	('PE', 'Peru'),
	('PH', 'Philippines'),
	('PL', 'Poland'),
	('PT', 'Portugal'),
	('QA', 'Qatar'),
	('RO', 'Romania'),
	('RU', 'Russia'),
	('RW', 'Rwanda'),
	('KN', 'Saint Kitts and Nevis'),
	('LC', 'Saint Lucia'),
	('VC', 'Saint Vincent and the Grenadines'),
	('WS', 'Samoa'),
	('SM', 'San Marino'),
	('ST', 'Sao Tome and Principe'),
	('SA', 'Saudi Arabia'),
	('SN', 'Senegal'),
	('RS', 'Serbia'),
	('SC', 'Seychelles'),
	('SL', 'Sierra Leone'),
	('SG', 'Singapore'),
	('SK', 'Slovakia'),
	('SI', 'Slovenia'),
	('SB', 'Solomon Islands'),
	('SO', 'Somalia'),
	('ZA', 'South Africa'),
	('GS', 'South Georgia and the South Sandwich Islands'),
	('SS', 'South Sudan'),
	('ES', 'Spain'),
	('LK', 'Sri Lanka'),
	('SD', 'Sudan'),
	('SR', 'Suriname'),
	('SJ', 'Svalbard and Jan Mayen'),
	('SE', 'Sweden'),
	('CH', 'Switzerland'),
	('SY', 'Syrian Arab Republic'),
	('TW', 'Taiwan, Province of China'),
	('TJ', 'Tajikistan'),
	('TZ', 'Tanzania, United Republic of'),
	('TH', 'Thailand'),
	('TL', 'Timor-Leste'),
	('TG', 'Togo'),
	('TK', 'Tokelau'),
	('TO', 'Tonga'),
	('TT', 'Trinidad and Tobago'),
	('TN', 'Tunisia'),
	('TR', 'Turkey'),
	('TM', 'Turkmenistan'),
	('TC', 'Turks and Caicos Islands'),
	('TV', 'Tuvalu'),
	('UG', 'Uganda'),
	('UA', 'Ukraine'),
	('AE', 'United Arab Emirates'),
	('GB', 'United Kingdom'),
	('US', 'United States'),
	('UM', 'United States Minor Outlying Islands'),
	('UY', 'Uruguay'),
	('UZ', 'Uzbekistan'),
	('VU', 'Vanuatu'),
	('VE', 'Venezuela, Bolivarian Republic of'),
	('VN', 'Viet Nam'),
	('VG', 'Virgin Islands, British'),
	('VI', 'Virgin Islands, U.S.'),
	('WF', 'Wallis and Futuna'),
	('EH', 'Western Sahara'),
	('YE', 'Yemen'),
	('ZM', 'Zambia'),
	('ZW', 'Zimbabwe'),
)

CURRENCY = (
    ("AFN", "Afghani"),
	("DZD", "Algerian Dinar"),
	("ARS", "Argentine Peso"),
	("AMD", "Armenian Dram"),
	("AWG", "Aruban Guilder"),
	("AUD", "Australian Dollar"),
	("AZN", "Azerbaijanian Manat"),
	("BSD", "Bahamian Dollar"),
	("BHD", "Bahraini Dinar"),
	("THB", "Baht"),
	("PAB", "Balboa"),
	("BBD", "Barbados Dollar"),
	("BYR", "Belarussian Ruble"),
	("BZD", "Belize Dollar"),
	("BMD", "Bermudian Dollar"),
	("VEF", "Bolivar Fuerte"),
	("BOB", "Boliviano"),
	("BRL", "Brazilian Real"),
	("BND", "Brunei Dollar"),
	("BGN", "Bulgarian Lev"),
	("BIF", "Burundi Franc"),
	("CAD", "Canadian Dollar"),
	("CVE", "Cape Verde Escudo"),
	("KYD", "Cayman Islands Dollar"),
	("GHS", "Cedi"),
	("CLP", "Chilean Peso"),
	("COP", "Colombian Peso"),
	("KMF", "Comoro Franc"),
	("CDF", "Congolese Franc"),
	("BAM", "Convertible Mark"),
	("NIO", "Cordoba Oro"),
	("CRC", "Costa Rican Colon"),
	("HRK", "Croatian Kuna"),
	("CUP", "Cuban Peso"),
	("CZK", "Czech Koruna"),
	("GMD", "Dalasi"),
	("DKK", "Danish Krone"),
	("MKD", "Denar"),
	("DJF", "Djibouti Franc"),
	("STD", "Dobra"),
	("DOP", "Dominican Peso"),
	("VND", "Dong"),
	("XCD", "East Caribbean Dollar"),
	("EGP", "Egyptian Pound"),
	("SVC", "El Salvador Colon"),
	("ETB", "Ethiopian Birr"),
	("EUR", "Euro"),
	("FKP", "Falkland Islands Pound"),
	("FJD", "Fiji Dollar"),
	("HUF", "Forint"),
	("GIP", "Gibraltar Pound"),
	("XAU", "Gold"),
	("HTG", "Gourde"),
	("PYG", "Guarani"),
	("GNF", "Guinea Franc"),
	("GYD", "Guyana Dollar"),
	("HKD", "Hong Kong Dollar"),
	("UAH", "Hryvnia"),
	("ISK", "Iceland Krona"),
	("INR", "Indian Rupee"),
	("IRR", "Iranian Rial"),
	("IQD", "Iraqi Dinar"),
	("JMD", "Jamaican Dollar"),
	("JOD", "Jordanian Dinar"),
	("KES", "Kenyan Shilling"),
	("PGK", "Kina"),
	("LAK", "Kip"),
	("KWD", "Kuwaiti Dinar"),
	("MWK", "Kwacha"),
	("AOA", "Kwanza"),
	("MMK", "Kyat"),
	("GEL", "Lari"),
	("LVL", "Latvian Lats"),
	("LBP", "Lebanese Pound"),
	("ALL", "Lek"),
	("HNL", "Lempira"),
	("SLL", "Leone"),
	("RON", "Leu"),
	("LRD", "Liberian Dollar"),
	("LYD", "Libyan Dinar"),
	("SZL", "Lilangeni"),
	("LTL", "Lithuanian Litas"),
	("LSL", "Loti"),
	("MGA", "Malagasy Ariary"),
	("MYR", "Malaysian Ringgit"),
	("MUR", "Mauritius Rupee"),
	("MZN", "Metical"),
	("MXN", "Mexican Peso"),
	("MDL", "Moldovan Leu"),
	("MAD", "Moroccan Dirham"),
	("BOV", "Mvdol"),
	("NGN", "Naira"),
	("ERN", "Nakfa"),
	("NAD", "Namibia Dollar"),
	("NPR", "Nepalese Rupee"),
	("ANG", "Netherlands Antillean Guilder"),
	("ILS", "New Israeli Sheqel"),
	("TMT", "New Manat"),
	("TWD", "New Taiwan Dollar"),
	("NZD", "New Zealand Dollar"),
	("BTN", "Ngultrum"),
	("KPW", "North Korean Won"),
	("NOK", "Norwegian Krone"),
	("PEN", "Nuevo Sol"),
	("MRO", "Ouguiya"),
	("PKR", "Pakistan Rupee"),
	("XPD", "Palladium"),
	("MOP", "Pataca"),
	("TOP", "Pa’anga"),
	("CUC", "Peso Convertible"),
	("UYU", "Peso Uruguayo"),
	("PHP", "Philippine Peso"),
	("XPT", "Platinum"),
	("GBP", "Pound Sterling"),
	("BWP", "Pula"),
	("QAR", "Qatari Rial"),
	("GTQ", "Quetzal"),
	("ZAR", "Rand"),
	("OMR", "Rial Omani"),
	("KHR", "Riel"),
	("MVR", "Rufiyaa"),
	("IDR", "Rupiah"),
	("RUB", "Russian Ruble"),
	("RWF", "Rwanda Franc"),
	("SHP", "Saint Helena Pound"),
	("SAR", "Saudi Riyal"),
	("RSD", "Serbian Dinar"),
	("SCR", "Seychelles Rupee"),
	("XAG", "Silver"),
	("SGD", "Singapore Dollar"),
	("SBD", "Solomon Islands Dollar"),
	("KGS", "Som"),
	("SOS", "Somali Shilling"),
	("TJS", "Somoni"),
	("ZAR", "South African Rand"),
	("LKR", "Sri Lanka Rupee"),
	("XSU", "Sucre"),
	("SDG", "Sudanese Pound"),
	("SRD", "Surinam Dollar"),
	("SEK", "Swedish Krona"),
	("CHF", "Swiss Franc"),
	("SYP", "Syrian Pound"),
	("BDT", "Taka"),
	("WST", "Tala"),
	("TZS", "Tanzanian Shilling"),
	("KZT", "Tenge"),
	("TTD", "Trinidad and Tobago Dollar"),
	("MNT", "Tugrik"),
	("TND", "Tunisian Dinar"),
	("TRY", "Turkish Lira"),
	("AED", "UAE Dirham"),
	("USD", "US Dollar"),
	("UGX", "Uganda Shilling"),
	("COU", "Unidad de Valor Real"),
	("CLF", "Unidades de fomento"),
	("UYI", "Uruguay Peso en Unidades Indexadas (URUIURUI)"),
	("UZS", "Uzbekistan Sum"),
	("VUV", "Vatu"),
	("KRW", "Won"),
	("YER", "Yemeni Rial"),
	("JPY", "Yen"),
	("CNY", "Yuan Renminbi"),
	("ZMK", "Zambian Kwacha"),
	("ZWL", "Zimbabwe Dollar"),
	("PLN", "Zloty"),
)


TAGS = (
    ("CM", "Completed"),
    ("IP", "In-Progress"),
    )


TASK_TAGS = (
	("Frontend", "Frontend"),
    ("UI", "UI"),
    ("UX", "UX"),
    ("Coding", "Coding"),
    ("Testing", "Testing"),
    ("Debug", "Debug"),
    ("Database", "Database"),
    ("Deployment", "Deployment"),
    ("Content-Writing", "Content-Writing"),
    ("SEO Services", "SEO Services"),
    ("R&D", "R&D"),
    ("Other", "Other"),
)


PRO_TYPE = (
    ("P1", "TYPE-1"),
    ("P2", "TYPE-2"),
    ("P3", "TYPE-3"),
    ("P4", "TYPE-4"),
    ("P5", "TYPE-5"),
)


GEN = (
    ("M", "Male"),
    ("F", "Female"),
    )


class EmployeeManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender, phone, date_of_birth, joining_date, qualification, designation, address, ctc, hr, acc, resume, picture, edu_docs, aadhar, pan, certificate, additional_certificate, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, phone, designation, company, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            date_of_birth=date_of_birth,
            joining_date=joining_date,
            qualification=qualification,
            designation=designation,
            address=address,
			ctc=ctc,
            hr=hr,
            acc=acc,
			resume=resume, 
			picture=picture,
			edu_docs=edu_docs, 
			aadhar=aadhar, 
			pan=pan,
			certificate=certificate,
			additional_certificate=additional_certificate,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, gender, phone, date_of_birth, joining_date, qualification, designation, address, ctc, hr, acc, resume, picture, edu_docs, aadhar, pan, certificate, additional_certificate, password=None):
        """
        Creates and saves a superuser with the given email, name, phone, designation, company, and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            date_of_birth=date_of_birth,
            joining_date=joining_date,
            qualification=qualification,
            designation=designation,
            address=address,
			ctc=ctc,
            hr=hr,
            acc=acc,
			resume=resume, 
			picture=picture,
			edu_docs=edu_docs, 
			aadhar=aadhar,
			pan=pan, 
			certificate=certificate,
			additional_certificate=additional_certificate,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#Custome User model:
class Employee(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True,)
    emp_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1,choices=GEN)
    phone = PhoneNumberField()
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    address = models.TextField(max_length=350)
    ctc = models.PositiveIntegerField()
    resume = models.FileField(upload_to='media/resume',blank=True,null=True)
    picture = models.FileField(upload_to='media/picture',blank=True,null=True)
    edu_docs = models.FileField(upload_to='media/edu_docs',blank=True,null=True)
    aadhar = models.FileField(upload_to='media/aadhar',blank=True,null=True)
    pan = models.FileField(upload_to='media/pan',blank=True,null=True)
    certificate = models.FileField(upload_to='media/certificate',blank=True,null=True)
    additional_certificate = models.FileField(upload_to='media/additional_certificate',blank=True,null=True)
    hr = models.BooleanField(null=True,blank=True)
    acc = models.BooleanField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone','designation','gender', 'date_of_birth', 'joining_date', 'qualification', 'address', 'picture', 'ctc','hr', 'acc', 'resume', 'edu_docs', 'aadhar', 'pan','certificate','additional_certificate']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Client(models.Model):
    client_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    contact_number = models.PositiveIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country =  models.CharField(max_length=2,choices=COUNTRIES)
    billing_name = models.CharField(max_length=100)
    pan_number = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=100)
    client_doc = models.FileField(upload_to='media/client',blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.client_name



class ClientContact(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	designation = models.CharField(max_length=50)
	gender = models.CharField(max_length=1,choices=GEN)
	company_email = models.EmailField()
	personal_email = models.EmailField()
	phone = models.PositiveIntegerField()
	skype_id = models.CharField(max_length=50)
	whatsapp = models.PositiveIntegerField()
    
	def __str__(self):
             return self.first_name


TYP = (
    ("SDP", "Software Development"),
    ("SEO", "Search Engine Optimization"),
    )
class Project(models.Model):
    project_name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_contact = models.PositiveIntegerField()
    start_date = models.DateField()
    delivery_date = models.DateField(null=True,blank=True)
    currency = models.CharField(max_length=3,choices=CURRENCY)
    project_value = models.PositiveIntegerField()
    hours = models.DurationField(null=True,blank=True)
    max_hours = models.DurationField(null=True,blank=True)
    hours_approvedby = models.CharField(max_length=50)
    sales_rep = models.CharField(max_length=50)
    project_manager = models.CharField(max_length=50)
    type = models.CharField(max_length=3,choices=TYP)
    status = models.CharField(max_length=2,choices=TAGS)
    date = models.DateField(auto_now_add=True)
    no_milestone = models.PositiveIntegerField()

    def display_duration(self):
        hour = int(self.hours.total_seconds() / 3600)
        minute = int((self.hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"

    def display_duration_max(self):
        hour = int(self.max_hours.total_seconds() / 3600)
        minute = int((self.max_hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"

    def __str__(self):
        return self.project_name
    


# class Task(models.Model):
#     name = models.CharField(max_length=10,choices=TASK_TAGS)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     hours = models.DurationField(null=True,blank=True)

#     def display_duration(self):
#         hour = int(self.hours.total_seconds() / 3600)
#         minute = int((self.hours.total_seconds() % 3600) / 60)
#         return f"{hour} hrs {minute} mins"
    
#     def __str__(self):
#         return f"{self.name} ({self.project.project_name})"


class Resource(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hours = models.DurationField()
    max_hours = models.DurationField()
    date = models.DateField(auto_now_add=True)
    
    def display_duration(self):
        if self.hours is None:
            return ''
        hour = int(self.hours.total_seconds() / 3600)
        minute = int((self.hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"

    def display_duration_max(self):
        if self.max_hours is None:
            return ''
        hour = int(self.max_hours.total_seconds() / 3600)
        minute = int((self.max_hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"

    def __str__(self):
        return f"{self.employee.first_name} ({self.project.project_name})"


class Ips(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.CharField(max_length=15,choices=TASK_TAGS)
    comments = models.CharField(max_length=200, null=True)
    hours = models.DurationField()
    date = models.DateField(auto_now_add=True)
    
    def display_duration(self):
        hour = int(self.hours.total_seconds() / 3600)
        minute = int((self.hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"
    
    def __str__(self):
        return str(self.id)


STS = (
    ("PR", "Present"),
    ("AB", "Absent"),
    )
class Attendance(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	checkin = models.DateTimeField(null=True,blank=True)
	checkout = models.DateTimeField(null=True,blank=True)
	difference = models.DurationField(null=True,blank=True)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=2,choices=STS)
	def __str__(self):
		return f'{self.checkin} ({self.checkout})'
    

class Menu(models.Model):
    name = models.CharField(max_length=50, null=True)
    item_1 = models.CharField(max_length=50, null=True)
    item_2 = models.CharField(max_length=50, null=True)
    item_3 = models.CharField(max_length=50, null=True)
    item_4 = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    def __str__(self):
        return self.name
    

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hours = models.DurationField()
    delivery_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return f'{self.name} ({self.project})'
    

class Sprint(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    name = name = models.CharField(max_length=100)
    hours = models.DurationField()
    def display_duration(self):
        hour = int(self.hours.total_seconds() / 3600)
        minute = int((self.hours.total_seconds() % 3600) / 60)
        return f"{hour} hrs {minute} mins"
    def __str__(self):
        return f'{self.name} {self.milestone} ({self.milestone.project})'
    
