from django.shortcuts import render
from django.http import HttpResponse
from .middleware import Accesare
from .middleware import data_in_romana
from django.utils.html import escape
from django.shortcuts import render
from django.urls import get_resolver, URLPattern, URLResolver

# Create your views here.
accesari = []

def index(request):
    accesare = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    
    accesari.append(accesare)
    print(accesare)
    
    return render(request, "index.html")
    
def info(request):    
    accesare = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    
    accesari.append(accesare)
    print(accesare)
    
    tip_data = request.GET.get("data", "")
    sectiune_data = accesare.data(tip_data)
    
    return render(request, "info.html", {
        "sectiune_data": sectiune_data
    })
    
def exemplu_template(request):
    return render(request,"template.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )

def exemplu_template2(request):
    return render(request,"template2.html")

def obtine_pagini(patterns, prefix=""):
    pagini = []

    for pattern in patterns:
        if isinstance(pattern, URLPattern):
            pagini.append("/" + prefix + str(pattern.pattern))

        elif isinstance(pattern, URLResolver):
            pagini.extend(
                obtine_pagini(pattern.url_patterns, prefix + str(pattern.pattern))
            )

    return pagini

def log(request):
    accesare = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    accesari.append(accesare)

    ultimele = request.GET.get("ultimele")
    detalii = request.GET.get("accesari")
    iduri = request.GET.getlist("iduri")
    dubluri = request.GET.get("dubluri", "false")
    tabel = request.GET.get("tabel")
    mesaj = ""

    # Subpunctul 1 - ultimele n accesari
    if ultimele is None:
        lista_afisata = accesari

    else:
        try:
            n = int(ultimele)

            if n < 0:
                return HttpResponse(
                    "Parametrul ultimele trebuie sa fie un numar pozitiv."
                )

            if n == 0:
                lista_afisata = []

            elif n > len(accesari):
                k = len(accesari)
                lista_afisata = accesari
                mesaj = f"<p>Exista doar {k} accesari fata de {n} accesari cerute</p>"

            else:
                lista_afisata = accesari[-n:]

        except ValueError:
            return HttpResponse(
                "Parametrul ultimele trebuie sa fie numeric."
            )

    # Subpunctul 2 - filtrare dupa iduri
    if iduri:
        lista_iduri = []

        for grup in iduri:
            for id_text in grup.split(","):
                try:
                    id_numar = int(id_text)
                    lista_iduri.append(id_numar)
                except ValueError:
                    return HttpResponse("Eroare: idurile trebuie sa fie numere intregi.")

        if dubluri != "true":
            lista_iduri = list(dict.fromkeys(lista_iduri))

        lista_filtrata = []

        for id_cautat in lista_iduri:
            for a in lista_afisata:
                if a.id == id_cautat:
                    lista_filtrata.append(a)
                    break

        lista_afisata = lista_filtrata

    continut = "<h1>Log accesari</h1>"

    if tabel is not None:
        proprietati = ["id", "ip_client", "url", "pagina", "data", "lista_parametri"]

        if tabel == "tot":
            coloane = proprietati
        else:
            coloane = tabel.split(",")

        if any(col not in proprietati for col in coloane):
            return HttpResponse("Eroare: proprietate invalida.")

        continut += "<table border='1'>"

        # Antetul tabelului
        continut += "<tr>"
        for col in coloane:
            continut += f"<th>{col}</th>"
        continut += "</tr>"

        # Datele accesarilor
        for a in lista_afisata:
            continut += "<tr>"

            valori = {
                "id": a.id,
                "ip_client": a.ip_client,
                "url": a.url(),
                "pagina": a.pagina(),
                "data": a.data_accesare.strftime("%d/%m/%Y %H:%M:%S"),
                "lista_parametri": a.lista_parametri()
            }

            for col in coloane:
                continut += f"<td>{valori[col]}</td>"

            continut += "</tr>"

        continut += "</table>"

    else:
        for a in lista_afisata:
            continut += f"<pre>{str(a)}</pre>"

    if mesaj:
        continut += mesaj

    # Subpunctul 2 - accesari=nr
    if detalii == "nr":
        continut += "<h2>Numar accesari</h2>"
        continut += f"<p>Numar total de accesari: {len(accesari)}</p>"

    # Subpunctul 3 - accesari=detalii
    if detalii == "detalii":
        continut += "<h2>Detalii accesari</h2>"
        continut += "<ul>"

        for a in lista_afisata:
            data_ora = data_in_romana(
                a.data_accesare,
                "%A, %d %B %Y %H:%M:%S"
            )
            continut += f"<li>{data_ora}</li>"

        continut += "</ul>"

    # Subpunctul 3 - Parametri
    continut += "<h2>Parametri</h2>"

    numar_parametri = len(request.GET)
    continut += f"<p>Numar parametri: {numar_parametri}</p>"

    continut += "<ul>"

    for nume_parametru in request.GET.keys():
        continut += f"<li>{nume_parametru}</li>"

    continut += "</ul>"
    
    pagini = {
        p: 0
        for p in obtine_pagini(get_resolver().url_patterns)
        if p.startswith("/app/")
    }

    for a in accesari:
        pagina = a.pagina()

        if pagina in pagini:
            pagini[pagina] += 1

    minim = min(pagini.values())
    maxim = max(pagini.values())

    pagini_minime = [p for p in pagini if pagini[p] == minim]
    pagini_maxime = [p for p in pagini if pagini[p] == maxim]

    continut += "<h2>Statistici accesari</h2>"
    continut += f"<p>Pagina cea mai putin accesata: {', '.join(pagini_minime)} ({minim} accesari)</p>"
    continut += f"<p>Pagina cea mai mult accesata: {', '.join(pagini_maxime)} ({maxim} accesari)</p>"

    return render(request, "log.html", {
    "continut": continut
    })

def istoric(request):
    accesare = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    accesari.append(accesare)

    return render(request, "istoric.html")


def despre(request):
    accesare = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    accesari.append(accesare)

    return render(request, "despre.html")  

def detalii_accesare(request, id):
    accesare_noua = Accesare(
        ip_client=request.ip,
        parametri=request.GET,
        url=request.get_full_path()
    )
    accesari.append(accesare_noua)

    for a in accesari:
        if a.id == int(id):
            continut = "<h1>Detalii accesare</h1>"
            continut += f"<pre>{escape(str(a))}</pre>"
            return HttpResponse(continut)

    return HttpResponse(
        "<h1>Eroare: accesarea nu exista</h1>",
        status=404
    )
    
def in_lucru(request):
    return render(request, "in_lucru.html")


