from datetime import datetime

def get_ip(request):
    req_headers = request.META
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')

class Accesare:
    contor=1
    def __init__(self, ip_client, parametri={}, url=""):
        self.id=Accesare.contor
        Accesare.contor+=1
        self.ip_client=ip_client
        self.url_complet = url
        self.parametri = parametri
        self.data_accesare = datetime.now()
        
    def __str__(self):
        return (
        f"id: {self.id}\n"
        f"ip_client: {self.ip_client}\n"
        f"url: {self.url()}\n"
        f"pagina: {self.pagina()}\n"
        f"data: {self.data()}\n"
        f"lista_parametri: {self.lista_parametri()}"
    )
    
    def lista_parametri(self):
        return list(self.parametri.items())
    
    def url(self):
        return self.url_complet

    def pagina(self):
        return self.url_complet.split("?")[0]
    
    def data(self, tip="", format="%A, %d %B %Y"):
        data_formatata = data_in_romana(self.data_accesare, format)
        ora = self.data_accesare.strftime("%H:%M:%S")

        if tip == "zi":
            return f"<h2>Data</h2><p>{data_formatata}</p>"

        if tip == "timp":
            return f"<h2>Ora</h2><p>{ora}</p>"

        return f"<h2>Data si ora</h2><p>{data_formatata}, {ora}</p>"

def data_in_romana(data, format="%A, %d %B %Y"):
    zile = {
        "Monday": "Luni",
        "Tuesday": "Marti",
        "Wednesday": "Miercuri",
        "Thursday": "Joi",
        "Friday": "Vineri",
        "Saturday": "Sambata",
        "Sunday": "Duminica"
    }

    luni = {
        "January": "Ianuarie",
        "February": "Februarie",
        "March": "Martie",
        "April": "Aprilie",
        "May": "Mai",
        "June": "Iunie",
        "July": "Iulie",
        "August": "August",
        "September": "Septembrie",
        "October": "Octombrie",
        "November": "Noiembrie",
        "December": "Decembrie"
    }

    rezultat = data.strftime(format)

    for engleza, romana in zile.items():
        rezultat = rezultat.replace(engleza, romana)

    for engleza, romana in luni.items():
        rezultat = rezultat.replace(engleza, romana)

    return rezultat
  
class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # cod de procesare a cererii ....      
        #putem trimite date către funcția de vizualizare; le setăm ca proprietăți în request     
        request.proprietate_noua=17
        request.ip=get_ip(request)       
        # se apelează indirect funcția de vizualizare (din views.py)
        response = self.get_response(request)      

        # putem adauga un header HTTP pentru toate răspunsurile
        response['header_nou'] = 'valoare'
        
        #verificăm tipul de conținut folosind headerul HTTP Content-Type
        # putem transmite divere resurse (imagini, css etc.), nu doar html-uri
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
           
            # obținem conținutul raspunsului
            # (response.content este memorat sub forma de bytes -> transformăm în string
            content = response.content.decode('utf-8')
           
            # Modificăm conținutul raspunsului generat din views
            new_content = content.replace(
                '</body>',
                f'<div>Ip: {request.ip}</div></body>'
            )
           
            # Suprascriem conținutul răspunsului (in obiectul response)
            response.content = new_content.encode('utf-8')
           
            # Actualizăm lungimea conținutului -> obligatoriu pentru headerele HTTP
            response['Content-Length'] = len(response.content)
       
        return response
