import requests
import re
import time
import html
import json
import os
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURATION DES IDENTIFIANTS
# ==========================================
USERNAME = os.environ.get("MESRS_USERNAME")
PASSWORD = os.environ.get("MESRS_PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ Erreur : Identifiants introuvables. Vérifiez les GitHub Secrets.")
    exit(1)

# URLs
URL_LOGIN = "https://progres.mesrs.dz/webrecrutement/index.xhtml"
URL_VOEUX = "https://progres.mesrs.dz/webrecrutement/pages/editVoeuxCandidat.xhtml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# La liste complète des 179 établissements
ETABLISSEMENTS = {
    "5186397": "المدرسة الوطنية العليا للعلوم الاسلامية  دار القرآن",
    "136974": "université oran 1",
    "136984": "université larbi tébessi tébessa",
    "136985": "université ibn khaldoun - tiaret",
    "136976": "université d’oum el bouaghi",
    "1950": "université d’oran 2 mohamed ben ahmed",
    "136989": "Université de Tlemcen",
    "137306": "université de tissemsilt",
    "137305": "Université de tipaza",
    "137307": "Université de tindouf",
    "137304": "université de tamanghasset",
    "136978": "université des sciences islamiques émir abdelkader constantine",
    "136987": "université des sciences et de la technologie houari boumediène alger",
    "136988": "université des sciences et de la technologie d'oran",
    "5186399": "Université des sciences de la santé alger",
    "136983": "université de souk ahras",
    "136982": "université de skikda",
    "136981": "université de sidi bel abbes",
    "136980": "université de sétif 2",
    "136979": "université de sétif 1",
    "136977": "université de saida",
    "137303": "université de relizane",
    "136975": "université de ouargla",
    "137302": "université de naama",
    "136973": "université de m’sila",
    "136972": "université de mostaganem",
    "137301": "université de mila",
    "136971": "université de médéa",
    "136970": "université de mascara",
    "136963": "université d’el tarf",
    "136962": "université d’el oued",
    "136969": "université de laghouat",
    "5186267": "université de la formation continue",
    "136968": "université de khenchela",
    "136967": "université de khemis miliana",
    "136966": "université de jijel",
    "136965": "université de guelma",
    "136964": "université de ghardaia",
    "136961": "université de djelfa",
    "136960": "université de  constantine 3 salah boubnider",
    "136958": "université de constantine 1",
    "136957": "université de chlef",
    "136956": "université de boumerdes",
    "136955": "université de bouira",
    "136954": "université de bordj bou arréridj",
    "136953": "université de blida 2",
    "136952": "université de blida 1",
    "136951": "université de biskra",
    "136950": "université de béjaia",
    "136657": "université de béchar",
    "136656": "université de batna 1",
    "136653": "Université d’alger 2",
    "136652": "université d’alger 1",
    "136991": "université  d'ain temouchent",
    "136651": "université d'adrar",
    "136959": "université constantine 2-abdelhamid mehri",
    "473": "université batna 2",
    "136655": "université badji mokhtar de annaba",
    "136654": "Université Alger 3",
    "136986": "Université mouloud mammeri – tizi ouzou",
    "5186403": "Ministère de la Santé",
    "5186274": "ENSEREDD",
    "5186390": "Instruit Supérieur des Sciences (I.S.S)",
    "5186240": "institut supérieur pour les hautes études de sécurité nationale.  el -biar",
    "5186248": "institut supérieur des métiers des arts du spectacle et de l’audio-visuel. bordj - el - kiffan",
    "5186392": "Institut Supérieur des Langues Etrangères En-nour (ISLE)",
    "5186391": "Institut Supérieur de gestion (ISG)",
    "5186251": "institut supérieur de formation ferroviaire.  rouiba / alger",
    "5186389": "Institut Supérieur de Commerce et de Gestion (I.S.C.G)",
    "5186272": "institut ntionale des finances (inf)",
    "5186250": "institut national supérieur de musique /alger",
    "5186319": "institut national de recherche forestière",
    "5186318": "institut national de la recherche agronomique d’algérie (inraa)",
    "5186255": "institut national de la poste et des TIC /alger",
    "5186253": "institut hydrométéorologique de formation et de recherche /  oran",
    "5186385": "Institut d’Optométrie (I.O) Bordj Bou-Arreridj",
    "5186393": "Institut  de Technologie (Futuris Institute)",
    "5186383": "Institut de Management (INSIM  SUP)",
    "5186380": "Institut de Management et Développement (MDI) Alger",
    "5186381": "Institut de Management d’Alger (IMA)",
    "5186259": "institut de formation supérieure en sciences et technologie du sport d’ain-benian",
    "5186260": "institut de formation supérieure des cadres de la jeunesse.tixeraine",
    "5186262": "institut de formation supérieure des cadres de la jeunesse. ouargla",
    "5186263": "institut de formation supérieure des cadres de la jeunesse et des sports. oran",
    "5186261": "institut de formation supérieure des cadres de la jeunesse et des sports. constantine",
    "5186382": "Institut de Formation d’Assurances et de Gestion (IFAG)",
    "5186234": "école supérieure navale de tamentfoust / alger",
    "5186275": "école supérieure en sciences et technologies de l'informatique et du numérique de bejaia",
    "269": "ecole supérieure en sciences appliquées de tlemcen",
    "137345": "ecole supérieure en informatique 08 mai 1945 -sidi bel abbes-",
    "297": "école supérieure en génie électrique et énergétique",
    "5186237": "école supérieure du matériel. el harrach",
    "5186379": "Ecole Supérieure d’Hôtellerie et de Restauration d’Alger (ESHRA)",
    "254": "ecole supérieure de technologies industrielles annaba",
    "5186242": "école supérieure  des transmissions. koléa ",
    "5186236": "école supérieure des techniques de l’aéronautique. dar el beida",
    "5186388": "Ecole Supérieure des Sciences et Technologie (E.S.S.T)",
    "5186243": "ecole supérieure des sciences de l’information et de la communication.sidi fredj",
    "222": "ecole supérieure des sciences de l’aliment et des industries agroalimentaires d’alger",
    "137310": "école supérieure des sciences de gestion annaba",
    "5186211": "ecole supérieure des sciences biologiques  d’ oran",
    "5186254": "école supérieure  de sécurité sociale. ben - aknoun / alger.",
    "5186249": "ecole supérieure des beaux - arts. telemly /alger",
    "284": "ecole supérieure de management de tlemcen",
    "5186245": "école supérieure de l’air. tafraoui / oran.",
    "5186241": "ecole supérieure de la gendarmerie nationale. zéralda",
    "5186244": "école supérieure de l’administration militaire / oran",
    "5186235": "ecole supérieure de la défense aérienne du territoire. réghaia",
    "137308": "école supérieure de gestion et de l’economie numérique –koléa",
    "137312": "École Supérieure d’Économie d’Oran",
    "137309": "ecole supérieure de comptabilité et de finance de constantine",
    "1958": "ecole supérieure de commerce",
    "5186325": "école supérieure  d’agriculture saharienne d’el oued",
    "5186378": " Ecole supérieure algérienne des affaires",
    "311": "ecole supérieure agronomique de mostaganem",
    "5186246": "ecole spécialisée hélicoptères ain -arnat / sétif",
    "137343": "ecole polytechnique d'architecture et d'urbanisme le moudjahid hocine ait ahmed",
    "137323": "ecole normale supérieure - laghouat",
    "137322": "ecole normale supérieure - kouba",
    "137325": "Ecole Normale Supérieure d’Oran",
    "5186355": "ecole normale supérieure des sourds-muets",
    "1962": "ecole normale supérieure de sétif",
    "5186368": "ecole normale supérieure de saida",
    "1963": "ecole normale supérieure de ouargla",
    "137326": "ENSET skikda",
    "137324": "ecole normale supérieure de mostaganem",
    "137320": "ecole normale supérieure de bouzaréah",
    "456": "ecole normale supérieure de bou saâda",
    "1961": "ecole normale supérieure de bechar",
    "137321": "ecole normale supérieure assia djebar constantine",
    "137342": "ecole nationale supérieure vétérinaire",
    "5186252": "ecole nationale supérieure maritime.  bou - smail. / tipaza",
    "5186264": "ecole nationale supérieure « imama » dar el imam /alger",
    "137339": "ecole nationale supérieure en statistiques et en économie appliquée",
    "5186285": "ecole nationale superieure en mathematiques alger pole de sidi abdellah",
    "5186284": "ecole nationale superieure en intelligence artificielle alger",
    "5186257": "école nationale supérieure du tourisme / alger",
    "1": "Ecole nationale Supérieure d'Informatique",
    "137332": "ecole nationale supérieure d'hydraulique",
    "5186362": "École Nationale Supérieure de Technologie et d'Ingénierie (Annaba)",
    "5186258": "ecole nationale supérieure de technologie du sport",
    "5186366": "Ecole Nationale Supérieure de Technologie des Systèmes Autonomes",
    "137340": "ecole nationale supérieure de technologie",
    "137341": "ecole nationale supérieure des travaux publics",
    "5186256": "ecole nationale supèrieure  des TIC / oran",
    "5186364": "Ecole Nationale Supérieure des Technologies Avancées",
    "5186208": "ecole nationale supérieure des sciences politiques",
    "5186377": "Ecole Nationale Supérieure des Sciences Géodésiques",
    "137337": "ecole nationale supérieure des sciences de la mer",
    "5186367": "ecole nationale supérieure des nanosciences et nanotechnologie",
    "137335": "ecole nationale supérieure des mines et de la métallurgie",
    "5186273": "école nationale supérieure des forêts",
    "5185704": "ecole nationale supérieure de management",
    "5186207": "ecole nationale supérieure de journalisme et des sciences de l’information",
    "5186372": "Ecole Nationale Supérieure de Cybersécurité",
    "137331": "ecole nationale supérieure de biotechnologie - constantine",
    "5186326": "école nationale supérieure  d’agriculture saharienne d’adrar",
    "137330": "ecole nationale supérieure agronomique",
    "5186232": "école nationale préparatoire aux études d’ingéniorat. rouïba",
    "137329": "ecole nationale polytechnique d’oran",
    "137336": "ecole nationale polytechnique de constantine",
    "137328": "ecole nationale polytechnique",
    "5186239": "école nationale de santé paramédicale militaire",
    "5186238": "école nationale de santé militaire",
    "5186247": "école nationale de conservation et de restauration des biens culturels",
    "5186265": "ENA",
    "5186233": "école militaire polytechnique / bordj -el -bahri",
    "1959": "Ecole des Hautes Etudes Commerciales",
    "5186384": "Ecole de Management de Tizi Ouzou (EMTO)",
    "5186387": "Ecole de Management d’Alger Business School  (E.M.A)",
    "5186386": "Ecole de Formation en Techniques de Gestion (E.F.T.G)",
    "2596297": "centre universitaire el chérif bouchoucha aflou",
    "137300": "centre universitaire d'illizi",
    "2596285": "centre universitaire de maghnia",
    "136992": "centre universitaire d’el bayadh",
    "2596309": "centre universitaire de barika",
    "5186317": "centre national de la recherche et de développement pour la peche et l'aquaculture",
    "5186316": "centre de recherche des satellites",
    "5186266": "autre etablissement",
    "5186231": "académie militaire de cherchell"
}

def recuperer_date_limite(session, view_state, etab_id, filiere_id):
    """
    Fonction Magique: Effectue la danse pour extraire la date (Trouver Spécialité -> Ajouter -> Lire -> Supprimer)
    """
    headers_ajax = HEADERS.copy()
    headers_ajax["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers_ajax["Faces-Request"] = "partial/ajax"
    date_limite = "Inconnue"

    try:
        # --- 1. SÉLECTIONNER LA FILIÈRE POUR AVOIR L'ID DE LA SPÉCIALITÉ ---
        payload_spec = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "editVoeuxCandidatForm:master1",
            "javax.faces.partial.execute": "editVoeuxCandidatForm:master1",
            "javax.faces.partial.render": "editVoeuxCandidatForm:specialite",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "editVoeuxCandidatForm": "editVoeuxCandidatForm",
            "editVoeuxCandidatForm:etab1_input": etab_id,
            "editVoeuxCandidatForm:master1_input": filiere_id,
            "editVoeuxCandidatForm:specialite_input": "0",
            "javax.faces.ViewState": view_state
        }
        r_spec = session.post(URL_VOEUX, headers=headers_ajax, data=payload_spec)
        match_vs = re.search(r'update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]></update>', r_spec.text)
        if match_vs: view_state = match_vs.group(1)
        
        # Trouver la première spécialité valide
        specs = re.findall(r'<option value="([^"]+)".*?</option>', r_spec.text)
        spec_id = "0"
        for s in specs:
            if s != "0":
                spec_id = s
                break
                
        if spec_id == "0": return date_limite, view_state

        # --- 2. AJOUTER AU PANIER ---
        payload_add = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "editVoeuxCandidatForm:j_idt114",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "editVoeuxCandidatForm",
            "editVoeuxCandidatForm:j_idt114": "editVoeuxCandidatForm:j_idt114",
            "editVoeuxCandidatForm": "editVoeuxCandidatForm",
            "editVoeuxCandidatForm:etab1_input": etab_id,
            "editVoeuxCandidatForm:master1_input": filiere_id,
            "editVoeuxCandidatForm:specialite_input": spec_id,
            "javax.faces.ViewState": view_state
        }
        r_add = session.post(URL_VOEUX, headers=headers_ajax, data=payload_add)
        match_vs = re.search(r'update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]></update>', r_add.text)
        if match_vs: view_state = match_vs.group(1)

        # --- 3. LIRE LA DATE (L'œil) ---
        payload_read = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "editVoeuxCandidatForm:voeuxTable:0:detail",
            "javax.faces.partial.execute": "editVoeuxCandidatForm:voeuxTable:0:detail",
            "javax.faces.partial.render": "editVoeuxCandidatForm:detailDialog",
            "editVoeuxCandidatForm:voeuxTable:0:detail": "editVoeuxCandidatForm:voeuxTable:0:detail",
            "editVoeuxCandidatForm": "editVoeuxCandidatForm",
            "javax.faces.ViewState": view_state
        }
        r_read = session.post(URL_VOEUX, headers=headers_ajax, data=payload_read)
        match_date = re.search(r'<label id="editVoeuxCandidatForm:j_idt143" class="ui-outputlabel ui-widget value">(.*?)</label>', r_read.text)
        if match_date:
            date_limite = match_date.group(1).strip()
            
        match_vs = re.search(r'update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]></update>', r_read.text)
        if match_vs: view_state = match_vs.group(1)

        # --- 4. SUPPRIMER DU PANIER (La poubelle) ---
        payload_delete = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "editVoeuxCandidatForm:voeuxTable:0:delete",
            "javax.faces.partial.execute": "editVoeuxCandidatForm:voeuxTable:0:delete",
            "javax.faces.partial.render": "editVoeuxCandidatForm",
            "editVoeuxCandidatForm:voeuxTable:0:delete": "editVoeuxCandidatForm:voeuxTable:0:delete",
            "editVoeuxCandidatForm": "editVoeuxCandidatForm",
            "javax.faces.ViewState": view_state
        }
        r_delete = session.post(URL_VOEUX, headers=headers_ajax, data=payload_delete)
        match_vs = re.search(r'update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]></update>', r_delete.text)
        if match_vs: view_state = match_vs.group(1)
        
    except Exception as e:
        print(f" [Erreur Date: {e}]", end="")
        
    return date_limite, view_state


def login_et_scanner():
    print("\n" + "="*50)
    print("🚀 DÉMARRAGE DU TRACKER AVEC CONNEXION AUTO ET DÉLAIS")
    print("="*50 + "\n")
    
    # CHARGEMENT DU CACHE : On mémorise les anciennes dates pour ne pas spammer le site !
    cache_dates = {}
    if os.path.exists("postes_ouverts.json"):
        try:
            with open("postes_ouverts.json", "r", encoding="utf-8") as f:
                anciennes_donnees = json.load(f)
                for poste in anciennes_donnees.get("postes", []):
                    if "date_limite" in poste and poste["date_limite"] != "Inconnue":
                        cache_dates[poste["universite"]] = poste["date_limite"]
        except Exception:
            pass

    session = requests.Session()
    
    print("1️⃣ Accès à la page de connexion...")
    try:
        response_login_page = session.get(URL_LOGIN, headers=HEADERS, timeout=120)
        match_vs_login = re.search(r'name="javax\.faces\.ViewState".*?value="([^"]+)"', response_login_page.text)
        
        if not match_vs_login:
            print("❌ Échec : ViewState de login introuvable.")
            return
            
        view_state_login = match_vs_login.group(1)
        
        print("2️⃣ Tentative de connexion...")
        payload_login = {
            "loginFrm": "loginFrm",
            "loginFrm:j_username": USERNAME,
            "loginFrm:j_password": PASSWORD,
            "loginFrm:loginBtn": "",
            "javax.faces.ViewState": view_state_login
        }
        
        headers_post_login = HEADERS.copy()
        headers_post_login["Content-Type"] = "application/x-www-form-urlencoded"
        response_auth = session.post(URL_LOGIN, headers=headers_post_login, data=payload_login)
        
        if "Déconnexion" in response_auth.text or "Mon Dossier" in response_auth.text or "BOUSSOUF" in response_auth.text:
            print("✅ Connexion réussie !\n")
        else:
            print("❌ Échec de la connexion. Vérifie tes identifiants.")
            return

        print("3️⃣ Accès à la page des concours...")
        response_voeux = session.get(URL_VOEUX, headers=HEADERS)
        match_vs_voeux = re.search(r'name="javax\.faces\.ViewState".*?value="([^"]+)"', response_voeux.text)
        if not match_vs_voeux: return
        view_state = match_vs_voeux.group(1)
        
        print(f"\n4️⃣ Début du scan des {len(ETABLISSEMENTS)} universités...\n")
        headers_ajax = HEADERS.copy()
        headers_ajax["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers_ajax["Faces-Request"] = "partial/ajax"
        
        compteur = 0
        total = len(ETABLISSEMENTS)
        resultats_propres = []
        
        for i, (id_etab, nom_etab) in enumerate(ETABLISSEMENTS.items(), 1):
            print(f"[{i}/{total}] {nom_etab[:40]}...", end=" ", flush=True)
            
            payload_ajax = {
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "editVoeuxCandidatForm:etab1",
                "javax.faces.partial.execute": "editVoeuxCandidatForm:etab1",
                "javax.faces.partial.render": "editVoeuxCandidatForm:master1",
                "javax.faces.behavior.event": "change",
                "javax.faces.partial.event": "change",
                "editVoeuxCandidatForm": "editVoeuxCandidatForm",
                "editVoeuxCandidatForm:etab1_focus": "",
                "editVoeuxCandidatForm:etab1_input": id_etab,
                "editVoeuxCandidatForm:master1_focus": "",
                "editVoeuxCandidatForm:master1_input": "0",
                "editVoeuxCandidatForm:specialite_focus": "",
                "editVoeuxCandidatForm:specialite_input": "0",
                "javax.faces.ViewState": view_state
            }
            
            response_post = session.post(URL_VOEUX, headers=headers_ajax, data=payload_ajax)
            match_new_vs = re.search(r'javax\.faces\.ViewState[^>]*><!\[CDATA\[(.*?)\]\]>', response_post.text)
            if match_new_vs: view_state = match_new_vs.group(1)
            
            options = re.findall(r'<option value="([^"]+)".*?>(.*?)</option>', response_post.text)
            filieres = [(val, html.unescape(nom)) for val, nom in options if val != "0"]
            
            if filieres:
                print(" ✅ POSTES OUVERTS !")
                
                # --- MAGIE DU CACHE : On récupère la date si on ne l'a pas encore ! ---
                if nom_etab not in cache_dates:
                    print("     🔍 Récupération de la date limite en cours...", end=" ")
                    id_premiere_filiere = filieres[0][0] # On prend la toute première
                    date_univ, view_state = recuperer_date_limite(session, view_state, id_etab, id_premiere_filiere)
                    cache_dates[nom_etab] = date_univ
                    print(f"[{date_univ}]")
                # ----------------------------------------------------------------------

                for val_fil, nom_fil in filieres:
                    match_nettoyage = re.search(r'Filière \d+:\s*(.*?)\s*\(Nombre de poste :\s*(\d+)\s*\),\s*(.*)', nom_fil)
                    if match_nettoyage:
                        specialite = match_nettoyage.group(1).strip()
                        nb_postes = int(match_nettoyage.group(2))
                        entite = match_nettoyage.group(3).strip()
                    else:
                        specialite = nom_fil
                        nb_postes = "?"
                        entite = "Inconnue"
                        
                    print(f"      -> {specialite} ({nb_postes} postes)")
                    
                    resultats_propres.append({
                        "universite": nom_etab,
                        "specialite": specialite,
                        "postes": nb_postes,
                        "departement": entite,
                        "date_limite": cache_dates[nom_etab] # La date est injectée ici !
                    })
                compteur += 1
            else:
                print(" Vide.")
                
            time.sleep(1) # Pause anti-bannissement

        print("\n" + "="*50)
        print(f"🎉 Scan terminé ! {compteur} établissement(s) recrutent actuellement.")
        
        donnees_finales = {
            "mise_a_jour": datetime.now().strftime("%d/%m/%Y à %H:%M"),
            "postes": resultats_propres
        }
        
        with open("postes_ouverts.json", "w", encoding="utf-8") as f:
            json.dump(donnees_finales, f, ensure_ascii=False, indent=4)
            
        print(f"💾 Les données ont été sauvegardées dans 'postes_ouverts.json'")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Erreur technique inattendue : {e}")

if __name__ == "__main__":
    login_et_scanner()
