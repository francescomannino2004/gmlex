# Data Analysis Module I (Data Lab for Entrepreneurship) (21072)

- Docenti: Breschi · Gagliardi (TA: Bhagwat)
- Ambito d'esame: Part I Python/pandas (notebook) + Part II econometria (slide + Hill-Griffiths-Lim). L'esame si concentra sulla teoria della prima parte di ogni sessione e sulle slide.
- Esame: Esame scritto (Blackboard + Respondus, 1h30) — data: da definire
- Formato: Domande aperte, chiuse e multiple choice: metodi econometrici, interpretazione dei risultati, applicazione a problemi di business. Senza AI.
- Valutazione: 60% esame scritto; 40% group project PitchBook (presentazione ~25 min)

## Programma (syllabus)

| N. | Data | Argomento | Stato | Appunti disponibili |
|---|---|---|---|---|
| 1 | 2026-09-07 | Intro + Python recap | da esame | nessuna registrazione |
| 2 | 2026-09-11 | Pandas DataFrames | da esame | nessuna registrazione |
| 3 | 2026-09-14 | Pandas: subset, add, remove data | da esame | nessuna registrazione |
| 4 | 2026-09-21 | Pandas: cleaning data, missing | da esame | nessuna registrazione |
| 5 | 2026-09-25 | Pandas: grouping data | da esame | nessuna registrazione |
| 6 | 2026-09-28 | Pandas: merging data | da esame | nessuna registrazione |
| 7 | 2026-10-02 | Pandas: working with text | da esame | nessuna registrazione |
| 8 | 2026-10-05 | Nature of econometric data | da esame | nessuna registrazione |
| 9 | 2026-10-09 | Descriptive Analysis | da esame | Data Analysis 9-10 |
| 10 | 2026-10-12 | Linear regression model (1) | da esame | Data Analysis 12-10, Data Analysis 12-10 |
| 11 | 2026-10-16 | Linear regression model (2): logs, quadratics, interactions | da esame | Data Analysis 16-10 |
| 12 | 2026-10-30 | Hypothesis testing | da esame | nessuna registrazione |
| 13 | 2026-11-02 | Further specification issues | da esame | nessuna registrazione |
| 14 | 2026-11-06 | Binary dependent variables | da esame | nessuna registrazione |
| 15 | 2026-11-09 | Data lab / Guest speaker | data lab | nessuna registrazione |
| 16 | 2026-11-13 | Data lab / Guest speaker | data lab | nessuna registrazione |
| 17 | 2026-11-16 | Data lab / Guest speaker | data lab | nessuna registrazione |
| 18 | 2026-11-23 | Data lab / Guest speaker | data lab | nessuna registrazione |
| 19 | 2026-11-27 | Final presentations | lavoro di gruppo | nessuna registrazione |
| 20 | 2026-11-30 | Final presentations | lavoro di gruppo | nessuna registrazione |
| 21 | 2026-12-04 | Final presentations | lavoro di gruppo | nessuna registrazione |

## Appunti delle lezioni (dalle registrazioni Wispr Flow)

### Data Analysis 9-10 — Descriptive Analysis (caso Etiopia)
_Data: 2026-10-09 · Argomento del syllabus 9: Descriptive Analysis_

Descriptive analysis for econometrics: distributions, central tendency, dispersion, outliers, correlation, and common pitfalls, illustrated with an Ethiopia technology-adoption study.

#### Course Format and Exam
- **Exam questions will focus on theory covered in the first part of each session and on the slides.**
- Second part of each session uses a continuing case developed across classes with different methodologies.
- Project must show descriptive patterns and key variable distributions before any regression.

#### Distributions and Summary Metrics
- Descriptive analysis summarizes central tendency, variability, and correlations; it is the first step of any analysis.
- Distribution types: normal, skewed (e.g. funding is right skewed), uniform, and bimodal (signals subgroups).
    - Mean below median in negative skew, above in positive skew; gap signals outliers
- Rule of thumb: need more than 100 observations for a simple linear regression.
- No variability means no information: regressions cannot uncover relationships without variation in X or Y.
    - Highly skewed variables can be log-transformed to plot more readably

#### Outliers and Use of AI Tools
- Outliers can be data errors (e.g. negative R&D), rare real phenomena, or data manipulation and fabrication.
- Dropping or recoding outliers is an assumption that must be justified; dropping top-funded firms distorts results.
- Scatter plots reveal outliers better than histograms.
- Students must be able to verify and correct AI analysis; undeclared fabricated data is an ethical and legal issue.

#### Correlation and Common Mistakes
- Correlation can be positive, negative, or none; only statistically significant correlations are credible.
- Cross-tabulation example: most tech startups founded by males, with variation by industry.
- Pitfalls: truncated axes, outlier-driven analysis, pie charts not summing to 100, and **confusing correlation with causality**.

#### Ethiopia Technology Adoption Case
- UN-funded panel of about 1,000 rural households in Ethiopia, surveyed every two years from 2013 to 2021.
- 65% adopted new technologies, but mostly crop changes; water harvesting adoption was below 5%.
- Newborn gender acted as a natural experiment: families with sons were about 3 to 3.5% more likely to adopt.
- Mechanism: daughters expected to marry and relocate, so families avoided long-term investments without a male heir.

### Data Analysis 12-10 — Linear regression model (1)
_Data: 2026-10-12 · Argomento del syllabus 10: Linear regression model (1)_

Introduction to regression analysis: model structure, coefficient interpretation, key assumptions (exogeneity, homoskedasticity), reading regression tables and hypothesis testing.

#### Regression Fundamentals
- Regression estimates the average of y conditional on x via an intercept and slope; individuals deviate by their error term
- A good project question fits in two lines and names the dependent and main independent variable
- Simple model assumes constant returns; non-linearities come next class
    - Theory, not the regression, should drive what goes into the model
- Intercept is average y when all x equal 0; slope is change in y from a unitary increase in x

#### Key Assumptions and Bias
- **Zero conditional mean (exogeneity)**: x must be uncorrelated with the error term to make causal claims
    - Ability bias in wage on education is the classic violation
    - Omitted variables uncorrelated with x do not bias causal estimates
- Sample selection can make estimates differ from the population; observations should be independent
- Residual plot of food expenditure shows heteroskedasticity; **always run regressions with robust standard errors**

#### Reading Output and Hypothesis Testing
- OLS minimizes the sum of squared residuals; tables report coefficient, standard error, t-statistic, p-value
- Food example: 100 dollar increase in weekly income linked to 10.21 dollars more food spending; intercept 83.42
    - **Check variable scale (hundreds of dollars), a typical exam trap**
- Default test is H0: beta = 0; alpha conventionally 0.05; say 'reject' or 'fail to reject', never 'accept'
    - p-value 0.062: significant at 10% not 5%; t-stat rule of thumb about 2 (2.06) at 5%
- Type I error controlled by alpha; Type II reduced only through more observations and power

#### Multiple Regression
- Adding regressors removes confounders from the error term; coefficients read holding other variables fixed (ceteris paribus)

### Data Analysis 12-10 — Caso: numero di co-founder e fondi raccolti
_Data: 2026-10-12 · Argomento del syllabus 10: Linear regression model (1)_

Class review of the co-founder team-size case: the founders effect on total raised is significant but explains little variation, and employees and deals are bad regressors to exclude.

#### Case Goal and Sample
- Question: recommend a formal team-size bonus, no formal role, or a weak secondary role for applicants with more founders
- Co-founders lost significance once many other factors were added
- Sample limited to accelerator startups; about 1,507 observations after missings

#### Theoretical Expectations
- Expected positive effect: more founders bring heterogeneous skills and competencies
- But theory is ambiguous: coordination, communication and conflict costs offset the benefits; data decides which dominates

#### Simple Regression Results
- Intercept about 4.1 million: predicted funding for a startup with 0 founders
- Each additional founder raises average total raised by about 7.04 million, p-value 0.001, significant at 1%
- **R-squared is very low (about 0.88%)**: founders are significant but explain little of funding variation
- Estimates must report robust standard errors

#### Multiple Regression and Controls
- Adding years since 2012 leaves the founders coefficient stable; its own coefficient is about −4
    - Likely captures liability of youth: younger firms had less time to raise money
- Toggling regressors on/off is normally the golden rule, but here employees and deals are **bad controls**:
    - Employees likely measured after funding: **reverse causality**
    - Deals determined simultaneously with total raised: **simultaneity bias**

### Data Analysis 16-10 — Linear regression (2): log, quadratici, interazioni + Stata
_Data: 2026-10-16 · Argomento del syllabus 11: Linear regression model (2): logs, quadratics, interactions_

Modeling nonlinearities (logs, quadratic terms) and interaction terms, followed by a Stata crash course on the PitchBook startup database.

#### Using AI Coding Tools
- Don't fully outsource analysis to AI; use it alongside Stata for support and validation.
- In a past exercise an AI tool silently cut about 300 observations, invalidating a student's regressions.
    - Always check observation counts and be able to trace each step of the code

#### Logarithmic Transformations
- Nonlinearities are added via variable transformations or extra terms, keeping the model linear in parameters.
- **Interpretation: log-log = elasticity (% change in y for 1% change in x); log-level: multiply β by 100 (% change in y for a unit change in x); level-log: divide β by 100 (unit change in y for 1% change in x).**
    - Example: level-log food model coefficient 132 means 1% more income adds about 1.32 in food spending
- Use logs for skewed continuous or many-valued integer variables; avoid for few-value units, percentages, negatives.
    - With meaningful zeros (e.g. total raised), use log(1 + x)
- **Interpretation of transformed coefficients will be on the exam**; always use the natural log.

#### Quadratic and Interaction Terms
- Quadratic terms test U-shaped or inverted U-shaped relations; the linear term must always be included.
    - Turning point: x* = −β1 / (2·β2)
- Housing price vs. square meters is usually U-shaped in data, driven by the luxury segment after the turning point.
- Interaction terms test moderation by a third variable; baseline variables must stay in the regression.
- With an interaction, each baseline coefficient is the effect when the other interacted variable equals zero.
    - Wage example: education 9.4%, experience 0.6%, negative interaction term

#### Stata Crash Course (PitchBook Database)
- Data checks: describe, count, list, codebook, duplicates, tabulate with missing; company ID has no missings or duplicates.
    - Accelerator dummy missings recoded to 0, keeping about 57,000 firms instead of 22,000
- Descriptives: summarize (detail), bysort, histograms, kernel density, box plots, scatter plots, encode, bar and pie charts.
- Regressions: robust SE, estimates store, residual plots, test, log specs, quadratic turning point, margins.
    - Use `##` to include interaction plus baseline terms automatically; `#` adds only the interaction

### Data Analysis 15-10 — 2° TA meeting progetto (syndication e failure)
_Data: 2026-10-15 · Argomento del syllabus 0: Progetto di gruppo: incontri con la TA_

TA check-in on the group's VC syndication project: the research question was reframed around startup survival, and the TA gave guidance on round comparison, failure definition, missing data, and dataset construction.

#### Research Question
- Question: among VC-backed US startups, is syndicate size (number of investors) related to failure after early rounds?
- "Risk perception" is unmeasurable; reframe as startup survival or likelihood of going out of business.

#### Comparing Financing Rounds
- Compare startups by deal type stage (Seed, early, later), not by chronological round number.
    - PitchBook only records raises above about 10k, so earlier rounds may be missing
- Syndication expected to matter more in early stages; later stages carry less risk.

#### Failure Definition and Missing Data
- Business status date and ownership status date may not reflect actual failure dates, but no better option exists.
- Open question: measure failure within a fixed window (24 or 36 months) via survival analysis.
- About 18% of completed VC rounds lack a deal ID and cannot be merged across files; selection bias handled through controls.
- 26% of deals lack investor info, 10% lack financing dates.

#### Dataset Construction and Regression
- Start from the company file (founded year, industry, number of founders, HQ country), then merge deals on company ID.
- Don't restrict the sample upfront: define non-negotiable variables, build a general dataset, and cut later.
- Syndication is the independent variable, failure the dependent; other variables enter as controls.

#### Decisions Made
- Failure = bankruptcy or out of business in either ownership status or business status.
- Rounds without a deal ID are dropped; deals missing financing dates are excluded.

## Banca domande di esercizio (con soluzioni: NON mostrarle prima che lo studente risponda)

### Domande — Data Analysis 9-10 — Descriptive Analysis (caso Etiopia)
1. [Scelta multipla] In una distribuzione asimmetrica positiva (right-skewed) come i fondi raccolti dalle startup: — Opzioni: A) Media > mediana | B) Media < mediana | C) Media = mediana | D) La mediana non esiste — Soluzione: A. Pochi valori molto alti spostano la media verso destra. Il gap media-mediana segnala outlier.
2. [Scelta multipla] Cosa fare con gli outlier? — Opzioni: A) Eliminarli sempre | B) Indagarli: possono essere errori, fenomeni rari reali o manipolazioni; ogni eliminazione/ricodifica è un'assunzione da giustificare | C) Ignorarli | D) Sostituirli con la media — Soluzione: B. Eliminare le startup più finanziate distorce i risultati. Gli scatter plot li mostrano meglio degli istogrammi.
3. [Scelta multipla] Cosa segnala una distribuzione bimodale? — Opzioni: A) Errore nei dati | B) La presenza di sottogruppi | C) Normalità | D) Eteroschedasticità — Soluzione: B. Altri tipi: normale, asimmetrica, uniforme.
4. [Aperta] Nel caso Etiopia, perché il genere del neonato è un 'esperimento naturale' e qual è il meccanismo trovato? — Traccia di soluzione: Il genere del figlio è casuale (esogeno) rispetto alle caratteristiche della famiglia, quindi isola l'effetto causale. Famiglie con figli maschi erano ~3-3,5% più propense ad adottare nuove tecnologie: le figlie ci si aspetta che si sposino e si trasferiscano, quindi senza erede maschio le famiglie evitano investimenti di lungo periodo (es. water harvesting).
5. [Aperta] Elenca almeno quattro errori comuni nell'analisi descrittiva. — Traccia di soluzione: Assi troncati (fanno sembrare grandi differenze piccole), analisi trainate dagli outlier, grafici a torta che non sommano a 100, confondere correlazione con causalità, considerare correlazioni non statisticamente significative, troppe poche osservazioni (servono >100 per una regressione semplice), variabili senza variabilità.

### Domande — Data Analysis 12-10 — Linear regression model (1)
1. [Scelta multipla] Cosa richiede l'assunzione di zero conditional mean (esogeneità)? — Opzioni: A) Che x abbia media zero | B) Che x sia incorrelata con il termine di errore | C) Che gli errori abbiano varianza costante | D) Che y sia normale — Soluzione: B. Violazione classica: ability bias nella regressione del salario sull'istruzione. Varianza costante = omoschedasticità.
2. [Scelta multipla] p-value = 0,062. Con α = 5%: — Opzioni: A) Si rifiuta H0 | B) Non si rifiuta H0 (fail to reject); è significativo solo al 10% | C) Si accetta H0 | D) Il coefficiente è zero — Soluzione: B. Non si dice mai 'accettare' H0.
3. [Scelta multipla] Food = 83,42 + 10,21 × income, con income in centinaia di dollari. Interpretazione corretta? — Opzioni: A) +1$ di reddito → +10,21$ di spesa alimentare | B) +100$ di reddito settimanale → +10,21$ di spesa alimentare | C) +10,21% di spesa per ogni 1% di reddito | D) Il reddito non influisce — Soluzione: B. Trappola tipica d'esame: controllare l'unità di misura delle variabili.
4. [Scelta multipla] Come si riduce l'errore di II tipo? — Opzioni: A) Abbassando α | B) Aumentando le osservazioni e la potenza del test | C) Usando errori standard robusti | D) Non si può ridurre — Soluzione: B. L'errore di I tipo è controllato da α.
5. [Aperta] Perché usare sempre gli errori standard robusti? Come ti accorgi del problema guardando i residui? — Traccia di soluzione: Perché con eteroschedasticità (varianza dell'errore non costante, es. spesa alimentare più variabile ai redditi alti) gli SE classici sono sbagliati e quindi t-stat e p-value non sono affidabili; i robusti correggono. Si vede dal residual plot: la dispersione dei residui si allarga (forma a imbuto) al crescere di x.

### Domande — Data Analysis 12-10 — Caso: numero di co-founder e fondi raccolti
1. [Scelta multipla] Il coefficiente dei founder è significativo all'1% ma l'R² è 0,88%. Cosa significa? — Opzioni: A) Il modello è sbagliato | B) L'effetto è statisticamente significativo ma il numero di founder spiega pochissima variazione dei fondi raccolti | C) L'effetto non esiste | D) Bisogna eliminare l'intercetta — Soluzione: B. Significatività e capacità esplicativa sono cose diverse.
2. [Scelta multipla] Perché il numero di dipendenti è un 'bad control' nella regressione dei fondi raccolti? — Opzioni: A) Ha troppi missing | B) Reverse causality: probabilmente misurato dopo il funding, quindi causato dai fondi | C) È una dummy | D) È collineare con l'anno — Soluzione: B. Il numero di deal invece è determinato simultaneamente al totale raccolto: simultaneity bias.
3. [Aperta] Interpreta il coefficiente di 'years since 2012' (~ −4) e spiega perché il coefficiente dei founder resta stabile aggiungendolo. — Traccia di soluzione: Ogni anno di fondazione più recente è associato a ~4 milioni in meno raccolti, a parità di founder: cattura la 'liability of youth' (le imprese più giovani hanno avuto meno tempo per raccogliere). Il coefficiente dei founder è stabile perché l'anno non è (molto) correlato col numero di founder, quindi non era un confondente rilevante.

### Domande — Data Analysis 16-10 — Linear regression (2): log, quadratici, interazioni + Stata
1. [Scelta multipla] Modello log-level: ln(y) = β0 + 0,05·x. Interpretazione? — Opzioni: A) +1 unità di x → +0,05 unità di y | B) +1 unità di x → circa +5% di y | C) +1% di x → +0,05% di y | D) +1% di x → +0,05 unità di y — Soluzione: B. Log-level: β×100 = variazione % di y per unità di x. Log-log = elasticità. Level-log: β/100 = variazione in unità di y per +1% di x.
2. [Scelta multipla] Level-log: food = β0 + 132·ln(income). Interpretazione? — Opzioni: A) +1% di reddito → +1,32 di spesa alimentare | B) +1% di reddito → +132 di spesa | C) +1 di reddito → +132% | D) Elasticità pari a 132 — Soluzione: A. β/100 = 1,32.
3. [Scelta multipla] Quando NON usare il logaritmo? — Opzioni: A) Per variabili continue asimmetriche | B) Per variabili con pochi valori, percentuali, valori negativi | C) Per i fondi raccolti con zeri (usa ln(1+x)) | D) Per il reddito — Soluzione: B. Con zeri significativi si usa log(1+x); si usa sempre il logaritmo naturale.
4. [Scelta multipla] In Stata, cosa fa `reg y c.educ##c.exper`? — Opzioni: A) Include solo l'interazione | B) Include educ, exper e la loro interazione | C) Esegue due regressioni separate | D) Calcola la correlazione — Soluzione: B. `##` include interazione + termini base; `#` solo l'interazione. I termini base devono restare nel modello.
5. [Aperta] y = β0 + β1·x + β2·x². Con β1 = 4 e β2 = −0,1 che forma ha la relazione e dov'è il turning point? Perché il termine lineare va sempre incluso? — Traccia di soluzione: β2 < 0 → U rovesciata. Turning point x* = −β1/(2β2) = −4/(2×−0,1) = 20. Il termine lineare va sempre incluso perché senza di esso si impone che il vertice sia a x = 0, vincolando arbitrariamente la forma.
6. [Aperta] Con un termine di interazione educ×exper, come si interpreta il coefficiente di educ da solo? — Traccia di soluzione: È l'effetto dell'istruzione quando exper = 0 (non un effetto medio). L'effetto marginale dell'istruzione è β_educ + β_inter × exper: con interazione negativa, il rendimento dell'istruzione diminuisce al crescere dell'esperienza.

### Domande — Data Analysis 15-10 — 2° TA meeting progetto (syndication e failure)
1. [Aperta] Riassumi la domanda di ricerca del tuo progetto, la definizione di failure scelta e le principali decisioni sul dataset. — Traccia di soluzione: Tra le startup USA VC-backed, la dimensione del sindacato (numero di investitori) è legata al fallimento dopo i primi round? Failure = bankruptcy o out of business in ownership status o business status. Si confrontano i round per deal type stage (seed, early, later), non per numero cronologico. Si parte dal company file e si fa merge dei deal su company ID; si droppano round senza deal ID e deal senza data di finanziamento; non restringere il campione all'inizio. Syndication = variabile indipendente, failure = dipendente, altre variabili come controlli.

## Materiali dei docenti

### syllabus-data-analysis.pdf (reading)

[Pagina 1]
SYLLABUS 2026/2027
21072 DATA ANALYSIS MODULE I (DATA LAB FOR
ENTREPRENEURSHIP)
Classe impartita in lingua inglese
Programs: INTENT (8 crediti - I sem. - OB | 8 cfu - ECON-04/A)
Class: 27 (I sem.)
Department: Management and Technology
Course director: STEFANO BRESCHI
Classe 27
RUJUTA SHIRISH BHAGWAT
Department of Management and Technology
Università Bocconi, Milan, Italy
rujuta.bhagwat@unibocconi.it
STEFANO BRESCHI
Department of Management and Technology
Università Bocconi, Milan, Italy
stefano.breschi@unibocconi.it
LUISA GAGLIARDI
Department of Management and Technology
Università Bocconi, Milan, Italy
luisa.gagliardi@unibocconi.it
Attenzione! Il programma di seguito riportato è da considerarsi valido SOLO per l'anno accademico 2026/2027.
MISSION
This course aims to provide students with a strong foundation in the principles and techniques
of data analysis and econometric modeling. The first part will cover topics such as data
manipulation, data visualization, and statistical analysis using Python, one of the most popular
programming languages. In this part of the course, students will learn how to write efficient and
effective code to analyze and interpret data and will develop the ability to communicate their
findings in a clear and concise manner. The second part of the course will cover statistical
inference and regression analysis. Students will learn how to apply these techniques to real-
world data sets and will develop the skills necessary to interpret and communicate their findings
effectively. Throughout the course, a special emphasis will be put on the importance of critical
thinking and problem-solving in the field of data analysis and econometrics. By the end of the
course, students will be equipped with the knowledge and skills necessary to conduct rigorous
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 1/9

[Pagina 2]
SYLLABUS 2026/2027
data analysis and econometric modeling in a variety of contexts in their future academic or
professional pursuits.
COURSE CONTENT DETAILED - SCHEDULE
- INTENT cl. 27
In today’s data-driven landscape, understanding the dynamics of high-tech ventures requires
mastery of complex, multi-source datasets and advanced analytical tools. This course
empowers students to streamline and reshape raw startup ecosystem data—from fundraising
rounds to performance metrics—into robust, analysis-ready formats. Through hands-on labs in
Python and Stata, students will develop reproducible pipelines for data cleaning, integration,
and visualization, then apply core econometric techniques (OLS, IV, panel models) to test
hypotheses on growth, valuation, and investment trends. Throughout the lab, we emphasize
critical thinking and problem-solving as essential skills for navigating complex data workflows
and econometric challenges. By the end of the course, students will be fully prepared to carry
out robust data transformations and econometric analyses across a range of academic and
professional settings.
Class group 27 — INTENT — Breschi S. / Gagliardi L. — 10:15-12:45, Room N39, Sraffa 13 (3rd
floor)
# Day Date Time Room Topic
1 Monday 07-Sep 10:15 - 12:45 N39 Intro + Python
recap
2 Friday 11-Sep 10:15 - 12:45 N39 Pandas
DataFrames
3 Monday 14-Sep 10:15 - 12:45 N39 Pandas:
subset, add,
remove data
4 Monday 21-Sep 10:15 - 12:45 N39 Pandas:
cleaning data,
missing
5 Friday 25-Sep 10:15 - 11:45 N39 Pandas:
grouping data
6 Monday 28-Sep 10:15 - 12:45 N39 Pandas:
merging data
7 Friday 02-Oct 10:15 - 12:45 N39 Pandas:
working with
text
8 Monday 05-Oct 10:15 - 12:45 N39 Nature of
econometric
data
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 2/9

[Pagina 3]
SYLLABUS 2026/2027
9 Friday 09-Oct 10:15 - 12:45 N39 Descriptive
Analysis
10 Monday 12-Oct 10:15 - 12:45 N39 Linear
regression
model (1)
11 Friday 16-Oct 10:15 - 12:45 N39 Linear
regression
model (2)
12 Friday 30-Oct 10:15 - 12:45 N39 Hypothesis
testing
13 Monday 02-Nov 10:15 - 12:45 N39 Further
specification
issues
14 Friday 06-Nov 10:15 - 12:45 N39 Binary
dependent
variables
15 Monday 09-Nov 10:15 - 12:45 N39 Data lab* /
Guest
speaker**
16 Friday 13-Nov 10:15 - 12:45 N39 Data lab* /
Guest
speaker**
17 Monday 16-Nov 10:15 - 12:45 N39 Data lab* /
Guest
speaker**
18 Monday 23-Nov 10:15 - 12:45 N39 Data lab* /
Guest
speaker**
19 Friday 27-Nov 10:15 - 12:45 N39 Final
presentations
20 Monday 30-Nov 10:15 - 12:45 N39 Final
presentations
21 Friday 04-Dec 10:15 - 12:45 N39 Final
presentations
Class group 28 — INTENT — Breschi S. / Gagliardi L. — 13:45-16:15, Sraffa 13 (3rd floor)
# Day Date Time Room Topic
1 Monday 07-Sep 13:45 - 16:15 N39 Intro + Python
recap
2 Friday 11-Sep 13:45 - 16:15 N37 Pandas
DataFrames
3 Monday 14-Sep 13:45 - 16:15 N39 Pandas:
subset, add,
remove data
4 Friday 18-Sep 13:45 - 16:15 N37 Pandas:
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 3/9

[Pagina 4]
SYLLABUS 2026/2027
cleaning data,
missing
5 Monday 21-Sep 13:45 - 16:15 N39 Pandas:
grouping data
6 Monday 28-Sep 13:45 - 16:15 N39 Pandas:
merging data
7 Friday 02-Oct 13:45 - 16:15 N37 Pandas:
working with
text
8 Monday 05-Oct 13:45 - 16:15 N39 Nature of
econometric
data
9 Friday 09-Oct 13:45 - 16:15 N37 Descriptive
Analysis
10 Monday 12-Oct 13:45 - 16:15 N39 Linear
regression
model (1)
11 Friday 16-Oct 13:45 - 16:15 N37 Linear
regression
model (2)
12 Friday 30-Oct 13:45 - 16:15 N37 Hypothesis
testing
13 Monday 02-Nov 13:45 - 16:15 N39 Further
specification
issues
14 Friday 06-Nov 13:45 - 16:15 N37 Binary
dependent
variables
15 Monday 09-Nov 13:45 - 16:15 N39 Data lab* /
Guest
speaker**
16 Friday 13-Nov 13:45 - 16:15 N37 Data lab* /
Guest
speaker**
17 Monday 16-Nov 13:45 - 16:15 N12 Data lab* /
Guest
speaker**
18 Monday 23-Nov 13:45 - 16:15 N39 Data lab* /
Guest
speaker**
19 Friday 27-Nov 13:45 - 16:15 N37 Final
presentations
20 Monday 30-Nov 13:45 - 16:15 N39 Final
presentations
21 Friday 04-Dec 13:45 - 16:15 N37 Final
presentations
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 4/9

[Pagina 5]
SYLLABUS 2026/2027
TEACHING METHODS
Selection:
Lectures
Lectures
Guest speaker's talks (in class or in distance)
Practical Exercises
Software-Based Exercises
In-class exercises
Data Analysis, Graphic Representations/Calculators
Individual works / Assignments
Project Work
Project Presentation
Collaborative Works / Assignments
Report/essay
Project work
Project Presentation
The course adopts a hands-on, bootcamp-style approach that combines lectures, coding
sessions, and applied econometric analysis. Almost every session integrates the explanation of
concepts with their direct implementation on real-world data.
Lectures and conceptual Inputs: Introduction to Python for data wrangling and
visualization, and to econometric methods (using Stata) for regression analysis and
hypothesis testing.
Practical, software-based exercises: In-class coding labs where students learn to
import, clean, structure, and analyze data using Python and econometric software.
Guest speaker seminars: Industry practitioners present applications of data to startup
finance, venture capital, and market analysis.
Collaborative project work: Students work in teams to develop an empirical project
based on Pitchbook data (US startups, 2012–2019). Teams identify a research question,
construct a dataset, apply econometric methods, and present results at the end of the
course.
Team support and feedback: Dedicated sessions with the teaching assistant to guide
teams on dataset construction, model selection, and interpretation of results.
Problem-solving and self-assessment: Instructor-led exercises, mock exams, and
quizzes to reinforce core techniques and ensure continuous learning.
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 5/9

[Pagina 6]
SYLLABUS 2026/2027
This blended approach ensures that students acquire both the technical skills (Python
programming, econometric modeling) and the applied research experience needed to turn
complex data into actionable business insights.
ASSESSMENT METHODS
Selected methods: Continuous
assessment
Partial exams General exam
Written individual
exam
(traditional/online)
x
Open and/or closed
answers questions
exam
x
Collaborative Works /
Assignment (report,
exercise, presentation,
project work etc.)
x
Assessment of the
results
achieved/outcome
x
Attending students
Written Exam (60% of final grade): Duration 1.5 hour. Includes both open and
closed questions, as well as multiple-choice items. The exam evaluates
students’ understanding of econometric methods, ability to interpret results, and
capacity to apply them to business problems.
Group Project (40% of final grade): Teams of up to 5 students develop an
empirical project using Pitchbook data (U.S. startups, 2012–2019). Projects must
identify a research question, build and analyze the relevant dataset, and present
findings in a slide deck (about 25 minutes). All group members receive the same
grade. To be considered “attending,” students must participate in a group and
deliver a final presentation. The project grade remains valid for all exam sessions
in the academic year.
Non-attending students
Written Exam only (100% of final grade): Duration 2.5 hours. Includes open,
closed, and multiple-choice questions. Focuses on econometric techniques and
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 6/9

[Pagina 7]
SYLLABUS 2026/2027
their application to real-world data, with no project component.
Organizational details
Group self-enrollment is managed via Blackboard.
Project support sessions are organized with the teaching assistant to guide
students on dataset construction, econometric methods, and interpretation of
results.
Mock exams will be distributed during the course to familiarize students with
exam structure.
The written exam is administered on Blackboard with Respondus Lockdown
Browser.
Assessment criteria
Written exam: accuracy of answers, clarity of reasoning, and ability to link
methods to applications.
Project: originality and clarity of the research question, appropriateness of
empirical methods, quality of data analysis, and effectiveness of the
presentation.
The final grade is determined by the weighted average of the written exam and project for
attending students, and by the written exam only for non-attending students.
GENAI USE
The use of Generative Artificial Intelligence tools by students, solely as support during teaching
activities*, is:
Consentito
Allowed
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 7/9

[Pagina 8]
SYLLABUS 2026/2027
TEACHING MATERIALS
- INTENT cl. 27
Attending and non-attending students
Part I (Python and Data Analysis): Jupyter notebooks distributed in class.
(Optional textbook) Stephanie Molin (2021). Hands-On Data Analysis with
Pandas. Packt Publishing Limited (chapters, 1-4).
Part II (Econometrics): Lecture slides and a curated selection of research papers made
available in advance through Blackboard.
Hill, R. C., Griffiths, W. E., & Lim, G. C. (2018). Principles of Econometrics. John
Wiley & Sons (selected chapters).
Sharing and access
All teaching materials (slides, datasets, Jupyter notebooks, project instructions, and
readings) will be distributed via Blackboard.
Auxiliary files for project work (data dictionary, ER diagram, etc.) are available in the
dedicated Pitchbook folder on Blackboard.
Selected bibliographic references are accessible through the Bocconi Library (Course
Reserve).
HONOR CODE
Bocconi University conceives of education as an ongoing process that stretches across a
person’s entire professional life. The University hopes that the entire Bocconi community will
respect the values of fairness and correctness associated with it, values which inspire and guide
the conduct of all community members as they pursue common objectives and a shared
mission. Bocconi University is also committed to building a truly inclusive climate based on
diversity. With the collaboration of faculty and students, it aims to ensure a safe learning
environment free from any form of discrimination based on race, religion, gender, geography,
age, disability or sexual orientation, in which there is room for a diversity of approaches and
where discussions are always conducted in a respectful manner. The Bocconi University Honor
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 8/9

[Pagina 9]
SYLLABUS 2026/2027
Code is published on the website at http://www.unibocconi.eu/honorcode, we encourage all
students to read it.
COURSE ETIQUETTE
AI Policy
In this course you are strongly encouraged to use AI, but always with a clear purpose. Think of
AI as an extra team member you can question and challenge: use it to test your ideas, explore
different perspectives, and refine your reasoning. You may find it helpful both when preparing
your project and when studying the course material more broadly. In both situations, the goal is
not to let AI provide ready-made answers, but to use it as a tool to deepen your understanding
and strengthen your ability to explain and defend your own reasoning. This will also prepare you
for the final exam, which you will complete without access to AI. Whenever you use AI in
preparing your work, you must include a short note in your document to acknowledge how it
was used.
Aggiornato al 24/08/2026 11:35
Powered by TCPDF (www.tcpdf.org)
© Università Bocconi | Via Sarfatti 25 | 20136 Milano | Tel. 02.5836.1 Pag. 9/9
