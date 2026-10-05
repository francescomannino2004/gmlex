#!/usr/bin/env python3
"""Generates the static pages of the site in Italian and English.

All text lives in this file. Edit it, then run:  python3 _build/build.py
Italian pages are written to the repository root, English pages to en/, French pages to fr/.
(Folders starting with "_" are not published by GitHub Pages.)
"""
import datetime
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ('it', 'en', 'fr')

# Bump when logo, CSS or JS change, so browsers fetch the new files instead of cached ones
ASSET_VERSION = '2026100502'

PAGES = {
    'home':     {'it': 'index.html',            'en': 'en/index.html',          'fr': 'fr/index.html'},
    'lawyer':   {'it': 'avvocato.html',         'en': 'en/the-lawyer.html',     'fr': 'fr/l-avocat.html'},
    'areas':    {'it': 'aree-di-attivita.html', 'en': 'en/practice-areas.html', 'fr': 'fr/domaines-de-competence.html'},
    'press':    {'it': 'rassegna-stampa.html',  'en': 'en/press.html',          'fr': 'fr/revue-de-presse.html'},
    'contacts': {'it': 'contatti.html',         'en': 'en/contacts.html',       'fr': 'fr/contact.html'},
}

FAX = '+39 091 8163003'
PEC = 'manliomannino@pecavvpa.it'
EMAIL = 'm.mannino@gmlex.com'
# Home background photo. Put the file in assets/ and fill in the credit required by its licence, e.g.
# HERO_PHOTO = {'file': 'palermo.jpg', 'credit': 'Foto: Nome Autore, CC BY-SA 4.0, via Wikimedia Commons'}
# While it is None the home shows the drawn Palermo skyline.
HERO_PHOTO = None
VAT = None  # Partita IVA (obbligatoria per legge sul sito), es. '01234567890'. Se None non viene mostrata.

OFFICES = [
    {'id': 'palermo', 'city': {'it': 'Palermo', 'en': 'Palermo', 'fr': 'Palerme'},
     'street': 'Via Salvatore Meccio, 16', 'zip': '90141 Palermo',
     'q': 'Via+Salvatore+Meccio+16,+90141+Palermo', 'main': True,
     'phone': '+39 091 325611', 'phone_href': 'tel:+39091325611'},
    {'id': 'roma', 'city': {'it': 'Roma', 'en': 'Rome', 'fr': 'Rome'},
     'street': 'Piazza Cavour, 3', 'zip': '00192 Roma',
     'q': 'Piazza+Cavour+3,+00192+Roma', 'main': False,
     'phone': '+39 06 45436820', 'phone_href': 'tel:+390645436820'},
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
            'fr': "Les avocats Manlio Mannino et Alessandro Gatto ont assisté quatre pédiatres de Palerme devant le Tribunal du travail dans une demande portant sur la rémunération de 10 euros par nouveau patient prévue par l'accord régional complémentaire de 2011, que l'autorité sanitaire locale (ASP) n'avait versée qu'une seule fois au lieu de chaque année de suivi. Le litige s'est conclu par un accord amiable avec l'ASP, conformément à la directive régionale du 30 avril 2025.",
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
            'fr': "La Cour d'appel a fait droit aux arguments des avocats Manlio Mannino et Alessandro Gatto, conseils du mari et des trois enfants d'une femme décédée des suites d'une hépatite C contractée lors de transfusions sanguines. Infirmant le jugement de première instance, la Cour a condamné le ministère de la Santé à réparer le préjudice, en appliquant le critère du « plus probable que non » soutenu par la défense pour situer la contamination après 1958.",
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
    'it': ['Istituti di credito nazionali e internazionali', 'Società di gestione del credito', 'Enti previdenziali',
           'Enti locali', 'Aziende a rilevanza pubblica', 'Compagnie aeree', 'Società italiane e straniere',
           'Curatele fallimentari', 'Privati cittadini'],
    'en': ['National and international banks', 'Credit management companies', 'Social security institutions',
           'Local authorities', 'Publicly relevant companies', 'Airlines', 'Italian and foreign companies',
           'Bankruptcy trustees', 'Private individuals'],
}

T = {
    'it': {
        'nav.studio': 'Lo Studio', 'nav.areas': 'Aree di attività', 'nav.press': 'Rassegna stampa',
        'nav.contacts': 'Contatti', 'nav.cta': 'Contattaci', 'home': 'Home', 'menu': 'Apri il menu',
        'title.home': 'GMLEX - Studio Legale Mannino | Avvocati a Palermo e Roma',
        'title.areas': 'Aree di attività | GMLEX - Studio Legale Mannino',
        'title.press': 'Rassegna stampa | GMLEX - Studio Legale Mannino',
        'title.contacts': 'Contatti | GMLEX - Studio Legale Mannino',
        'desc.home': "Studio Legale Mannino, Avv. Manlio Mannino, avvocato cassazionista: dal 1994 assistenza in diritto civile e amministrativo a Palermo e Roma. Credito e recupero crediti, procedure esecutive, previdenza, responsabilità civile, famiglia, immobiliare e altro.",
        'desc.areas': 'Credito e recupero crediti, procedure esecutive e concorsuali, previdenza e lavoro, responsabilità civile, diritto amministrativo, navigazione aerea, famiglia, immobiliare, societario, tributario, successioni e CEDU: le aree di attività dello Studio Legale Mannino.',
        'desc.press': 'Le vicende seguite dallo Studio Legale Mannino di cui si è occupata la stampa.',
        'desc.contacts': 'Contatti e sedi dello Studio Legale Mannino: Palermo, Via Salvatore Meccio 16, e Roma, Piazza Cavour 3. Tel. +39 091 325611 · +39 06 45436820.',

        'hero.eyebrow': 'Studio Legale · Palermo · Roma',
        'hero.title': 'La vostra tutela,<br><em>la nostra esperienza.</em>',
        'hero.lead': "Dal 1994 lo Studio Legale Mannino affianca istituti di credito, imprese, enti pubblici e privati nel diritto civile e amministrativo, in giudizio e fuori dal giudizio.",
        'hero.cta2': 'Le aree di attività',
        'stat.years': "anni di attività", 'stat.areas': 'aree di attività', 'stat.offices': 'sedi: Palermo e Roma',

        'studio.eyebrow': 'Lo Studio', 'studio.title': 'Radici solide, visione nazionale.',
        'studio.body': [
            "Lo Studio Legale Mannino è stato costituito dall'<strong>Avv. Manlio Mannino</strong>, avvocato cassazionista, che dal 1994 esercita la professione nel diritto civile e amministrativo, con sedi a Palermo e a Roma.",
            "Nel tempo lo Studio ha affiancato istituti di credito di primaria importanza nazionale e internazionale, società di gestione del credito, enti previdenziali, enti locali, compagnie aeree, aziende a rilevanza pubblica e società italiane e straniere, senza mai perdere di vista le esigenze dei privati cittadini.",
            "Ogni incarico è seguito con metodo e attenzione, grazie a una rete di collaboratori interni ed esterni e a un dialogo diretto e costante con il cliente.",
        ],
        'studio.sign': 'Avvocato Cassazionista',
        'values': [
            ('award', 'Esperienza', 'Dal 1994 al fianco di istituti di credito, imprese, enti e privati.'),
            ('chat', 'Rapporto diretto', 'Un dialogo chiaro e costante: il cliente sa sempre a che punto è la sua pratica.'),
            ('team', 'Squadra su misura', 'Collaboratori interni ed esterni per affrontare ogni questione con le competenze necessarie.'),
            ('pin', 'Palermo e Roma', 'Due sedi per assistere i clienti in Sicilia e sul territorio nazionale.'),
        ],

        'areas.eyebrow': 'Aree di attività', 'areas.title': 'Competenze al servizio delle vostre esigenze',
        'areas.lead': 'Consulenza e assistenza, giudiziale e stragiudiziale, in diritto civile e amministrativo.',
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

        'areas.page.title': 'Competenze in diritto civile e amministrativo',
        'areas.page.lead': 'Lo Studio presta consulenza e assistenza, in giudizio e fuori dal giudizio, nelle seguenti materie.',

        'contacts.page.title': 'Contatti',
        'contacts.page.lead': 'Siamo a disposizione per fissare un appuntamento presso la sede di Palermo o di Roma.',
        'office': 'Sede', 'phone': 'Telefono', 'fax': 'Fax', 'pec': 'PEC', 'email': 'Email',
        'map.show': 'Mostra la mappa',
        'map.note': 'La mappa è fornita da Google Maps: cliccando, alcuni dati di navigazione verranno trasmessi a Google.',
        'map.directions': 'Indicazioni stradali',

        'footer.text': 'Dal 1994 assistenza legale in diritto civile e amministrativo per istituti di credito, imprese, enti e privati.',
        'footer.offices': 'Sedi', 'footer.contacts': 'Contatti', 'footer.explore': 'Esplora',
        'footer.vat': 'P.IVA',
        'footer.cookies': 'Questo sito non utilizza cookie propri. Le mappe di Google vengono caricate solo su richiesta.',
        'lang.label': 'Lingua', 'tel': 'Tel.',
    },
    'en': {
        'nav.studio': 'The Firm', 'nav.areas': 'Practice areas', 'nav.press': 'Press',
        'nav.contacts': 'Contacts', 'nav.cta': 'Contact us', 'home': 'Home', 'menu': 'Open menu',
        'title.home': 'GMLEX - Studio Legale Mannino | Lawyers in Palermo and Rome',
        'title.areas': 'Practice areas | GMLEX - Studio Legale Mannino',
        'title.press': 'Press | GMLEX - Studio Legale Mannino',
        'title.contacts': 'Contacts | GMLEX - Studio Legale Mannino',
        'desc.home': 'Studio Legale Mannino, Avv. Manlio Mannino, Supreme Court lawyer: civil and administrative law in Palermo and Rome since 1994. Lending and debt recovery, enforcement, social security, civil liability, family, real estate and more.',
        'desc.areas': 'Lending and debt recovery, enforcement and insolvency, social security and employment, civil liability, administrative law, aviation, family, real estate, corporate, tax, inheritance and ECHR: the practice areas of Studio Legale Mannino.',
        'desc.press': 'Cases handled by Studio Legale Mannino that have been covered by the press.',
        'desc.contacts': 'Contacts and offices of Studio Legale Mannino: Palermo, Via Salvatore Meccio 16, and Rome, Piazza Cavour 3. Tel. +39 091 325611 · +39 06 45436820.',

        'hero.eyebrow': 'Law firm · Palermo · Rome',
        'hero.title': 'Your protection,<br><em>our experience.</em>',
        'hero.lead': 'Since 1994, Studio Legale Mannino has stood beside banks, businesses, public bodies and individuals in civil and administrative law, both in and out of court.',
        'hero.cta2': 'Practice areas',
        'stat.years': 'years of practice', 'stat.areas': 'practice areas', 'stat.offices': 'offices: Palermo and Rome',

        'studio.eyebrow': 'The Firm', 'studio.title': 'Solid roots, a national outlook.',
        'studio.body': [
            'Studio Legale Mannino was founded by <strong>Avv. Manlio Mannino</strong>, a lawyer admitted to the Italian Supreme Court, who has practised civil and administrative law since 1994, with offices in Palermo and Rome.',
            'Over the years the firm has assisted leading national and international banks, credit management companies, social security institutions, local authorities, airlines, publicly relevant companies and Italian and foreign businesses, without ever losing sight of the needs of private individuals.',
            'Every matter is handled with method and care, thanks to a network of in-house and external collaborators and a direct, ongoing dialogue with the client.',
        ],
        'studio.sign': 'Supreme Court lawyer (Cassazionista)',
        'values': [
            ('award', 'Experience', 'Since 1994 alongside banks, businesses, public bodies and individuals.'),
            ('chat', 'Direct relationship', 'Clear and constant communication: clients always know where their matter stands.'),
            ('team', 'A tailored team', 'In-house and external collaborators to handle every matter with the necessary expertise.'),
            ('pin', 'Palermo and Rome', 'Two offices serving clients in Sicily and throughout Italy.'),
        ],

        'areas.eyebrow': 'Practice areas', 'areas.title': 'Expertise tailored to your needs',
        'areas.lead': 'Advice and assistance, in and out of court, in civil and administrative law.',
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

        'areas.page.title': 'Civil and administrative law expertise',
        'areas.page.lead': 'The firm provides advice and assistance, both in and out of court, in the following areas.',

        'contacts.page.title': 'Contacts',
        'contacts.page.lead': 'We are available to arrange an appointment at our Palermo or Rome office.',
        'office': 'Office', 'phone': 'Phone', 'fax': 'Fax', 'pec': 'Certified email (PEC)', 'email': 'Email',
        'map.show': 'Show map',
        'map.note': 'The map is provided by Google Maps: by clicking, some browsing data will be sent to Google.',
        'map.directions': 'Get directions',

        'footer.text': 'Civil and administrative law since 1994 for banks, businesses, public bodies and individuals.',
        'footer.offices': 'Offices', 'footer.contacts': 'Contacts', 'footer.explore': 'Explore',
        'footer.vat': 'VAT no.',
        'footer.cookies': 'This website does not use its own cookies. Google maps are loaded only on request.',
        'lang.label': 'Language', 'tel': 'Tel.',
    },
}

# ---------------------------------------------------------------------------
# French
# ---------------------------------------------------------------------------
AREAS_FR = {
    'famiglia': ("Droit de la famille",
                 "Séparations, divorces, garde et entretien des enfants.",
                 "Des moments délicats, qui exigent compétence et sensibilité.",
                 "Le cabinet assiste ses clients dans les litiges et les accords relatifs aux relations familiales, en privilégiant, lorsque c'est possible, des solutions concertées qui protègent les intérêts de chacun, à commencer par ceux des enfants, dans le plein respect de la confidentialité.",
                 ["Séparations amiables et judiciaires", "Divorces", "Garde et résidence des enfants",
                  "Pensions alimentaires et prestations entre époux", "Régimes patrimoniaux entre époux",
                  "Modification des conditions de séparation et de divorce"]),
    'immobiliare': ("Droit immobilier",
                    "Ventes, baux, copropriété et droits réels.",
                    "Une assistance à chaque étape de la vie d'un bien immobilier.",
                    "De la négociation à la gestion des litiges, le cabinet accompagne propriétaires, locataires, copropriétés et entreprises dans toutes les questions liées à l'immobilier.",
                    ["Ventes et avant-contrats", "Baux d'habitation et commerciaux",
                     "Expulsions pour impayés et fin de bail", "Litiges de copropriété",
                     "Droits réels, servitudes et partages", "Protection de la possession"]),
    'societario': ("Droit des sociétés",
                   "Statuts, pactes d'associés, relations entre associés et contentieux.",
                   "Aux côtés des entreprises, de la constitution à la gestion des conflits.",
                   "Conseil continu et assistance contentieuse aux sociétés et à leurs associés, avec une approche concrète et attentive aux objectifs de l'entreprise.",
                   ["Constitution de sociétés et rédaction des statuts", "Pactes d'associés",
                    "Relations et litiges entre associés", "Responsabilité des dirigeants",
                    "Contestation des délibérations d'assemblée", "Contentieux des sociétés"]),
    'tributario': ("Droit fiscal",
                   "Redressements, avis de recouvrement et contentieux fiscal.",
                   "La défense du contribuable, avec rigueur et compétence.",
                   "Assistance aux particuliers et aux entreprises dans leurs relations avec l'administration fiscale et l'agent de recouvrement, de l'examen de l'acte jusqu'au procès devant les juridictions fiscales.",
                   ["Avis de redressement", "Avis de recouvrement et mises en demeure",
                    "Recours en première instance et en appel", "Procédures de règlement amiable",
                    "Suspension des actes d'imposition"]),
    'successioni': ("Successions",
                    "Testaments, partages successoraux et protection des héritiers réservataires.",
                    "Protéger le patrimoine et les volontés, de génération en génération.",
                    "Le cabinet accompagne les familles dans la planification de la transmission de leur patrimoine et les assiste lorsque surgissent des litiges entre héritiers, avec équilibre et discrétion.",
                    ["Rédaction de testaments", "Planification de la transmission patrimoniale",
                     "Partages successoraux", "Actions en réduction pour les héritiers réservataires",
                     "Contestation de testaments", "Litiges entre cohéritiers"]),
}
for _a in AREAS:
    if _a['id'] not in AREAS_FR:
        continue
    _t, _s, _l, _b, _i = AREAS_FR[_a['id']]
    _a['title']['fr'], _a['short']['fr'], _a['lead']['fr'], _a['body']['fr'], _a['items']['fr'] = _t, _s, _l, _b, _i

CLIENTS['fr'] = ['Établissements de crédit nationaux et internationaux', 'Sociétés de gestion de créances',
                 'Organismes de sécurité sociale', 'Collectivités locales', "Entreprises d'intérêt public",
                 'Compagnies aériennes', 'Sociétés italiennes et étrangères', 'Liquidateurs judiciaires', 'Particuliers']

T['fr'] = {
    'nav.studio': 'Le Cabinet', 'nav.areas': 'Compétences', 'nav.press': 'Presse',
    'nav.contacts': 'Contact', 'nav.cta': 'Nous contacter', 'home': 'Accueil', 'menu': 'Ouvrir le menu',
    'title.home': 'GMLEX - Studio Legale Mannino | Avocats à Palerme et Rome',
    'title.areas': 'Domaines de compétence | GMLEX - Studio Legale Mannino',
    'title.press': 'Revue de presse | GMLEX - Studio Legale Mannino',
    'title.contacts': 'Contact | GMLEX - Studio Legale Mannino',
    'desc.home': "Studio Legale Mannino, Me Manlio Mannino, avocat habilité devant la Cour de cassation : droit civil et administratif à Palerme et à Rome depuis 1994. Crédit et recouvrement, procédures d'exécution, sécurité sociale, responsabilité civile, famille, immobilier et plus.",
    'desc.areas': "Crédit et recouvrement, procédures d'exécution et collectives, sécurité sociale et travail, responsabilité civile, droit administratif, navigation aérienne, famille, immobilier, sociétés, fiscalité, successions et CEDH : les domaines de compétence du Studio Legale Mannino.",
    'desc.press': "Les affaires suivies par le Studio Legale Mannino dont la presse s'est fait l'écho.",
    'desc.contacts': 'Contact et bureaux du Studio Legale Mannino : Palerme, Via Salvatore Meccio 16, et Rome, Piazza Cavour 3. Tél. +39 091 325611 · +39 06 45436820.',

    'hero.eyebrow': "Cabinet d'avocats · Palerme · Rome",
    'hero.title': 'Votre protection,<br><em>notre expérience.</em>',
    'hero.lead': "Depuis 1994, le Studio Legale Mannino accompagne établissements de crédit, entreprises, organismes publics et particuliers en droit civil et administratif, devant les tribunaux comme en dehors.",
    'hero.cta2': 'Domaines de compétence',
    'stat.years': "années d'activité", 'stat.areas': 'domaines de compétence', 'stat.offices': 'bureaux : Palerme et Rome',

    'studio.eyebrow': 'Le Cabinet', 'studio.title': 'Des racines solides, une vision nationale.',
    'studio.body': [
        "Le Studio Legale Mannino a été fondé par <strong>Maître Manlio Mannino</strong>, avocat habilité devant la Cour de cassation italienne, qui exerce depuis 1994 en droit civil et administratif, avec des bureaux à Palerme et à Rome.",
        "Au fil des années, le cabinet a accompagné des établissements de crédit de premier plan, nationaux et internationaux, des sociétés de gestion de créances, des organismes de sécurité sociale, des collectivités locales, des compagnies aériennes, des entreprises d'intérêt public et des sociétés italiennes et étrangères, sans jamais perdre de vue les besoins des particuliers.",
        "Chaque dossier est traité avec méthode et attention, grâce à un réseau de collaborateurs internes et externes et à un dialogue direct et constant avec le client.",
    ],
    'studio.sign': 'Avocat habilité devant la Cour de cassation',
    'values': [
        ('award', 'Expérience', "Depuis 1994 aux côtés d'établissements de crédit, d'entreprises, d'organismes publics et de particuliers."),
        ('chat', 'Relation directe', 'Un dialogue clair et constant : le client sait toujours où en est son dossier.'),
        ('team', 'Une équipe sur mesure', 'Des collaborateurs internes et externes pour traiter chaque question avec les compétences nécessaires.'),
        ('pin', 'Palerme et Rome', "Deux bureaux pour accompagner les clients en Sicile et dans toute l'Italie."),
    ],

    'areas.eyebrow': 'Domaines de compétence', 'areas.title': 'Des compétences au service de vos besoins',
    'areas.lead': 'Conseil et assistance, judiciaire et extrajudiciaire, en droit civil et administratif.',
    'more': 'En savoir plus',
    'areas.cta.title': 'Vous ne trouvez pas votre domaine ?',
    'areas.cta.text': 'Contactez le cabinet : nous examinerons ensemble votre situation.',
    'areas.cta.more': 'Nous contacter',

    'clients.eyebrow': 'Clients', 'clients.title': 'Ils font confiance au cabinet',
    'clients.lead': 'Une clientèle diversifiée, publique et privée, accompagnée avec le même soin.',

    'press.eyebrow': 'Revue de presse', 'press.title': 'Le cabinet dans la presse',
    'press.lead': "Quelques affaires suivies par le cabinet dont les médias se sont fait l'écho.",
    'press.all': 'Toute la revue de presse', 'press.read': "Lire l'article (en italien)",
    'press.empty': 'La revue de presse est en cours de mise à jour.',
    'press.note': "Les titres sont cités dans leur version originale italienne ; tous les droits sur les articles appartiennent aux éditeurs respectifs. Les résumés sont rédigés par le cabinet ; pour le texte intégral, veuillez consulter la source.",
    'press.page.title': 'Revue de presse',
    'press.page.lead': "Les affaires suivies par le cabinet dont se sont fait l'écho journaux et médias en ligne.",

    'cta.title': 'Parlons de votre dossier.',
    'cta.text': 'Contactez le cabinet pour prendre rendez-vous à notre bureau de Palerme ou de Rome.',
    'cta.btn': 'Tous les contacts',

    'areas.page.title': 'Compétences en droit civil et administratif',
    'areas.page.lead': 'Le cabinet fournit conseil et assistance, devant les tribunaux comme en dehors, dans les domaines suivants.',

    'contacts.page.title': 'Contact',
    'contacts.page.lead': 'Nous sommes à votre disposition pour fixer un rendez-vous à notre bureau de Palerme ou de Rome.',
    'office': 'Bureau', 'phone': 'Téléphone', 'fax': 'Fax', 'pec': 'E-mail certifié (PEC)', 'email': 'E-mail',
    'map.show': 'Afficher la carte',
    'map.note': 'La carte est fournie par Google Maps : en cliquant, certaines données de navigation seront transmises à Google.',
    'map.directions': 'Itinéraire',

    'footer.text': "Droit civil et administratif depuis 1994 pour établissements de crédit, entreprises, organismes publics et particuliers.",
    'footer.offices': 'Bureaux', 'footer.contacts': 'Contact', 'footer.explore': 'Explorer',
    'footer.vat': 'N° TVA',
    'footer.cookies': "Ce site n'utilise pas de cookies propres. Les cartes Google ne sont chargées qu'à la demande.",
    'lang.label': 'Langue', 'tel': 'Tél.',
}

# ---------------------------------------------------------------------------
# Areas drawn from the lawyer's profile (all three languages inline)
# ---------------------------------------------------------------------------
def _area(id_, icon, title, short, lead, body, items):
    return {'id': id_, 'icon': icon, 'title': title, 'short': short, 'lead': lead, 'body': body, 'items': items}

NEW_AREAS = [
    _area('recupero-crediti', 'coins',
          {'it': 'Credito e recupero crediti', 'en': 'Lending and debt recovery', 'fr': 'Crédit et recouvrement de créances'},
          {'it': 'Gestione e recupero del credito ipotecario e chirografario, stragiudiziale e giudiziale.',
           'en': 'Management and recovery of secured and unsecured claims, out of court and in court.',
           'fr': "Gestion et recouvrement des créances hypothécaires et chirographaires, à l'amiable et en justice."},
          {'it': 'Un approccio commerciale e finanziario: contenere i costi, ottimizzare i tempi.',
           'en': 'A commercial and financial approach: containing costs, optimising timeframes.',
           'fr': 'Une approche commerciale et financière : maîtriser les coûts, optimiser les délais.'},
          {'it': "È il settore in cui lo Studio opera principalmente, al fianco di istituti di credito di primaria importanza nazionale e internazionale e di società di gestione del credito: gestione e recupero del credito ipotecario e chirografario, consulenza sulle garanzie del credito e attività di due diligence sugli asset da cartolarizzare o da acquistare.",
           'en': "This is the firm's main area of practice, alongside leading national and international banks and credit management companies: management and recovery of secured and unsecured claims, advice on credit guarantees and due diligence on assets to be securitised or acquired.",
           'fr': "C'est le principal domaine d'activité du cabinet, aux côtés d'établissements de crédit de premier plan, nationaux et internationaux, et de sociétés de gestion de créances : gestion et recouvrement des créances hypothécaires et chirographaires, conseil sur les garanties du crédit et due diligence sur les actifs à titriser ou à acquérir."},
          {'it': ['Recupero stragiudiziale e giudiziale del credito', 'Crediti ipotecari e chirografari',
                  'Decreti ingiuntivi ed esecuzioni mobiliari e immobiliari', 'Consulenza sulle garanzie del credito',
                  'Cartolarizzazioni (securitization) e asset management', 'Due diligence su crediti da cartolarizzare o acquistare'],
           'en': ['Out-of-court and judicial debt recovery', 'Secured and unsecured claims',
                  'Payment orders and enforcement against movable and real property', 'Advice on credit guarantees',
                  'Securitisation and asset management', 'Due diligence on receivables to be securitised or acquired'],
           'fr': ['Recouvrement amiable et judiciaire', 'Créances hypothécaires et chirographaires',
                  'Injonctions de payer et saisies mobilières et immobilières', 'Conseil sur les garanties du crédit',
                  "Titrisation et gestion d'actifs", 'Due diligence sur les créances à titriser ou à acquérir']}),
    _area('esecuzioni', 'gavel',
          {'it': 'Procedure esecutive e concorsuali', 'en': 'Enforcement and insolvency proceedings', 'fr': "Procédures d'exécution et collectives"},
          {'it': 'Vendite giudiziarie, curatele fallimentari e liquidazioni.',
           'en': 'Judicial sales, bankruptcy trusteeships and liquidations.',
           'fr': 'Ventes judiciaires, liquidations judiciaires et liquidations de sociétés.'},
          {'it': 'Esperienza maturata anche attraverso incarichi conferiti da tribunali e pubbliche amministrazioni.',
           'en': 'Experience gained also through appointments by courts and public authorities.',
           'fr': 'Une expérience acquise également au travers de missions confiées par les tribunaux et les administrations publiques.'},
          {'it': "L'Avv. Mannino è custode e delegato alle vendite nelle procedure esecutive immobiliari, è legale di curatele fallimentari e di società in liquidazione e ha svolto incarichi di commissario liquidatore di società cooperative.",
           'en': 'Avv. Mannino acts as custodian and delegate for judicial sales in real estate enforcement proceedings, is counsel to bankruptcy trustees and companies in liquidation, and has served as liquidator of cooperative societies.',
           'fr': 'Me Mannino est gardien et délégué aux ventes dans les procédures de saisie immobilière, avocat de liquidations judiciaires et de sociétés en liquidation, et a exercé des fonctions de liquidateur de sociétés coopératives.'},
          {'it': ['Custodia e delega alle vendite giudiziarie', 'Procedure esecutive immobiliari',
                  'Assistenza a curatele fallimentari', 'Società in liquidazione', 'Liquidazione di società cooperative'],
           'en': ['Custody and delegated judicial sales', 'Real estate enforcement proceedings',
                  'Counsel to bankruptcy trustees', 'Companies in liquidation', 'Liquidation of cooperative societies'],
           'fr': ['Garde des biens et délégation des ventes judiciaires', 'Procédures de saisie immobilière',
                  'Assistance aux liquidateurs judiciaires', 'Sociétés en liquidation', 'Liquidation de sociétés coopératives']}),
    _area('previdenziale', 'shield',
          {'it': 'Previdenza e lavoro', 'en': 'Social security and employment', 'fr': 'Sécurité sociale et droit du travail'},
          {'it': 'Assistenza agli enti previdenziali e contenzioso previdenziale e del lavoro.',
           'en': 'Counsel to social security institutions; social security and employment litigation.',
           'fr': 'Assistance aux organismes de sécurité sociale ; contentieux social et du travail.'},
          {'it': 'Al fianco di enti previdenziali, professionisti e lavoratori.',
           'en': 'Alongside social security institutions, professionals and workers.',
           'fr': 'Aux côtés des organismes de sécurité sociale, des professionnels et des salariés.'},
          {'it': "L'Avv. Mannino è legale di enti previdenziali, che assiste anche nel recupero dei crediti contributivi, e segue controversie previdenziali e di lavoro davanti al Tribunale del Lavoro.",
           'en': 'Avv. Mannino acts for social security institutions, including in the recovery of contribution claims, and handles social security and employment disputes before the Labour Court.',
           'fr': "Me Mannino est l'avocat d'organismes de sécurité sociale, qu'il assiste notamment dans le recouvrement des cotisations, et traite des litiges sociaux et du travail devant le Tribunal du travail."},
          {'it': ['Assistenza a enti previdenziali', 'Recupero di crediti contributivi', 'Contenzioso previdenziale',
                  'Controversie di lavoro', 'Compensi dei medici convenzionati'],
           'en': ['Counsel to social security institutions', 'Recovery of contribution claims', 'Social security litigation',
                  'Employment disputes', 'Fees of contracted doctors'],
           'fr': ['Assistance aux organismes de sécurité sociale', 'Recouvrement des cotisations',
                  'Contentieux de la sécurité sociale', 'Litiges du travail', 'Rémunération des médecins conventionnés']}),
    _area('responsabilita', 'scale',
          {'it': 'Responsabilità civile e risarcimento', 'en': 'Civil liability and compensation', 'fr': 'Responsabilité civile et indemnisation'},
          {'it': 'Risarcimento del danno, anche in ambito sanitario.',
           'en': 'Compensation for damage, including in healthcare.',
           'fr': 'Réparation du préjudice, y compris en matière de santé.'},
          {'it': 'Tutelare chi ha subito un danno.', 'en': 'Protecting those who have suffered harm.',
           'fr': 'Défendre ceux qui ont subi un préjudice.'},
          {'it': "Assistenza nelle azioni di risarcimento del danno, anche nei confronti della Pubblica Amministrazione, come nei casi di contagio da emotrasfusione, e nelle controversie per danni a persone e cose.",
           'en': 'Assistance in compensation claims, including against public authorities, as in cases of infection through blood transfusions, and in disputes over personal injury and property damage.',
           'fr': "Assistance dans les actions en réparation, y compris contre l'administration, comme dans les cas de contamination par transfusion sanguine, et dans les litiges relatifs aux dommages aux personnes et aux biens."},
          {'it': ['Responsabilità sanitaria', 'Danni da emotrasfusione', 'Responsabilità della Pubblica Amministrazione',
                  'Danni da rovina di edificio', 'Danno patrimoniale e non patrimoniale'],
           'en': ['Healthcare liability', 'Damage from blood transfusions', 'Liability of public authorities',
                  'Damage from building collapse', 'Pecuniary and non-pecuniary damage'],
           'fr': ['Responsabilité médicale', 'Préjudices liés aux transfusions sanguines', "Responsabilité de l'administration",
                  "Dommages causés par la ruine d'un bâtiment", 'Préjudice patrimonial et extrapatrimonial']}),
    _area('amministrativo', 'columns',
          {'it': 'Diritto amministrativo', 'en': 'Administrative law', 'fr': 'Droit administratif'},
          {'it': 'Consulenza e contenzioso per enti locali, aziende pubbliche e privati.',
           'en': 'Advice and litigation for local authorities, public companies and individuals.',
           'fr': 'Conseil et contentieux pour collectivités locales, entreprises publiques et particuliers.'},
          {'it': 'Al fianco di enti pubblici e privati nei rapporti con la Pubblica Amministrazione.',
           'en': 'Supporting public bodies and private parties in their dealings with public administration.',
           'fr': "Aux côtés des organismes publics et des particuliers dans leurs relations avec l'administration."},
          {'it': 'Lo Studio presta consulenza e attività giudiziaria in materia civile e amministrativa in favore di enti locali, aziende a rilevanza pubblica e privati.',
           'en': 'The firm provides advice and litigation services in civil and administrative matters to local authorities, publicly relevant companies and private clients.',
           'fr': "Le cabinet fournit conseil et assistance contentieuse en matière civile et administrative aux collectivités locales, aux entreprises d'intérêt public et aux particuliers."},
          {'it': ['Consulenza a enti locali', 'Contenzioso amministrativo', 'Aziende a rilevanza pubblica',
                  'Opposizione a sanzioni amministrative'],
           'en': ['Advice to local authorities', 'Administrative litigation', 'Publicly relevant companies',
                  'Challenges to administrative penalties'],
           'fr': ['Conseil aux collectivités locales', 'Contentieux administratif', "Entreprises d'intérêt public",
                  'Contestation de sanctions administratives']}),
    _area('navigazione-aerea', 'plane',
          {'it': 'Diritto della navigazione aerea', 'en': 'Aviation law', 'fr': 'Droit de la navigation aérienne'},
          {'it': 'Consulenza alle compagnie aeree su questioni contrattuali ed extracontrattuali.',
           'en': 'Advising airlines on contractual and non-contractual matters.',
           'fr': 'Conseil aux compagnies aériennes sur les questions contractuelles et extracontractuelles.'},
          {'it': 'Un settore specialistico, al fianco delle compagnie aeree.', 'en': 'A specialist field, alongside airlines.',
           'fr': 'Un domaine spécialisé, aux côtés des compagnies aériennes.'},
          {'it': 'Consulenza e attività giudiziaria in favore di compagnie aeree, italiane e straniere, nelle problematiche contrattuali ed extracontrattuali legate al trasporto aereo.',
           'en': 'Advice and litigation for Italian and foreign airlines on contractual and non-contractual issues relating to air transport.',
           'fr': 'Conseil et contentieux pour des compagnies aériennes italiennes et étrangères sur les questions contractuelles et extracontractuelles liées au transport aérien.'},
          {'it': ['Contrattualistica del trasporto aereo', 'Responsabilità contrattuale ed extracontrattuale',
                  'Contenzioso in materia di navigazione aerea'],
           'en': ['Air transport contracts', 'Contractual and non-contractual liability', 'Aviation litigation'],
           'fr': ['Contrats de transport aérien', 'Responsabilité contractuelle et extracontractuelle',
                  'Contentieux de la navigation aérienne']}),
    _area('cedu', 'globe',
          {'it': 'Diritti umani e CEDU', 'en': 'Human rights and the ECHR', 'fr': "Droits de l'homme et CEDH"},
          {'it': "Tutela contro le violazioni della Convenzione Europea dei Diritti dell'Uomo.",
           'en': 'Protection against violations of the European Convention on Human Rights.',
           'fr': "Protection contre les violations de la Convention européenne des droits de l'homme."},
          {'it': 'I diritti fondamentali, oltre i confini nazionali.', 'en': 'Fundamental rights, beyond national borders.',
           'fr': 'Les droits fondamentaux, au-delà des frontières nationales.'},
          {'it': "Esperienza in materia di Convenzione Europea dei Diritti dell'Uomo e delle Libertà Fondamentali, con riguardo all'applicazione della normativa europea in Italia e alla tutela contro le violazioni della Convenzione.",
           'en': 'Experience with the European Convention for the Protection of Human Rights and Fundamental Freedoms, concerning the application of European law in Italy and protection against violations of the Convention.',
           'fr': "Expérience en matière de Convention de sauvegarde des droits de l'homme et des libertés fondamentales, s'agissant de l'application du droit européen en Italie et de la protection contre les violations de la Convention."},
          {'it': ['Tutela contro le violazioni della CEDU', 'Applicazione della normativa europea in Italia',
                  'Diritti e libertà fondamentali'],
           'en': ['Protection against ECHR violations', 'Application of European law in Italy', 'Fundamental rights and freedoms'],
           'fr': ['Protection contre les violations de la CEDH', "Application du droit européen en Italie",
                  'Droits et libertés fondamentaux']}),
]
AREA_ORDER = ['recupero-crediti', 'esecuzioni', 'previdenziale', 'responsabilita', 'amministrativo', 'navigazione-aerea',
              'famiglia', 'immobiliare', 'societario', 'tributario', 'successioni', 'cedu']
_by_id = {a['id']: a for a in AREAS + NEW_AREAS}
AREAS = [_by_id[i] for i in AREA_ORDER]

# ---------------------------------------------------------------------------
# Lawyer profile page (from the profile and CV supplied by the firm;
# client names, case numbers and personal data are deliberately left out)
# ---------------------------------------------------------------------------
LAWYER = {
    'it': {
        'nav.lawyer': "L'Avvocato", 'title.lawyer': "Avv. Manlio Mannino | GMLEX - Studio Legale Mannino",
        'desc.lawyer': "Profilo dell'Avv. Manlio Mannino, avvocato cassazionista abilitato dal 1994: credito e recupero crediti, procedure esecutive, diritto amministrativo, navigazione aerea, CEDU.",
        'lawyer.lead': "Avvocato cassazionista, abilitato all'esercizio della professione forense dal 1994.",
        'lawyer.facts': [("Abilitazione", "1994 · Corte d'Appello di Palermo"), ('Albo dei Cassazionisti', 'dal 2012'),
                         ('Formazione', 'Laurea in Giurisprudenza, Università degli Studi di Palermo'),
                         ('Lingue', 'Italiano, Inglese'), ('Sedi', 'Palermo · Roma')],
        'lawyer.bio.title': 'Profilo',
        'lawyer.bio': [
            "Manlio Mannino è avvocato abilitato all'esercizio della professione forense dal maggio 1994. Da allora ha esercitato senza soluzione di continuità l'attività professionale, maturando una significativa esperienza nel diritto civile e nel diritto amministrativo.",
            "Oggi opera principalmente nel settore del credito immobiliare, curando la gestione e il recupero del credito ipotecario e chirografario, in sede stragiudiziale e giudiziale, in un'ottica commerciale e finanziaria volta a contenere i costi e a ottimizzare i tempi del recupero. Svolge consulenza sulle garanzie del credito (securitization e asset management) e organizza attività di due diligence per la determinazione degli asset da cartolarizzare o da acquistare, con riferimento alle diverse tipologie di credito.",
            "Ha prestato e presta tuttora assistenza a istituti di credito di primaria importanza nazionale e internazionale e a società di gestione del credito. È legale di enti previdenziali e opera per aziende a rilevanza pubblica, enti locali, società di rilievo nazionale e società straniere.",
            "Si occupa inoltre di diritto della navigazione aerea, con attività di consulenza in favore di compagnie aeree nelle problematiche contrattuali ed extracontrattuali, e ha maturato esperienza in materia di Convenzione Europea dei Diritti dell'Uomo, con riguardo all'applicazione della normativa europea in Italia e alla tutela contro le violazioni della Convenzione.",
            "È stato socio fondatore dello Studio legale associato Giaimo Mannino, operante nei settori del diritto amministrativo, bancario, civile, commerciale, del lavoro, penale e tributario, con funzioni di amministrazione, direzione e controllo.",
        ],
        'lawyer.path.title': 'Percorso e incarichi',
        'lawyer.path': [
            ('1991', "Laurea in Giurisprudenza presso l'Università degli Studi di Palermo"),
            ('1994', "Abilitazione all'esercizio della professione forense presso la Corte d'Appello di Palermo e avvio dell'attività professionale"),
            ('1994', 'Nomina a Vice Pretore Onorario'),
            ('2000 – 2006', "Commissario liquidatore di società cooperative per l'Assessorato regionale alla Cooperazione"),
            ('2008', 'Componente di commissione di esami per avvocato del Policlinico di Messina'),
            ('2012', "Iscrizione all'Albo degli avvocati abilitati al patrocinio davanti alla Corte di Cassazione"),
            ('Dal 2018', 'Custode e delegato alle vendite nelle procedure esecutive immobiliari'),
        ],
        'lawyer.more': "Il profilo dell'avvocato",
    },
    'en': {
        'nav.lawyer': 'The Lawyer', 'title.lawyer': 'Avv. Manlio Mannino | GMLEX - Studio Legale Mannino',
        'desc.lawyer': 'Profile of Avv. Manlio Mannino, Supreme Court lawyer admitted to the Bar in 1994: lending and debt recovery, enforcement, administrative law, aviation, ECHR.',
        'lawyer.lead': 'Lawyer admitted to practise before the Italian Supreme Court, member of the Bar since 1994.',
        'lawyer.facts': [('Admitted to the Bar', '1994 · Court of Appeal of Palermo'), ('Supreme Court Bar', 'since 2012'),
                         ('Education', 'Law degree, University of Palermo'),
                         ('Languages', 'Italian, English'), ('Offices', 'Palermo · Rome')],
        'lawyer.bio.title': 'Profile',
        'lawyer.bio': [
            'Manlio Mannino has been admitted to the Bar since May 1994. Since then he has practised without interruption, building significant experience in civil and administrative law.',
            'Today he works mainly in real estate lending, managing and recovering secured and unsecured claims, both out of court and in court, with a commercial and financial approach aimed at containing costs and optimising recovery times. He advises on credit guarantees (securitisation and asset management) and organises due diligence to identify the assets to be securitised or acquired across different types of credit.',
            'He has assisted, and continues to work with, leading national and international banks and credit management companies. He acts for social security institutions and works for publicly relevant companies, local authorities, national companies and foreign companies.',
            'He also practises aviation law, advising airlines on contractual and non-contractual matters, and has gained experience with the European Convention on Human Rights, concerning the application of European law in Italy and protection against violations of the Convention.',
            'He was a founding partner of the associated law firm Giaimo Mannino, active in administrative, banking, civil, commercial, employment, criminal and tax law, where he held management, direction and control functions.',
        ],
        'lawyer.path.title': 'Career and appointments',
        'lawyer.path': [
            ('1991', 'Law degree from the University of Palermo'),
            ('1994', 'Admitted to the Bar at the Court of Appeal of Palermo; start of professional practice'),
            ('1994', 'Appointed Honorary Deputy Magistrate (Vice Pretore Onorario)'),
            ('2000 – 2006', 'Liquidator of cooperative societies for the Sicilian Regional Department for Cooperation'),
            ('2008', 'Member of an examining board for lawyers at the Policlinico of Messina'),
            ('2012', 'Admitted to practise before the Italian Supreme Court of Cassation'),
            ('Since 2018', 'Custodian and delegate for judicial sales in real estate enforcement proceedings'),
        ],
        'lawyer.more': "The lawyer's profile",
    },
    'fr': {
        'nav.lawyer': "L'Avocat", 'title.lawyer': 'Me Manlio Mannino | GMLEX - Studio Legale Mannino',
        'desc.lawyer': "Profil de Me Manlio Mannino, avocat habilité devant la Cour de cassation italienne, inscrit au barreau depuis 1994 : crédit et recouvrement, procédures d'exécution, droit administratif, navigation aérienne, CEDH.",
        'lawyer.lead': 'Avocat habilité devant la Cour de cassation italienne, inscrit au barreau depuis 1994.',
        'lawyer.facts': [('Inscription au barreau', "1994 · Cour d'appel de Palerme"), ('Cour de cassation', 'habilité depuis 2012'),
                         ('Formation', 'Diplôme en droit, Université de Palerme'),
                         ('Langues', 'Italien, anglais'), ('Bureaux', 'Palerme · Rome')],
        'lawyer.bio.title': 'Profil',
        'lawyer.bio': [
            "Manlio Mannino est avocat inscrit au barreau depuis mai 1994. Depuis lors, il exerce sans interruption et a acquis une solide expérience en droit civil et en droit administratif.",
            "Il intervient aujourd'hui principalement dans le domaine du crédit immobilier, en assurant la gestion et le recouvrement des créances hypothécaires et chirographaires, à l'amiable comme en justice, dans une optique commerciale et financière visant à maîtriser les coûts et à optimiser les délais de recouvrement. Il conseille sur les garanties du crédit (titrisation et gestion d'actifs) et organise des due diligences pour déterminer les actifs à titriser ou à acquérir selon les différents types de créances.",
            "Il a assisté et collabore toujours avec des établissements de crédit de premier plan, nationaux et internationaux, ainsi qu'avec des sociétés de gestion de créances. Il est l'avocat d'organismes de sécurité sociale et intervient pour des entreprises d'intérêt public, des collectivités locales, des sociétés d'envergure nationale et des sociétés étrangères.",
            "Il pratique également le droit de la navigation aérienne, en conseillant des compagnies aériennes sur les questions contractuelles et extracontractuelles, et a acquis une expérience en matière de Convention européenne des droits de l'homme, s'agissant de l'application du droit européen en Italie et de la protection contre les violations de la Convention.",
            "Il a été associé fondateur du cabinet associé Giaimo Mannino, actif en droit administratif, bancaire, civil, commercial, du travail, pénal et fiscal, où il exerçait des fonctions d'administration, de direction et de contrôle.",
        ],
        'lawyer.path.title': 'Parcours et fonctions',
        'lawyer.path': [
            ('1991', "Diplôme en droit de l'Université de Palerme"),
            ('1994', "Inscription au barreau auprès de la Cour d'appel de Palerme et début de l'exercice professionnel"),
            ('1994', 'Nommé juge suppléant honoraire (Vice Pretore Onorario)'),
            ('2000 – 2006', 'Liquidateur de sociétés coopératives pour le département régional sicilien de la Coopération'),
            ('2008', "Membre d'un jury d'examen pour avocats du Policlinico de Messine"),
            ('2012', 'Habilitation à plaider devant la Cour de cassation italienne'),
            ('Depuis 2018', 'Gardien et délégué aux ventes judiciaires dans les procédures de saisie immobilière'),
        ],
        'lawyer.more': "Le profil de l'avocat",
    },
}
for _l in LANGS:
    T[_l].update(LAWYER[_l])

MONTHS = {
    'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto',
           'settembre', 'ottobre', 'novembre', 'dicembre'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
           'September', 'October', 'November', 'December'],
    'fr': ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
           'septembre', 'octobre', 'novembre', 'décembre'],
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
    'pec': '<path d="M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h8"/><path d="M3 7l9 6 9-6"/><path d="M16 19l2 2 4-4"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'external': '<path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>',
    'chev': '<path d="M6 9l6 6 6-6"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'map': '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    'news': '<path d="M4 5h13v14a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v10a2 2 0 0 1-2 2"/><path d="M8 9h5M8 13h5M8 17h3"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    'gavel': '<path d="M13.5 3.5l7 7"/><path d="M11 6l7 7"/><path d="M12.2 4.8l-6 6 4 4 6-6"/><path d="M8.2 12.8L2.5 18.5l3 3 5.7-5.7"/><path d="M13 21h8"/>',
    'columns': '<path d="M3 21h18"/><path d="M5 18h14"/><path d="M12 3l9 5H3z"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/>',
    'plane': '<path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'scale': '<path d="M12 3v18M7 21h10"/><path d="M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/>',
}

# Logo: the firm's M with balance and laurel (assets/logo-mark.svg, recoloured from the supplied artwork)
# is always shown in the same colours; assets/wordmark.svg holds the name next to it.


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
    return f'{d.day} {MONTHS[lang][d.month - 1]} {d.year}'


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
  <meta name="theme-color" content="#221516">
  <link rel="icon" href="{a}logo-mark.svg?v={ASSET_VERSION}" type="image/svg+xml">
  <link rel="preload" href="{a}fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{a}fonts/cormorant-garamond-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{a}style.css?v={ASSET_VERSION}">
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
      <a href="{rel(page, lang, 'home', lang)}" class="logo"><img class="logo-mark" src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="72" height="49"><img class="logo-word" src="{a}wordmark.svg?v={ASSET_VERSION}" alt="Studio Legale Mannino" width="234" height="35"></a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}">
        <span></span><span></span><span></span>
      </button>
      <nav id="nav" class="nav">
        <a class="nav-link{act('lawyer')}" href="{rel(page, lang, 'lawyer', lang)}">{t['nav.lawyer']}</a>
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
    phones = '\n'.join(f'            <li>{t["tel"]} {o["city"][lang]} <a href="{o["phone_href"]}">{o["phone"]}</a></li>' for o in OFFICES)
    year = datetime.date.today().year
    return f'''
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="footer-logo"><img class="logo-mark" src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="66" height="45" loading="lazy"><img class="logo-word" src="{a}wordmark.svg?v={ASSET_VERSION}" alt="Studio Legale Mannino" width="200" height="30" loading="lazy"></span>
          <p>{t['footer.text']}</p>
        </div>
        <div>
          <h4>{t['footer.offices']}</h4>
{offices}
        </div>
        <div>
          <h4>{t['footer.contacts']}</h4>
          <ul>
{phones}
            <li>Fax {FAX}</li>
            <li>{t['email']} <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>PEC <a href="mailto:{PEC}">{PEC}</a></li>
          </ul>
        </div>
        <div>
          <h4>{t['footer.explore']}</h4>
          <ul>
            <li><a href="{rel(page, lang, 'home', lang, '#studio')}">{t['nav.studio']}</a></li>
            <li><a href="{rel(page, lang, 'lawyer', lang)}">{t['nav.lawyer']}</a></li>
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

  <script src="{a}main.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
'''


def cta_band(page, lang, pad_top=False):
    t = T[lang]
    phones = '\n'.join(f'            <a class="cta-phone" href="{o["phone_href"]}">{icon("phone")}<span><small>{o["city"][lang]}</small>{o["phone"]}</span></a>' for o in OFFICES)
    return f'''
    <section class="cta-band{' pad-top' if pad_top else ''}">
      <div class="container">
        <div class="cta-box reveal">
          <div>
            <h2>{t['cta.title']}</h2>
            <p>{t['cta.text']}</p>
          </div>
          <div class="cta-actions">
{phones}
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

    if HERO_PHOTO:
        hero_open = (f'<section class="hero has-photo" style="--hero-photo: url(\'{a}{HERO_PHOTO["file"]}\')">\n'
                     f'      <p class="hero-credit">{esc(HERO_PHOTO["credit"])}</p>')
    else:
        hero_open = '<section class="hero">\n      <div class="hero-skyline" aria-hidden="true"></div>'

    return head(P, lang) + header(P, lang) + f'''
  <main>
    {hero_open}
      <div class="container hero-grid">
        <div>
          <p class="eyebrow">{t['hero.eyebrow']}</p>
          <h1>{t['hero.title']}</h1>
          <p class="lead">{t['hero.lead']}</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="{rel(P, lang, 'areas', lang)}">{t['hero.cta2']}{icon('arrow')}</a>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hero-offset" aria-hidden="true"></div>
          <div class="hero-frame" aria-hidden="true"><img src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="720" height="493"></div>
          <a class="hero-card" href="{rel(P, lang, 'lawyer', lang)}"><img src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="58" height="40"><div><b>Avv. Manlio Mannino</b><span>{t['studio.sign']}</span></div></a>
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
            <img src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="66" height="45" loading="lazy">
            <div><strong>Avv. Manlio Mannino</strong><span>{t['studio.sign']}</span></div>
            <a class="more" href="{rel(P, lang, 'lawyer', lang)}">{t['lawyer.more']}{icon('arrow')}</a>
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
    blocks = '\n'.join(f'''        <article class="area-block" id="{ar['id']}">
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
              <li>{icon('phone')}<a href="{o['phone_href']}">{o['phone']}</a></li>{fax}
              <li>{icon('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
              <li>{icon('pec')}<a href="mailto:{PEC}">{PEC}</a></li>
            </ul>'''
        cards.append(f'''        <article class="office" id="{o['id']}">
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
          <a class="reach-item reveal" href="mailto:{EMAIL}"><span class="stat-icon">{icon('mail')}</span><div><small>{t['email']}</small><strong>{EMAIL}</strong></div></a>
          <a class="reach-item reveal" href="mailto:{PEC}"><span class="stat-icon">{icon('pec')}</span><div><small>{t['pec']}</small><strong>{PEC}</strong></div></a>
          <div class="reach-item reveal"><span class="stat-icon">{icon('fax')}</span><div><small>{t['fax']}</small><strong>{FAX}</strong></div></div>
        </div>
      </div>
    </section>
  </main>
''' + footer(P, lang)


def page_lawyer(lang):
    t = T[lang]
    P = 'lawyer'
    a = '../' * PAGES[P][lang].count('/') + 'assets/'
    facts = '\n'.join(f'            <div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in t['lawyer.facts'])
    bio = '\n'.join(f'          <p>{esc(p)}</p>' for p in t['lawyer.bio'])
    path = '\n'.join(f'          <li><span class="tl-year">{esc(y)}</span><span class="tl-text">{esc(x)}</span></li>' for y, x in t['lawyer.path'])
    return head(P, lang) + header(P, lang) + f'''
  <main>
{page_hero(P, lang, t['nav.lawyer'], 'Avv. Manlio Mannino', t['lawyer.lead'])}
    <section class="section">
      <div class="container lawyer-grid">
        <aside class="profile-card">
          <img src="{a}logo-mark.svg?v={ASSET_VERSION}" alt="" width="140" height="96">
          <h2>Avv. Manlio Mannino</h2>
          <p class="profile-role">{t['studio.sign']}</p>
          <dl class="facts">
{facts}
          </dl>
          <a class="btn btn-dark" href="{rel(P, lang, 'contacts', lang)}">{t['nav.cta']}{icon('arrow')}</a>
        </aside>
        <div class="lawyer-main">
          <p class="eyebrow">{t['lawyer.bio.title']}</p>
{bio}
          <p class="eyebrow tl-head">{t['lawyer.path.title']}</p>
          <ol class="timeline">
{path}
          </ol>
        </div>
      </div>
    </section>
{cta_band(P, lang)}  </main>
''' + footer(P, lang)


BUILDERS = {'home': page_home, 'lawyer': page_lawyer, 'areas': page_areas, 'press': page_press, 'contacts': page_contacts}

if __name__ == '__main__':
    for page, files in PAGES.items():
        for lang in LANGS:
            path = os.path.join(ROOT, files[lang])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(BUILDERS[page](lang))
            print('wrote', files[lang])
