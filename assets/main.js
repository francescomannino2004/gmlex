(function () {
  // English translations. Italian text lives in the HTML and is the default.
  var EN = {
    'title.home': 'Studio Legale Mannino | Law firm in Palermo and Rome',
    'title.areas': 'Practice areas | Studio Legale Mannino',
    'title.contacts': 'Contacts | Studio Legale Mannino',

    'nav.home': 'Home page',
    'nav.areas': 'Practice areas',
    'nav.contacts': 'Contacts',

    'city.rome': 'Rome',
    'country': 'Italy',

    'home.tagline': 'Over thirty years of experience in civil law',
    'home.band': 'Palermo · Rome',
    'home.studio.t': 'The Firm',
    'home.studio.body':
      '<p>The law firm of <strong>Avv. Manlio Mannino</strong>, with offices in Palermo and Rome, has been practising civil law for over thirty years, providing advice and assistance both in and out of court.</p>' +
      '<p>Over the years the firm has assisted institutional clients, banks, credit management companies, public bodies, airlines and companies of local and national importance, as well as private individuals.</p>' +
      '<p>Its main areas of practice include family law, social security law, debt recovery, real estate law, corporate law, tax law and inheritance law.</p>' +
      '<p>The firm works with both in-house and external collaborators, allowing each matter to be handled with care and continuity, while maintaining a direct relationship between lawyer and client.</p>',

    'areas.intro': 'The firm provides advice and assistance, both in and out of court, in civil law matters in the following areas.',

    'area.famiglia.t': 'Family law',
    'area.famiglia.d': 'The firm assists clients in disputes and agreements concerning family relationships: consensual and judicial separations, divorce, child custody and support, spousal maintenance and the settlement of property relations between spouses. Wherever possible, particular attention is paid to reaching agreed solutions, while respecting the privacy of those involved.',
    'area.previdenziale.t': 'Social security law',
    'area.previdenziale.d': 'Assistance in disputes with social security and welfare bodies concerning pensions, contributions, disability benefits and allowances, both at the administrative stage and before the courts.',
    'area.recupero-crediti.t': 'Debt recovery',
    'area.recupero-crediti.d': 'Management of debt recovery both out of court and in court: formal notices, applications for payment orders (decreti ingiuntivi), enforcement proceedings against movable and real property, and claims in insolvency proceedings. The firm has long-standing experience in assisting banks and credit management companies.',
    'area.immobiliare.t': 'Real estate law',
    'area.immobiliare.d': 'Advice and litigation concerning property sales, residential and commercial leases, eviction proceedings, condominium matters, rights in rem, partitions and protection of possession.',
    'area.societario.t': 'Corporate law',
    'area.societario.d': 'Assistance to companies throughout their corporate life: drafting and reviewing articles of association and shareholders’ agreements, relations between shareholders, directors’ liability and corporate litigation.',
    'area.tributario.t': 'Tax law',
    'area.tributario.d': 'Assistance in tax litigation before the first and second instance Tax Courts, concerning tax assessments, payment notices and collection measures, as well as in evaluating the procedures available to settle disputes without litigation.',
    'area.successioni.t': 'Inheritance law',
    'area.successioni.d': 'Advice on succession matters: drafting of wills, generational transfer planning, division of estates, actions to protect forced heirs and disputes among co-heirs.',

    'map.show': 'Show map',
    'map.note': 'The map is provided by Google Maps: by clicking, data will be transmitted to Google.',
    'map.directions': 'Get directions →',
    'contacts.note': 'For any information or to book an appointment, please contact the firm on <a href="tel:+39091325611">+39 091 325611</a> or by certified email (PEC) at <a href="mailto:manliomannino@pecavvpa.it">manliomannino@pecavvpa.it</a>.',

    'footer.addr': 'Palermo: Via Salvatore Meccio, 16 – 90141 · Rome: Piazza Cavour, 3 – 00192',
    'footer.vat': 'VAT no.: to be added',
    'footer.note': 'This website is for information purposes only. It does not use its own cookies; Google maps are loaded only on request.'
  };

  var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-i18n]'));
  var original = nodes.map(function (n) { return n.innerHTML; });

  function setLang(lang) {
    nodes.forEach(function (n, i) {
      var key = n.getAttribute('data-i18n');
      var html = lang === 'en' && EN[key] != null ? EN[key] : original[i];
      if (n.tagName === 'TITLE') n.textContent = html; else n.innerHTML = html;
    });
    document.documentElement.lang = lang;
    try { localStorage.setItem('lang', lang); } catch (e) {}
  }

  var initial = 'it';
  var param = /[?&]lang=(it|en)\b/.exec(location.search);
  if (param) initial = param[1];
  else { try { if (localStorage.getItem('lang') === 'en') initial = 'en'; } catch (e) {} }
  if (initial === 'en') setLang('en');

  document.querySelector('.lang-switch').addEventListener('click', function () {
    setLang(document.documentElement.lang === 'en' ? 'it' : 'en');
  });

  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  toggle.addEventListener('click', function () {
    toggle.setAttribute('aria-expanded', nav.classList.toggle('open'));
  });

  // Maps load only on click, so nothing is sent to Google before the visitor asks
  document.querySelectorAll('.map-load').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = 'https://maps.google.com/maps?q=' + btn.getAttribute('data-q') + '&z=16&output=embed';
      iframe.title = 'Google Maps';
      iframe.loading = 'lazy';
      iframe.referrerPolicy = 'no-referrer-when-downgrade';
      btn.replaceWith(iframe);
    });
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
