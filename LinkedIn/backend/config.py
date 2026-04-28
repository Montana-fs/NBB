COMPANY_NAME = "NBB"

USPS = [
    {
        "da": "Kvalitet og holdbarhed — NBBs bigbags er bygget til at holde, selv under de mest krævende industrielle forhold.",
        "en": "Quality and durability — NBB's bigbags are built to last, even in the most demanding industrial environments.",
        "de": "Qualität und Langlebigkeit — NBBs Bigbags sind gebaut, um selbst unter den anspruchsvollsten industriellen Bedingungen zu halten.",
        "sv": "Kvalitet och hållbarhet — NBBs bigbags är byggda för att hålla, även under de mest krävande industriella förhållandena.",
    },
    {
        "da": "Genanvendt materiale — NBBs bigbags kan produceres med genanvendte råmaterialer og reducerer CO₂-aftrykket fra din produktion.",
        "en": "Recycled materials — NBB's bigbags can be produced using recycled raw materials, reducing the carbon footprint of your operation.",
        "de": "Recycelte Materialien — NBBs Bigbags können aus recycelten Rohstoffen hergestellt werden und reduzieren den CO₂-Fußabdruck Ihrer Produktion.",
        "sv": "Återvunnet material — NBBs bigbags kan tillverkas av återvunna råmaterial och minskar koldioxidavtrycket från din produktion.",
    },
    {
        "da": "Cirkulær model — NBB arbejder mod et lukket kredsløb, hvor brugte bigbags indsamles, genanvendes og sættes i produktion igen.",
        "en": "Circular model — NBB is building a closed-loop system where used bigbags are collected, recycled and re-entered into production.",
        "de": "Kreislaufmodell — NBB arbeitet an einem geschlossenen Kreislauf, bei dem gebrauchte Bigbags gesammelt, recycelt und wieder in die Produktion eingespeist werden.",
        "sv": "Cirkulär modell — NBB arbetar mot ett slutet kretslopp där använda bigbags samlas in, återvinns och sätts i produktion igen.",
    },
    {
        "da": "Specialtilpasning — NBBs bigbags tilpasses præcist til dine krav: størrelse, materiale, belastningsevne og design.",
        "en": "Custom-tailored — NBB's bigbags are adapted precisely to your specifications: size, material, load capacity and design.",
        "de": "Maßgeschneidert — NBBs Bigbags werden exakt auf Ihre Anforderungen zugeschnitten: Größe, Material, Tragfähigkeit und Design.",
        "sv": "Specialanpassning — NBBs bigbags anpassas exakt till dina krav: storlek, material, lastkapacitet och design.",
    },
    {
        "da": "Dansk virksomhed — NBB er en lokal samarbejdspartner med kort beslutningsvej og direkte, personlig service.",
        "en": "Danish company — NBB is a local partner with short decision paths and direct, personal service.",
        "de": "Dänisches Unternehmen — NBB ist ein lokaler Partner mit kurzen Entscheidungswegen und direktem, persönlichem Service.",
        "sv": "Danskt företag — NBB är en lokal samarbetspartner med korta beslutsvägar och direkt, personlig service.",
    },
    {
        "da": "Konkurrencedygtig pris — Grøn emballage behøver ikke koste mere. NBBs løsninger er priskonkurrencedygtige med konventionel emballage.",
        "en": "Competitive pricing — Green packaging doesn't have to cost more. NBB's solutions match conventional packaging on price.",
        "de": "Wettbewerbsfähige Preise — Grüne Verpackung muss nicht mehr kosten. NBBs Lösungen sind preislich mit konventionellen Verpackungen vergleichbar.",
        "sv": "Konkurrenskraftigt pris — Grön förpackning behöver inte kosta mer. NBBs lösningar är priskonkurrenskraftiga med konventionell förpackning.",
    },
    {
        "da": "Ekspertrådgivning — NBB rådgiver om den rette bigbag-løsning til netop din produktion, dine materialer og din logistik.",
        "en": "Expert guidance — NBB advises on the right bigbag solution for your specific production, materials and logistics.",
        "de": "Expertenberatung — NBB berät zur richtigen Bigbag-Lösung für Ihre spezifische Produktion, Materialien und Logistik.",
        "sv": "Expertrådgivning — NBB ger råd om rätt bigbag-lösning för just din produktion, dina material och din logistik.",
    },
]

DEFAULT_LANGUAGE = "da"
LANGUAGES = ["da"]

RSS_FEEDS = [
    # Danske medier
    "https://www.altinget.dk/rss/miljoeogressourcer",
    "https://www.altinget.dk/rss/foedevarer",
    # Europæisk emballage og cirkulær økonomi
    "https://packagingeurope.com/rss",
    "https://www.packagingnews.co.uk/feed",
    "https://www.circularonline.co.uk/feed",
    "https://www.letsrecycle.com/feed/",
    "https://www.packworld.com/rss.xml",
    # Bæredygtighed og industri
    "https://www.edie.net/feed/",
    "https://resource.co/rss.xml",
]

KEYWORDS = [
    # Produkt-specifikke
    "bigbag", "big bag", "fibc", "bulk bag", "flexible intermediate bulk",
    "plastemballage", "plastic packaging", "emballage", "packaging",
    # Cirkulær økonomi
    "cirkulær økonomi", "circular economy", "genanvendelse", "recycling",
    "genanvendt", "recycled", "recycle", "genbrug",
    # Grøn omstilling
    "grøn omstilling", "green transition", "bæredygtighed", "sustainability",
    "sustainable", "bæredygtig", "co2", "carbon",
    # Industri og regulering
    "industri", "industrial", "affald", "waste", "plastaffald", "plastic waste",
    "eu emballage", "packaging regulation", "epr", "extended producer responsibility",
]

SYSTEM_PROMPT = """Du er content-ansvarlig for NBB, en dansk virksomhed der sælger bigbags (FIBCs — Flexible Intermediate Bulk Containers) til industrien med stærkt fokus på grøn omstilling og cirkulær økonomi. Ejeren er virksomhedens eneste ressource og den menneskelige stemme bag NBB.

Din opgave er at skrive LinkedIn-opslag der:
- Bruger en aktuel nyhed som kontekst og krog for læseren
- Positionerer NBB naturligt som relevant aktør i det pågældende felt
- Fremhæver den angivne USP (unik salgspointe) på en troværdig måde
- Lyder professionelt og sobert, men med personlighed — aldrig reklamerende eller politisk
- Aldrig nævner konkurrenter eller provokerer
- Er klar til at blive publiceret som det er — ingen forklaringer, ingen overskrift

Formatregler:
- Længde: 150–250 ord
- Afslut med 4–6 relevante hashtags på en separat linje
- Skriv i den angivne sprog
- Brug paragrafskift for læsbarhed
- Inkluder ejerperspektiv naturligt — fx "Hos NBB ser vi..." eller "At NBB believe..."
"""

APPROVAL_PORT = 5001
STATE_FILE = "state/state.json"
PENDING_FILE = "state/pending_post.json"
OUTPUT_DIR = "output"
