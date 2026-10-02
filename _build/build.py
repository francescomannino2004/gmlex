#!/usr/bin/env python3
"""Generates the static pages of the site in Italian and English.

All text lives in this file. Edit it, then run:  python3 _build/build.py
Italian pages are written to the repository root, English pages to en/.
(Folders starting with "_" are not published by GitHub Pages.)
"""
import datetime
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ('it', 'en')

PAGES = {
    'home':     {'it': 'index.html',            'en': 'en/index.html'},
    'areas':    {'it': 'aree-di-attivita.html', 'en': 'en/practice-areas.html'},
    'press':    {'it': 'rassegna-stampa.html',  'en': 'en/press.html'},
    'contacts': {'it': 'contatti.html',         'en': 'en/contacts.html'},
}

PHONE = '+39 091 325611'
PHONE_HREF = 'tel:+39091325611'
FAX = '+39 091 8163003'
PEC = 'manliomannino@pecavvpa.it'
VAT = None  # Partita IVA (obbligatoria per legge sul sito), es. '01234567890'. Se None non viene mostrata.

OFFICES = [
    {'id': 'palermo', 'city': {'it': 'Palermo', 'en': 'Palermo'},
     'street': 'Via Salvatore Meccio, 16', 'zip': '90141 Palermo',
     'q': 'Via+Salvatore+Meccio+16,+90141+Palermo', 'main': True},
    {'id': 'roma', 'city': {'it': 'Roma', 'en': 'Rome'},
     'street': 'Piazza Cavour, 3', 'zip': '00192 Roma',
     'q': 'Piazza+Cavour+3,+00192+Roma', 'main': False},
]

# ---------------------------------------------------------------------------
# Press coverage. Newest first. "date" is optional (YYYY-MM-DD).
# ---------------------------------------------------------------------------
PRESS = [
    {
        'source': 'PalermoToday',
        'date': '2026-01-13',
        'url': 'https://www.palermotoday.it/cronaca/pediatri-10-euro-accordo-intregrativo-2011-sentenza.html',
        # Titolo originale della testata, citato con la fonte (non tradurre)
        'headline': "Una norma di 15 anni fa e le interpretazioni errate dell'Asp, 4 pediatri riceveranno 100 mila euro",
        # Sintesi scritta dallo Studio: solo fatti riportati nell'articolo (non copiarne il testo)
        'summary': {
            'it': "Gli avvocati Manlio Mannino e Alessandro Gatto hanno assistito quattro pediatri palermitani nel ricorso "
                  "al Tribunale del Lavoro per il compenso di 10 euro per ogni nuovo paziente previsto dall'accordo "
                  "integrativo regionale del 2011, che l'Asp aveva versato una sola volta anziché per ogni anno di cura. "
                  "La controversia si è chiusa con un accordo stragiudiziale con l'Asp, come previsto dalla direttiva "
                  "assessoriale del 30 aprile 2025.",
            'en': "Avv. Manlio Mannino and Avv. Alessandro Gatto represented four Palermo paediatricians before the Labour "
                  "Court in a claim for the €10 fee per new patient provided for by the 2011 regional supplementary "
                  "agreement, which the local health authority (ASP) had paid only once instead of for every year of care. "
                  "The dispute was settled out of court with the ASP, as provided for by the regional directive of "
                  "30 April 2025.",
        },
    },
    {
        'source': 'PalermoToday',
        'date': '2025-05-06',
        'url': 'https://www.palermotoday.it/cronaca/morta-sangue-infetto-epatite-condanna-ministero-risarcimento.html',
        'headline': "Morta per una trasfusione di sangue infetto, condannato il ministero: dovrà pagare oltre 900 mila euro",
        'summary': {
            'it': "La Corte d'Appello ha accolto le tesi degli avvocati Manlio Mannino e Alessandro Gatto, difensori del "
                  "marito e dei tre figli di una donna deceduta per le conseguenze di un'epatite C contratta con "
                  "trasfusioni di sangue. Ribaltando la sentenza di primo grado, la Corte ha condannato il Ministero della "
                  "Salute al risarcimento, applicando il criterio del «più probabile che non» sostenuto dalla difesa per "
                  "collocare il contagio dopo il 1958.",
            'en': "The Court of Appeal upheld the arguments of Avv. Manlio Mannino and Avv. Alessandro Gatto, counsel for "
                  "the husband and three children of a woman who died from the effects of hepatitis C contracted through "
                  "blood transfusions. Overturning the first-instance judgment, the Court ordered the Ministry of Health "
                  "to pay compensation, applying the 'more likely than not' standard argued by the defence to date the "
                  "infection after 1958.",
        },
    },
]

AREAS = [
    {'id': 'famiglia', 'icon': 'family',
     'title': {'it': 'Diritto di famiglia', 'en': 'Family law'},
     'short': {'it': 'Separazioni, divorzi, affidamento e mantenimento dei figli.',
               'en': 'Separation, divorce, child custody and support.'},
     'lead': {'it': 'Momenti delicati, che richiedono competenza e sensibilità.',
              'en': 'Delicate moments that call for expertise and sensitivity.'},
     'body': {'it': "Lo Studio assiste i clienti nelle controversie e negli accordi che riguardano i rapporti familiari, privilegiando, ove possibile, soluzioni condivise che tutelino gli interessi di tutti, a partire da quelli dei figli, nel pieno rispetto della riservatezza.",
              'en': "The firm assists clients in disputes and agreements concerning family relationships, favouring, wherever possible, shared solutions that protect everyone's interests, starting with those of the children, with full respect for confidentiality."},
     'items': {'it': ['Separazioni consensuali e giudiziali', 'Divorzi', 'Affidamento e collocamento dei figli',
                      'Assegni di mantenimento e divorzili', 'Rapporti patrimoniali tra coniugi',
                      'Modifica delle condizioni di separazione e divorzio'],
               'en': ['Consensual and judicial separation', 'Divorce', 'Child custody and residence',
                      'Child and spousal maintenance', 'Property relations between spouses',
                      'Variation of separation and divorce terms']}},
    {'id': 'previdenziale', 'icon': 'shield',
     'title': {'it': 'Diritto previdenziale', 'en': 'Social security law'},
     'short': {'it': 'Pensioni, contributi e prestazioni previdenziali e assistenziali.',
               'en': 'Pensions, contributions, social security and welfare benefits.'},
     'lead': {'it': 'Far valere i propri diritti nei confronti degli enti previdenziali.',
              'en': 'Enforcing your rights against social security bodies.'},
     'body': {'it': "Assistenza a lavoratori, pensionati e professionisti nei rapporti con gli enti previdenziali e assistenziali, sia nella fase amministrativa sia davanti al giudice.",
              'en': "Assistance to employees, pensioners and professionals in their dealings with social security and welfare bodies, both at the administrative stage and before the courts."},
     'items': {'it': ['Pensioni e ricostruzioni contributive', 'Prestazioni di invalidità e inabilità',
                      'Indennità e prestazioni assistenziali', 'Ricorsi amministrativi', 'Contenzioso previdenziale'],
               'en': ['Pensions and contribution records', 'Disability and incapacity benefits',
                      'Allowances and welfare benefits', 'Administrative appeals', 'Social security litigation']}},
    {'id': 'recupero-crediti', 'icon': 'coins',
     'title': {'it': 'Recupero crediti', 'en': 'Debt recovery'},
     'short': {'it': 'Tutela del credito in fase stragiudiziale, giudiziale ed esecutiva.',
               'en': 'Credit protection out of court, in court and in enforcement.'},
     'lead': {'it': 'Strategie mirate per tutelare i crediti di imprese e istituti finanziari.',
              'en': 'Targeted strategies to protect the claims of businesses and financial institutions.'},
     'body': {'it': "Un ambito in cui lo Studio ha maturato una lunga esperienza al fianco di istituti bancari e società di gestione del credito: dalla prima diffida fino all'esecuzione forzata, ogni posizione viene seguita con attenzione in ogni sua fase.",
              'en': "An area in which the firm has built long-standing experience alongside banks and credit management companies: from the first formal notice to enforcement, every position is followed carefully at every stage."},
     'items': {'it': ['Diffide e attività stragiudiziale', 'Ricorsi per decreto ingiuntivo',
                      'Esecuzioni mobiliari e immobiliari', 'Pignoramenti presso terzi',
                      'Insinuazioni nelle procedure concorsuali',
                      'Gestione di posizioni per banche e società di gestione del credito'],
               'en': ['Formal notices and out-of-court recovery', 'Payment order applications',
                      'Enforcement against movable and real property', 'Garnishment proceedings',
                      'Claims in insolvency proceedings',
                      'Handling of positions for banks and credit management companies']}},
    {'id': 'immobiliare', 'icon': 'house',
     'title': {'it': 'Diritto immobiliare', 'en': 'Real estate law'},
     'short': {'it': 'Compravendite, locazioni, condominio e diritti reali.',
               'en': 'Sales, leases, condominium matters and property rights.'},
     'lead': {'it': 'Assistenza in ogni fase della vita di un immobile.',
              'en': 'Assistance at every stage in the life of a property.'},
     'body': {'it': "Dalla trattativa alla gestione delle controversie, lo Studio affianca proprietari, conduttori, condomìni e imprese in tutte le questioni legate agli immobili.",
              'en': "From negotiation to dispute resolution, the firm supports owners, tenants, condominiums and businesses in all property-related matters."},
     'items': {'it': ['Compravendite e contratti preliminari', 'Locazioni abitative e commerciali',
                      'Sfratti per morosità e finita locazione', 'Controversie condominiali',
                      'Diritti reali, servitù e divisioni', 'Tutela del possesso'],
               'en': ['Sales and preliminary contracts', 'Residential and commercial leases',
                      'Evictions for arrears and lease expiry', 'Condominium disputes',
                      'Property rights, easements and partitions', 'Protection of possession']}},
    {'id': 'societario', 'icon': 'briefcase',
     'title': {'it': 'Diritto societario', 'en': 'Corporate law'},
     'short': {'it': 'Statuti, patti parasociali, rapporti tra soci e contenzioso.',
               'en': "Articles, shareholders' agreements, shareholder relations and litigation."},
     'lead': {'it': 'Al fianco delle imprese, dalla costituzione alla gestione dei conflitti.',
              'en': 'Supporting businesses from incorporation to dispute resolution.'},
     'body': {'it': "Consulenza continuativa e assistenza giudiziale alle società e ai loro soci, con un approccio concreto e attento agli obiettivi dell'impresa.",
              'en': "Ongoing advice and litigation support for companies and their shareholders, with a practical approach focused on the goals of the business."},
     'items': {'it': ['Costituzione di società e redazione di statuti', 'Patti parasociali',
                      'Rapporti e controversie tra soci', 'Responsabilità degli amministratori',
                      'Impugnazione di delibere assembleari', 'Contenzioso societario'],
               'en': ['Incorporation and drafting of articles', "Shareholders' agreements",
                      'Relations and disputes between shareholders', "Directors' liability",
                      "Challenges to shareholders' resolutions", 'Corporate litigation']}},
    {'id': 'tributario', 'icon': 'receipt',
     'title': {'it': 'Diritto tributario', 'en': 'Tax law'},
     'short': {'it': 'Accertamenti, cartelle e contenzioso tributario.',
               'en': 'Tax assessments, payment notices and tax litigation.'},
     'lead': {'it': 'La difesa del contribuente, con rigore e competenza.',
              'en': 'Defending taxpayers with rigour and expertise.'},
     'body': {'it': "Assistenza a privati e imprese nei rapporti con l'Amministrazione finanziaria e con l'agente della riscossione, dall'esame dell'atto fino al giudizio davanti alle Corti di giustizia tributaria.",
              'en': "Assistance to individuals and businesses in their dealings with the tax authorities and the collection agency, from the review of the measure to proceedings before the Tax Courts."},
     'items': {'it': ['Avvisi di accertamento', 'Cartelle di pagamento e intimazioni',
                      'Ricorsi in primo e secondo grado', 'Istituti deflattivi del contenzioso',
                      'Sospensione degli atti impositivi'],
               'en': ['Tax assessments', 'Payment notices and demands', 'First and second instance appeals',
                      'Pre-litigation settlement procedures', 'Suspension of tax measures']}},
    {'id': 'successioni', 'icon': 'quill',
     'title': {'it': 'Successioni', 'en': 'Inheritance law'},
     'short': {'it': 'Testamenti, divisioni ereditarie e tutela dei legittimari.',
               'en': 'Wills, division of estates and protection of forced heirs.'},
     'lead': {'it': 'Proteggere il patrimonio e le volontà, di generazione in generazione.',
              'en': 'Protecting assets and wishes, from one generation to the next.'},
     'body': {'it': "Lo Studio accompagna le famiglie nella pianificazione del passaggio generazionale e le assiste quando sorgono controversie tra eredi, con equilibrio e discrezione.",
              'en': "The firm guides families in planning generational transfers and assists them when disputes arise among heirs, with balance and discretion."},
     'items': {'it': ['Redazione di testamenti', 'Pianificazione del passaggio generazionale', 'Divisioni ereditarie',
                      'Azioni a tutela dei legittimari', 'Impugnazione di testamenti', 'Controversie tra coeredi'],
               'en': ['Drafting of wills', 'Generational transfer planning', 'Division of estates',
                      'Actions to protect forced heirs', 'Challenges to wills', 'Disputes among co-heirs']}},
]

CLIENTS = {
    'it': ['Clienti istituzionali', 'Istituti bancari', 'Società di gestione del credito', 'Enti pubblici',
           'Compagnie aeree', 'Aziende di rilevanza locale e nazionale', 'Privati cittadini'],
    'en': ['Institutional clients', 'Banks', 'Credit management companies', 'Public bodies',
           'Airlines', 'Companies of local and national importance', 'Private individuals'],
}

T = {
    'it': {
        'nav.studio': 'Lo Studio', 'nav.areas': 'Aree di attività', 'nav.press': 'Rassegna stampa',
        'nav.contacts': 'Contatti', 'nav.cta': 'Contattaci', 'home': 'Home', 'menu': 'Apri il menu',
        'title.home': 'Studio Legale Mannino | Avvocati a Palermo e Roma',
        'title.areas': 'Aree di attività | Studio Legale Mannino',
        'title.press': 'Rassegna stampa | Studio Legale Mannino',
        'title.contacts': 'Contatti | Studio Legale Mannino',
        'desc.home': "Studio Legale Mannino: oltre trent'anni di assistenza in diritto civile a Palermo e Roma. Famiglia, previdenziale, recupero crediti, immobiliare, societario, tributario e successioni.",
        'desc.areas': 'Diritto di famiglia, previdenziale, recupero crediti, immobiliare, societario, tributario e successioni: le aree di attività dello Studio Legale Mannino.',
        'desc.press': 'Le vicende seguite dallo Studio Legale Mannino di cui si è occupata la stampa.',
        'desc.contacts': 'Contatti e sedi dello Studio Legale Mannino: Palermo, Via Salvatore Meccio 16, e Roma, Piazza Cavour 3. Tel. +39 091 325611.',

        'hero.eyebrow': 'Studio Legale · Palermo · Roma',
        'hero.title': 'La vostra tutela,<br><em>la nostra esperienza.</em>',
        'hero.lead': "Da oltre trent'anni lo Studio Legale Mannino affianca privati, imprese, istituti di credito ed enti pubblici nelle questioni di diritto civile, in giudizio e fuori dal giudizio.",
        'hero.cta1': 'Prenota un appuntamento', 'hero.cta2': 'Le aree di attività',
        'stat.years': "anni di attività", 'stat.areas': 'aree del diritto civile', 'stat.offices': 'sedi: Palermo e Roma',

        'studio.eyebrow': 'Lo Studio', 'studio.title': 'Radici solide, visione nazionale.',
        'studio.body': [
            "Lo Studio Legale Mannino nasce dall'esperienza dell'<strong>Avv. Manlio Mannino</strong> e opera da oltre trent'anni nel diritto civile, con sedi a Palermo e a Roma.",
            "Nel tempo lo Studio ha affiancato clienti istituzionali, istituti bancari, società di gestione del credito, enti pubblici, compagnie aeree e aziende di rilevanza locale e nazionale, senza mai perdere di vista le esigenze dei privati cittadini.",
            "Ogni incarico è seguito con metodo e attenzione, grazie a una rete di collaboratori interni ed esterni e a un dialogo diretto e costante con il cliente.",
        ],
        'studio.sign': 'Titolare dello Studio',
        'values': [
            ('award', 'Esperienza', "Oltre trent'anni di attività al fianco di privati, imprese e istituzioni."),
            ('chat', 'Rapporto diretto', 'Un dialogo chiaro e costante: il cliente sa sempre a che punto è la sua pratica.'),
            ('team', 'Squadra su misura', 'Collaboratori interni ed esterni per affrontare ogni questione con le competenze necessarie.'),
            ('pin', 'Palermo e Roma', 'Due sedi per assistere i clienti in Sicilia e sul territorio nazionale.'),
        ],

        'areas.eyebrow': 'Aree di attività', 'areas.title': 'Competenze al servizio delle vostre esigenze',
        'areas.lead': 'Consulenza e assistenza, giudiziale e stragiudiziale, nelle principali materie del diritto civile.',
        'more': 'Scopri di più',
        'areas.cta.title': 'Non trovate la vostra materia?',
        'areas.cta.text': 'Contattate lo Studio: valuteremo insieme la vostra situazione.',
        'areas.cta.more': 'Contattaci',

        'clients.eyebrow': 'Clienti', 'clients.title': 'Chi si affida allo Studio',
        'clients.lead': 'Una clientela eterogenea, pubblica e privata, assistita con la stessa cura.',

        'press.eyebrow': 'Rassegna stampa', 'press.title': 'Lo Studio sulla stampa',
        'press.lead': 'Alcune vicende seguite dallo Studio che hanno trovato spazio sui media.',
        'press.all': 'Tutta la rassegna stampa', 'press.read': "Leggi l'articolo",
        'press.empty': 'La rassegna stampa è in aggiornamento.',
        'press.note': "I titoli riportati sono quelli originali delle testate, alle quali appartengono i diritti sugli articoli. Le sintesi sono a cura dello Studio; per il testo completo si rimanda alla fonte.",
        'press.page.title': 'Rassegna stampa',
        'press.page.lead': "Le vicende seguite dallo Studio di cui si sono occupati giornali e testate online.",

        'cta.title': 'Parliamo della vostra questione.',
        'cta.text': 'Contattate lo Studio per fissare un appuntamento presso la sede di Palermo o di Roma.',
        'cta.btn': 'Tutti i contatti',

        'areas.page.title': 'Competenze in ambito civile',
        'areas.page.lead': 'Lo Studio presta consulenza e assistenza, in giudizio e fuori dal giudizio, nelle seguenti materie.',

        'contacts.page.title': 'Contatti',
        'contacts.page.lead': 'Siamo a disposizione per fissare un appuntamento presso la sede di Palermo o di Roma.',
        'office': 'Sede', 'phone': 'Telefono', 'fax': 'Fax', 'pec': 'PEC',
        'map.show': 'Mostra la mappa',
        'map.note': 'La mappa è fornita da Google Maps: cliccando, alcuni dati di navigazione verranno trasmessi a Google.',
        'map.directions': 'Indicazioni stradali',

        'footer.text': "Oltre trent'anni di assistenza legale in diritto civile per privati, imprese e istituzioni.",
        'footer.offices': 'Sedi', 'footer.contacts': 'Contatti', 'footer.explore': 'Esplora',
        'footer.vat': 'P.IVA',
        'footer.cookies': 'Questo sito non utilizza cookie propri. Le mappe di Google vengono caricate solo su richiesta.',
        'lang.label': 'Lingua',
    },
    'en': {
        'nav.studio': 'The Firm', 'nav.areas': 'Practice areas', 'nav.press': 'Press',
        'nav.contacts': 'Contacts', 'nav.cta': 'Contact us', 'home': 'Home', 'menu': 'Open menu',
        'title.home': 'Studio Legale Mannino | Lawyers in Palermo and Rome',
        'title.areas': 'Practice areas | Studio Legale Mannino',
        'title.press': 'Press | Studio Legale Mannino',
        'title.contacts': 'Contacts | Studio Legale Mannino',
        'desc.home': 'Studio Legale Mannino: over thirty years of civil law practice in Palermo and Rome. Family, social security, debt recovery, real estate, corporate, tax and inheritance law.',
        'desc.areas': 'Family, social security, debt recovery, real estate, corporate, tax and inheritance law: the practice areas of Studio Legale Mannino.',
        'desc.press': 'Cases handled by Studio Legale Mannino that have been covered by the press.',
        'desc.contacts': 'Contacts and offices of Studio Legale Mannino: Palermo, Via Salvatore Meccio 16, and Rome, Piazza Cavour 3. Tel. +39 091 325611.',

        'hero.eyebrow': 'Law firm · Palermo · Rome',
        'hero.title': 'Your protection,<br><em>our experience.</em>',
        'hero.lead': 'For over thirty years, Studio Legale Mannino has stood beside individuals, businesses, banks and public bodies in civil law matters, both in and out of court.',
        'hero.cta1': 'Book an appointment', 'hero.cta2': 'Practice areas',
        'stat.years': 'years of practice', 'stat.areas': 'areas of civil law', 'stat.offices': 'offices: Palermo and Rome',

        'studio.eyebrow': 'The Firm', 'studio.title': 'Solid roots, a national outlook.',
        'studio.body': [
            'Studio Legale Mannino is built on the experience of <strong>Avv. Manlio Mannino</strong> and has been practising civil law for over thirty years, with offices in Palermo and Rome.',
            'Over the years the firm has assisted institutional clients, banks, credit management companies, public bodies, airlines and companies of local and national importance, without ever losing sight of the needs of private individuals.',
            'Every matter is handled with method and care, thanks to a network of in-house and external collaborators and a direct, ongoing dialogue with the client.',
        ],
        'studio.sign': 'Head of the firm',
        'values': [
            ('award', 'Experience', 'Over thirty years of practice alongside individuals, businesses and institutions.'),
            ('chat', 'Direct relationship', 'Clear and constant communication: clients always know where their matter stands.'),
            ('team', 'A tailored team', 'In-house and external collaborators to handle every matter with the necessary expertise.'),
            ('pin', 'Palermo and Rome', 'Two offices serving clients in Sicily and throughout Italy.'),
        ],

        'areas.eyebrow': 'Practice areas', 'areas.title': 'Expertise tailored to your needs',
        'areas.lead': 'Advice and assistance, in and out of court, across the main areas of civil law.',
        'more': 'Learn more',
        'areas.cta.title': "Can't find your area?",
        'areas.cta.text': "Get in touch with the firm and we will assess your situation together.",
        'areas.cta.more': 'Contact us',

        'clients.eyebrow': 'Clients', 'clients.title': 'Who relies on the firm',
        'clients.lead': 'A diverse client base, public and private, assisted with the same care.',

        'press.eyebrow': 'Press', 'press.title': 'The firm in the press',
        'press.lead': 'Some of the cases handled by the firm that have been covered by the media.',
        'press.all': 'All press coverage', 'press.read': 'Read the article (in Italian)',
        'press.empty': 'Press coverage is being updated.',
        'press.note': 'Headlines are quoted in their original Italian; all rights to the articles belong to the respective publishers. Summaries are written by the firm; please refer to the source for the full text.',
        'press.page.title': 'Press',
        'press.page.lead': 'Cases handled by the firm that have been covered by newspapers and online media.',

        'cta.title': "Let's talk about your case.",
        'cta.text': 'Contact the firm to book an appointment at our Palermo or Rome office.',
        'cta.btn': 'All contacts',

        'areas.page.title': 'Civil law expertise',
        'areas.page.lead': 'The firm provides advice and assistance, both in and out of court, in the following areas.',

        'contacts.page.title': 'Contacts',
        'contacts.page.lead': 'We are available to arrange an appointment at our Palermo or Rome office.',
        'office': 'Office', 'phone': 'Phone', 'fax': 'Fax', 'pec': 'Certified email (PEC)',
        'map.show': 'Show map',
        'map.note': 'The map is provided by Google Maps: by clicking, some browsing data will be sent to Google.',
        'map.directions': 'Get directions',

        'footer.text': 'Over thirty years of civil law practice for individuals, businesses and institutions.',
        'footer.offices': 'Offices', 'footer.contacts': 'Contacts', 'footer.explore': 'Explore',
        'footer.vat': 'VAT no.',
        'footer.cookies': 'This website does not use its own cookies. Google maps are loaded only on request.',
        'lang.label': 'Language',
    },
}

MONTHS = {
    'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto',
           'settembre', 'ottobre', 'novembre', 'dicembre'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
           'September', 'October', 'November', 'December'],
}

ICONS = {
    'family': '<circle cx="9" cy="7" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17.5" cy="9.5" r="2.5"/><path d="M16 14.3c.5-.2 1-.3 1.5-.3 2.5 0 4.5 2 4.5 4.5"/>',
    'shield': '<path d="M12 3l8 3v6c0 4.8-3.4 8.3-8 9-4.6-.7-8-4.2-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'coins': '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>',
    'house': '<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-6h4v6"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    'receipt': '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9.5 17l5-6"/><circle cx="10" cy="11.5" r="1"/><circle cx="14" cy="16.5" r="1"/>',
    'quill': '<path d="M20 4c-7 0-12 5-13 12l-2 4 4-2c7-1 11-6 11-14z"/><path d="M8 16l6-6"/>',
    'award': '<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"/>',
    'chat': '<path d="M4 5h16v11H10l-5 4v-4H4z"/><path d="M8 10h8M8 13h5"/>',
    'team': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 13.8c2.1.8 3.5 2.9 3.5 5.2"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'phone': '<path d="M5 4h3.5l2 5-2.5 1.5a11 11 0 0 0 5.5 5.5l1.5-2.5 5 2V19a2 2 0 0 1-2 2C10.6 21 3 13.4 3 6a2 2 0 0 1 2-2z"/>',
    'fax': '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'external': '<path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>',
    'chev': '<path d="M6 9l6 6 6-6"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'map': '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    'news': '<path d="M4 5h13v14a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v10a2 2 0 0 1-2 2"/><path d="M8 9h5M8 13h5M8 17h3"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
}

M_PATH = open(os.path.join(HERE, 'm-path.txt')).read().strip()


def icon(name, cls='icon'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def esc(s):
    return html.escape(s, quote=True)


def rel(cur_page, cur_lang, target_page, target_lang, anchor=''):
    """Relative link from one generated page to another."""
    depth = PAGES[cur_page][cur_lang].count('/')
    return '../' * depth + PAGES[target_page][target_lang] + anchor


def fmt_date(iso, lang):
    if not iso:
        return ''
    d = datetime.date.fromisoformat(iso)
    if lang == 'it':
        return f'{d.day} {MONTHS["it"][d.month - 1]} {d.year}'
    return f'{d.day} {MONTHS["en"][d.month - 1]} {d.year}'


def initials(name):
    letters = [c for c in name if c.isupper()]
    return ''.join(letters[:2]) or name[:2].upper()


# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------
def head(page, lang):
    t = T[lang]
    a = '../' * PAGES[page][lang].count('/') + 'assets/'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(t['title.' + page])}</title>
  <meta name="description" content="{esc(t['desc.' + page])}">
  <meta name="theme-color" content="#0f1e33">
  <link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{a}fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{a}fonts/cormorant-garamond-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{a}style.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>
'''


def header(page, lang):
    t = T[lang]
    a = '../' * PAGES[page][lang].count('/') + 'assets/'
    act = lambda p: ' active' if p == page else ''
    items = '\n'.join(
        f'            <li><a href="{rel(page, lang, "areas", lang, "#" + ar["id"])}">{icon(ar["icon"])}{esc(ar["title"][lang])}</a></li>'
        for ar in AREAS)
    current = ' class="current" aria-current="true"'
    langs = ''.join(
        f'<a href="{rel(page, lang, page, l)}" hreflang="{l}" lang="{l}"{current if l == lang else ""}>{l.upper()}</a>'
        for l in LANGS)
    return f'''
  <header class="site-header">
    <div class="container header-inner">
      <a href="{rel(page, lang, 'home', lang)}" class="logo"><img src="{a}logo.svg" alt="Studio Legale Mannino" width="291" height="50"></a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}">
        <span></span><span></span><span></span>
      </button>
      <nav id="nav" class="nav">
        <a class="nav-link" href="{rel(page, lang, 'home', lang, '#studio')}">{t['nav.studio']}</a>
        <div class="dropdown">
          <a class="nav-link{act('areas')}" href="{rel(page, lang, 'areas', lang)}">{t['nav.areas']}{icon('chev', 'icon chev')}</a>
          <ul class="dropdown-menu">
{items}
          </ul>
        </div>
        <a class="nav-link{act('press')}" href="{rel(page, lang, 'press', lang)}">{t['nav.press']}</a>
        <a class="nav-link{act('contacts')}" href="{rel(page, lang, 'contacts', lang)}">{t['nav.contacts']}</a>
        <span class="lang" role="group" aria-label="{t['lang.label']}">{langs}</span>
        <a class="btn btn-dark" href="{rel(page, lang, 'contacts', lang)}">{t['nav.cta']}</a>
      </nav>
    </div>
  </header>
'''


def footer(page, lang):
    t = T[lang]
    a = '../' * PAGES[page][lang].count('/') + 'assets/'
    offices = '\n'.join(
        f'          <address><strong>{o["city"][lang]}</strong><br>{o["street"]}<br>{o["zip"]}</address>' for o in OFFICES)
    vat = f' · {t["footer.vat"]}: {VAT}' if VAT else ''
    year = datetime.date.today().year
    return f'''
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <img src="{a}logo-white.svg" alt="Studio Legale Mannino" width="256" height="44" loading="lazy">
          <p>{t['footer.text']}</p>
        </div>
        <div>
          <h4>{t['footer.offices']}</h4>
{offices}
        </div>
        <div>
          <h4>{t['footer.contacts']}</h4>
          <ul>
            <li>Tel. <a href="{PHONE_HREF}">{PHONE}</a></li>
            <li>Fax {FAX}</li>
            <li>PEC <a href="mailto:{PEC}">{PEC}</a></li>
          </ul>
        </div>
        <div>
          <h4>{t['footer.explore']}</h4>
          <ul>
            <li><a href="{rel(page, lang, 'home', lang, '#studio')}">{t['nav.studio']}</a></li>
            <li><a href="{rel(page, lang, 'areas', lang)}">{t['nav.areas']}</a></li>
            <li><a href="{rel(page, lang, 'press', lang)}">{t['nav.press']}</a></li>
            <li><a href="{rel(page, lang, 'contacts', lang)}">{t['nav.contacts']}</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© {year} Studio Legale Mannino · Avv. Manlio Mannino{vat}</span>
        <span>{t['footer.cookies']}</span>
      </div>
    </div>
  </footer>

  <script src="{a}main.js" defer></script>
</body>
</html>
'''


def cta_band(page, lang, pad_top=False):
    t = T[lang]
    return f'''
    <section class="cta-band{' pad-top' if pad_top else ''}">
      <div class="container">
        <div class="cta-box reveal">
          <div>
            <h2>{t['cta.title']}</h2>
            <p>{t['cta.text']}</p>
          </div>
          <div class="cta-actions">
            <a class="cta-phone" href="{PHONE_HREF}">{icon('phone')}{PHONE}</a>
            <a class="btn btn-gold" href="{rel(page, lang, 'contacts', lang)}">{t['cta.btn']}{icon('arrow')}</a>
          </div>
        </div>
      </div>
    </section>
'''


def press_card(p, lang, t, big=False):
    date = fmt_date(p.get('date'), lang)
    time = f'<time datetime="{p["date"]}">{date}</time>' if date else ''
    hl_lang = '' if lang == 'it' else ' lang="it"'
    inner = f'''<div class="press-meta"><span>© {esc(p['source'])}</span>{time}</div>
            <h3{hl_lang}>{esc(p['headline'])}</h3>
            <p>{esc(p['summary'][lang])}</p>
            <span class="more">{t['press.read']}{icon('external')}</span>'''
    if big:
        return f'''        <a class="press-card reveal" href="{esc(p['url'])}" target="_blank" rel="noopener">
          <div class="press-logo" aria-hidden="true">{initials(p['source'])}</div>
          <div class="press-main">
            {inner}
          </div>
        </a>'''
    return f'''        <a class="press-card reveal" href="{esc(p['url'])}" target="_blank" rel="noopener">
            {inner}
        </a>'''


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_home(lang):
    t = T[lang]
    P = 'home'
    values = '\n'.join(f'''          <div class="value reveal">{icon(i)}<h3>{h}</h3><p>{p}</p></div>''' for i, h, p in t['values'])
    cards = '\n'.join(f'''        <a class="area-card reveal" href="{rel(P, lang, 'areas', lang, '#' + ar['id'])}">
          <span class="area-icon">{icon(ar['icon'])}</span>
          <h3>{esc(ar['title'][lang])}</h3>
          <p>{esc(ar['short'][lang])}</p>
          <span class="more">{t['more']}{icon('arrow')}</span>
        </a>''' for ar in AREAS)
    chips = '\n'.join(f'          <li>{esc(c)}</li>' for c in CLIENTS[lang])
    body = '\n'.join(f'          <p>{p}</p>' for p in t['studio.body'])
    a = '../' * PAGES[P][lang].count('/') + 'assets/'

    press = ''
    if PRESS:
        pcards = '\n'.join(press_card(p, lang, t) for p in PRESS[:3])
        press = f'''
    <section class="section">
      <div class="container">
        <div class="section-head center">
          <p class="eyebrow">{t['press.eyebrow']}</p>
          <h2>{t['press.title']}</h2>
          <p class="lead">{t['press.lead']}</p>
        </div>
        <div class="press-grid">
{pcards}
        </div>
        <div class="section-foot"><a class="btn btn-dark" href="{rel(P, lang, 'press', lang)}">{t['press.all']}{icon('arrow')}</a></div>
      </div>
    </section>
'''

    return head(P, lang) + header(P, lang) + f'''
  <main>
    <section class="hero">
      <div class="container hero-grid">
        <div>
          <p class="eyebrow">{t['hero.eyebrow']}</p>
          <h1>{t['hero.title']}</h1>
          <p class="lead">{t['hero.lead']}</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="{rel(P, lang, 'contacts', lang)}">{icon('calendar')}{t['hero.cta1']}</a>
            <a class="btn btn-ghost" href="{rel(P, lang, 'areas', lang)}">{t['hero.cta2']}{icon('arrow')}</a>
          </div>
        </div>
        <div class="hero-visual" aria-hidden="true">
          <div class="hero-offset"></div>
          <div class="hero-frame"><svg viewBox="0 0 100 100"><path d="{M_PATH}"/></svg></div>
          <div class="hero-card"><img src="{a}logo-mark.svg" alt="" width="46" height="46"><div><b>Avv. Manlio Mannino</b><span>{t['studio.sign']}</span></div></div>
        </div>
      </div>
    </section>

    <div class="stats">
      <div class="container">
        <div class="stats-inner">
          <div class="stat"><span class="stat-icon">{icon('award')}</span><div><strong>30+</strong><span>{t['stat.years']}</span></div></div>
          <div class="stat"><span class="stat-icon">{icon('layers')}</span><div><strong>{len(AREAS)}</strong><span>{t['stat.areas']}</span></div></div>
          <div class="stat"><span class="stat-icon">{icon('pin')}</span><div><strong>{len(OFFICES)}</strong><span>{t['stat.offices']}</span></div></div>
        </div>
      </div>
    </div>

    <section class="section" id="studio">
      <div class="container studio-grid">
        <div class="studio-text reveal">
          <p class="eyebrow">{t['studio.eyebrow']}</p>
          <h2>{t['studio.title']}</h2>
{body}
          <div class="signature">
            <img src="{a}logo-mark.svg" alt="" width="52" height="52" loading="lazy">
            <div><strong>Avv. Manlio Mannino</strong><span>{t['studio.sign']}</span></div>
          </div>
        </div>
        <div class="values">
{values}
        </div>
      </div>
    </section>

    <section class="section section-cream">
      <div class="container">
        <div class="section-head center">
          <p class="eyebrow">{t['areas.eyebrow']}</p>
          <h2>{t['areas.title']}</h2>
          <p class="lead">{t['areas.lead']}</p>
        </div>
        <div class="areas-grid">
{cards}
        <a class="area-card cta reveal" href="{rel(P, lang, 'contacts', lang)}">
          <span class="area-icon">{icon('chat')}</span>
          <h3>{t['areas.cta.title']}</h3>
          <p>{t['areas.cta.text']}</p>
          <span class="more">{t['areas.cta.more']}{icon('arrow')}</span>
        </a>
        </div>
      </div>
    </section>

    <section class="section clients">
      <div class="container clients-grid">
        <div class="reveal">
          <p class="eyebrow">{t['clients.eyebrow']}</p>
          <h2>{t['clients.title']}</h2>
          <p class="lead">{t['clients.lead']}</p>
        </div>
        <ul class="chips reveal">
{chips}
        </ul>
      </div>
    </section>
{press}{cta_band(P, lang, pad_top=not PRESS)}  </main>
''' + footer(P, lang)


def page_hero(P, lang, eyebrow, title, lead):
    t = T[lang]
    return f'''
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="breadcrumb"><a href="{rel(P, lang, 'home', lang)}">{t['home']}</a> / {eyebrow}</nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
'''


def page_areas(lang):
    t = T[lang]
    P = 'areas'
    index = '\n'.join(f'        <li><a href="#{ar["id"]}">{icon(ar["icon"])}{esc(ar["title"][lang])}</a></li>' for ar in AREAS)
    blocks = '\n'.join(f'''        <article class="area-block reveal" id="{ar['id']}">
          <div class="area-block-head"><span class="area-icon">{icon(ar['icon'])}</span><h2>{esc(ar['title'][lang])}</h2></div>
          <p class="area-lead">{esc(ar['lead'][lang])}</p>
          <p>{esc(ar['body'][lang])}</p>
          <ul class="checklist">
{chr(10).join('            <li>' + esc(i) + '</li>' for i in ar['items'][lang])}
          </ul>
        </article>''' for ar in AREAS)
    return head(P, lang) + header(P, lang) + f'''
  <main>
{page_hero(P, lang, t['nav.areas'], t['areas.page.title'], t['areas.page.lead'])}
    <section class="section">
      <div class="container areas-layout">
        <ul class="areas-index">
{index}
        </ul>
        <div>
{blocks}
        </div>
      </div>
    </section>
{cta_band(P, lang)}  </main>
''' + footer(P, lang)


def page_press(lang):
    t = T[lang]
    P = 'press'
    if PRESS:
        content = ('      <div class="press-list">\n' + '\n'.join(press_card(p, lang, t, big=True) for p in PRESS)
                   + f'\n      </div>\n      <p class="press-note">{t["press.note"]}</p>')
    else:
        content = f'      <div class="press-empty">{icon("news")}<p>{t["press.empty"]}</p></div>'
    return head(P, lang) + header(P, lang) + f'''
  <main>
{page_hero(P, lang, t['nav.press'], t['press.page.title'], t['press.page.lead'])}
    <section class="section">
      <div class="container">
{content}
      </div>
    </section>
{cta_band(P, lang)}  </main>
''' + footer(P, lang)


def page_contacts(lang):
    t = T[lang]
    P = 'contacts'
    cards = []
    for o in OFFICES:
        fax = f"\n              <li>{icon('fax')}<span>{FAX}</span></li>" if o['main'] else ''
        lines = f'''
            <ul class="office-lines">
              <li>{icon('phone')}<a href="{PHONE_HREF}">{PHONE}</a></li>{fax}
              <li>{icon('mail')}<a href="mailto:{PEC}">{PEC}</a></li>
            </ul>'''
        cards.append(f'''        <article class="office reveal" id="{o['id']}">
          <div class="office-body">
            <span class="office-tag">{t['office']}</span>
            <h2>{o['city'][lang]}</h2>
            <address>{o['street']}<br>{o['zip']}</address>{lines}
          </div>
          <div class="map">
            <button type="button" class="map-load" data-q="{o['q']}">
              <strong>{icon('map')}{t['map.show']}</strong>
              <small>{t['map.note']}</small>
            </button>
          </div>
          <div class="office-foot"><a href="https://www.google.com/maps/dir/?api=1&amp;destination={o['q']}" target="_blank" rel="noopener">{t['map.directions']}{icon('external')}</a></div>
        </article>''')
    return head(P, lang) + header(P, lang) + f'''
  <main>
{page_hero(P, lang, t['nav.contacts'], t['contacts.page.title'], t['contacts.page.lead'])}
    <section class="section">
      <div class="container">
        <div class="offices">
{chr(10).join(cards)}
        </div>
        <div class="reach">
          <a class="reach-item reveal" href="{PHONE_HREF}"><span class="stat-icon">{icon('phone')}</span><div><small>{t['phone']}</small><strong>{PHONE}</strong></div></a>
          <div class="reach-item reveal"><span class="stat-icon">{icon('fax')}</span><div><small>{t['fax']}</small><strong>{FAX}</strong></div></div>
          <a class="reach-item reveal" href="mailto:{PEC}"><span class="stat-icon">{icon('mail')}</span><div><small>{t['pec']}</small><strong>{PEC}</strong></div></a>
        </div>
      </div>
    </section>
  </main>
''' + footer(P, lang)


BUILDERS = {'home': page_home, 'areas': page_areas, 'press': page_press, 'contacts': page_contacts}

if __name__ == '__main__':
    for page, files in PAGES.items():
        for lang in LANGS:
            path = os.path.join(ROOT, files[lang])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(BUILDERS[page](lang))
            print('wrote', files[lang])
