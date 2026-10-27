
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField


# 1. CATEGORIE

class Categorie(models.Model):
    id_categorie = models.BigAutoField(primary_key=True)

    nume = models.CharField(
        max_length=100,
        unique=True,
        help_text="Denumirea categoriei, de exemplu SUV sau Sedan.",
        error_messages={
            "unique": "Exista deja o categorie cu acest nume.",
            "max_length": "Numele categoriei este prea lung.",
        }
    )

    descriere = models.TextField(null=True, blank=True)

    culoare = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="Culoarea asociata categoriei, folosita la afisare."
    )

    sigla = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Calea sau URL-ul catre sigla categoriei."
    )

    ordine_afisare = models.PositiveIntegerField(
        default=0,
        help_text="Ordinea in care apare categoria pe site."
    )

    etichete = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Etichete asociate categoriei, de exemplu familie, oras."
    )

    class Meta:
        ordering = ["ordine_afisare", "nume"]
        verbose_name = "Categorie"
        verbose_name_plural = "Categorii"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(ordine_afisare__gte=0),
                name="categorie_ordine_pozitiva"
            )
        ]

    def __str__(self):
        return self.nume


# 2. MARCA

class Marca(models.Model):
    id_marca = models.BigAutoField(primary_key=True)

    nume = models.CharField(
        max_length=100,
        unique=True,
        help_text="Numele producatorului auto.",
        error_messages={
            "unique": "Aceasta marca exista deja.",
            "max_length": "Numele marcii este prea lung.",
        }
    )

    tara_origine = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    an_infiintare = models.PositiveIntegerField(
        help_text="Anul infiintarii producatorului auto.",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["nume"]
        verbose_name = "Marca"
        verbose_name_plural = "Marci"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(an_infiintare__gte=1700) &
                    models.Q(an_infiintare__lte=2100)
                ) | models.Q(an_infiintare__isnull=True),
                name="marca_an_valid",
                violation_error_message="Anul infiintarii trebuie sa fie intre 1700 si 2100."
            )
        ]

    def __str__(self):
        return self.nume


# 3. SEDIU

class Sediu(models.Model):
    id_sediu = models.BigAutoField(primary_key=True)

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "Exista deja un sediu cu acest nume."
        }
    )

    adresa = models.CharField(max_length=255)

    telefon = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text="Adresa de email de contact a sediului.",
        error_messages={
            "invalid": "Introduceti o adresa de email valida.",
            "unique": "Aceasta adresa de email este deja folosita."
        }
    )

    class Meta:
        verbose_name = "Sediu"
        verbose_name_plural = "Sedii"

    def __str__(self):
        return f"{self.nume} - {self.adresa}"


# 4. DOTARE

class Dotare(models.Model):
    TIP_DOTARE_CHOICES = [
        ("confort", "Confort"),
        ("siguranta", "Siguranta"),
        ("tehnologie", "Tehnologie"),
        ("exterior", "Exterior"),
        ("performanta", "Performanta"),
    ]

    id_dotare = models.BigAutoField(primary_key=True)

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "Aceasta dotare exista deja."
        }
    )

    descriere = models.TextField(
        null=True,
        blank=True
    )

    tip_dotare = models.CharField(
        max_length=20,
        choices=TIP_DOTARE_CHOICES,
        default="confort",
        help_text="Categoria functionala a dotarii."
    )

    class Meta:
        ordering = ["tip_dotare", "nume"]
        verbose_name = "Dotare"
        verbose_name_plural = "Dotari"

    def __str__(self):
        return self.nume


# 5. AUTOTURISM

class Autoturism(models.Model):
    COMBUSTIBIL_CHOICES = [
        ("benzina", "Benzina"),
        ("motorina", "Motorina"),
        ("electric", "Electric"),
        ("hibrid", "Hibrid"),
        ("gpl", "GPL"),
    ]

    TRANSMISIE_CHOICES = [
        ("manuala", "Manuala"),
        ("automata", "Automata"),
    ]

    id_autoturism = models.BigAutoField(primary_key=True)

    model = models.CharField(
        max_length=100,
        help_text="Modelul masinii, de exemplu Golf sau Seria 3.",
        error_messages={
            "blank": "Modelul autoturismului este obligatoriu.",
            "max_length": "Numele modelului este prea lung."
        }
    )

    an_fabricatie = models.PositiveIntegerField(
        db_index=True,
        help_text="Anul in care a fost fabricat autoturismul."
    )

    pret = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_index=True,
        help_text="Pretul autoturismului in EUR.",
        error_messages={
            "invalid": "Introduceti un pret numeric valid."
        }
    )

    kilometraj = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Numarul de kilometri parcursi de autoturism."
    )

    combustibil = models.CharField(
        max_length=20,
        choices=COMBUSTIBIL_CHOICES
    )

    transmisie = models.CharField(
        max_length=20,
        choices=TRANSMISIE_CHOICES
    )

    culoare = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    serie_sasiu = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-HJ-NPR-Z0-9]{17}$",
                message="Seria de sasiu trebuie sa contina 17 caractere valide."
            )
        ],
        help_text="Seria VIN, formata din 17 caractere.",
        error_messages={
            "unique": "Exista deja un autoturism cu aceasta serie de sasiu.",
            "blank": "Seria de sasiu este obligatorie."
        }
    )

    disponibil = models.BooleanField(
        default=True,
        blank=True
    )

    data_adaugare = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name="autoturisme"
    )

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name="autoturisme"
    )

    sediu = models.ForeignKey(
        Sediu,
        on_delete=models.PROTECT,
        related_name="autoturisme"
    )

    dotari = models.ManyToManyField(
        Dotare,
        related_name="autoturisme",
        blank=True
    )

    class Meta:
        ordering = ["-data_adaugare"]
        verbose_name = "Autoturism"
        verbose_name_plural = "Autoturisme"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name="autoturism_pret_pozitiv",
                violation_error_message="Pretul trebuie sa fie mai mare decat zero."
            ),
            models.CheckConstraint(
                condition=models.Q(kilometraj__lte=2000000),
                name="autoturism_kilometraj_valid",
                violation_error_message="Kilometrajul depaseste limita admisa."
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(an_fabricatie__gte=1886) &
                    models.Q(an_fabricatie__lte=2100)
                ),
                name="autoturism_an_valid",
                violation_error_message="Anul fabricatiei trebuie sa fie intre 1886 si 2100."
            )
        ]

    def __str__(self):
        return f"{self.marca.nume} {self.model} ({self.an_fabricatie})"


# 6. FOTOGRAFIE_AUTO

class FotografieAuto(models.Model):
    id_fotografie = models.BigAutoField(primary_key=True)

    autoturism = models.ForeignKey(
        Autoturism,
        on_delete=models.CASCADE,
        related_name="fotografii"
    )

    nr_fotografie = models.PositiveIntegerField(
        help_text="Numarul fotografiei pentru autoturismul respectiv."
    )

    cale_fisier = models.ImageField(
        upload_to="autoturisme/",
        help_text="Incarcati o fotografie a autoturismului."
    )

    descriere = models.TextField(
        null=True,
        blank=True
    )

    data_incarcare = models.DateField(
        default=timezone.localdate
    )

    class Meta:
        ordering = ["autoturism", "nr_fotografie"]
        verbose_name = "Fotografie auto"
        verbose_name_plural = "Fotografii auto"

        constraints = [
            models.UniqueConstraint(
                fields=["autoturism", "nr_fotografie"],
                name="fotografie_numar_unic_per_auto"
            ),
            models.CheckConstraint(
                condition=models.Q(nr_fotografie__gte=1),
                name="fotografie_numar_pozitiv",
                violation_error_message="Numarul fotografiei trebuie sa fie cel putin 1."
            )
        ]

    def __str__(self):
        return f"Fotografia {self.nr_fotografie} - {self.autoturism}"
