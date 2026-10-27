from django.contrib import admin
from .models import (
    Categorie, Marca, Sediu,
    Dotare, Autoturism, FotografieAuto
)

# Register your models here.
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ["id_categorie", "nume", "ordine_afisare"]


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ["id_marca", "nume", "tara_origine"]


@admin.register(Sediu)
class SediuAdmin(admin.ModelAdmin):
    list_display = ["id_sediu", "nume", "adresa", "email"]


@admin.register(Dotare)
class DotareAdmin(admin.ModelAdmin):
    list_display = ["id_dotare", "nume", "tip_dotare"]


@admin.register(Autoturism)
class AutoturismAdmin(admin.ModelAdmin):
    list_display = [
        "id_autoturism", "marca", "model",
        "an_fabricatie", "pret", "disponibil"
    ]
    list_filter = ["marca", "categorie", "combustibil", "disponibil"]
    search_fields = ["model", "serie_sasiu"]


@admin.register(FotografieAuto)
class FotografieAutoAdmin(admin.ModelAdmin):
    list_display = [
        "id_fotografie", "autoturism",
        "nr_fotografie", "data_incarcare"
    ]

admin.site.site_header = "Panou de Administrare"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"

