import urllib.parse
cats = ['Gezond & verzorging',
        'Lichaamsverzorging',
        'Deodorant', 'Bodylotion en bodymilk', 'Bad en douche', 'Handzeep en handgel', 'Zonnebrand en aftersun', 'Lipverzorging', 'Watten', 'Handcremes', 'Persoonlijke hygiene', 'Maandverband', 'Intiemverzorging', 'Tampons', 'Inlegkruisjes', 'Incontinentie', 'Mini reisverpakkingen', 'Mini deodorant en geuren', 'Mini bad en douche', 'Mini shampoo en conditioner', 'Mini olie en lotion', 'Mini haarstyling', 'Mini tandpasta', 'Mini scheerschuim en scheergel', 'Toilettassen', 'Haarverzorging', 'Conditioner', 'Shampoo', 'Haarstyling', 'Haarkuur en haarmasker', 'Haarkleuring', 'Kappersproducten', 'Haarserum', 'Mondverzorging', 'Mondwater & spray', 'Tandenborstels', 'Tandpasta', 'Tandenstokers, floss & ragers', 'Kunstgebitverzorging', 'Elektrische tandenborstels', 'Scheren & ontharen', 'Scheermesjes', 'Scheerschuim en scheergel', 'Ontharingscreme, wax en hars', 'Scheerapparaten', 'Gezichtsverzorging man', 'Scheren', 'Aftershave', 'Creme', 'Reiniging man', 'Gezichtsmasker man', 'Gezichtsverzorging vrouw', 'Dagcreme', 'Reiniging', 'Gezichtsmasker', 'Oogcreme en serum', 'Onzuivere huid & acne', 'Nachtcreme', 'Accessoires', 'Optiek', 'Lenzen', 'Lenzenvloeistof', 'Dames brillen', 'Leesbrillen', 'Heren brillen', 'Wondverzorging', 'Wondverzorging', 'Pleisters', 'Wondontsmetting', 'Sportverzorging', 'Bandages en windsels', 'EHBO', 'Seksualiteit', 'Glijmiddelen en seksspeeltjes', 'Condooms', "Vibrators en dildo's", 'Vitaminen en supplementen', 'Multivitaminen', 'Botten', 'Weerstand', 'Enkelvoudige vitaminen', 'Uiterlijk', 'Ontspanning en rust', 'Overige voedingssuplementen', 'Blaas', 'Kind', 'Gewrichten', 'Hart en visolie', 'Mineralen', 'Energie', 'Man', 'Zwangerschap', 'Natuurlijke gezondheid', 'Geneesmiddelen', 'Weerstand', 'Luchtwegen en verkoudheid', 'Spierwrijfmiddelen', 'Huidverzorging en koortslip', 'Pijnstillers', 'Spijsvertering', 'Stoppen met roken', 'Luizen', 'Reisziekte', 'Aambeien', 'Homeopathisch', 'Oor en mond', 'Vaginale schimmel', 'Allergieen', 'Afslanken', 'Supplementen', 'Maaltijdvervangers', 'Voetverzorging', 'Voetverzorging', 'Kalknagels', 'Voetschimmel', 'Voetdeodorant', 'Verzorgende voetcremes', 'Wratten', 'Eelt en harde huid', 'Sportvoeding', 'Sportdranken', 'Sportvoeding', 'Zwangerschap', 'Zwangerschapstest en ovulatietest', 'Zwangerschapsvitamines', 'Haaraccessoires', 'Haaraccessoires', 'Gehoorbescherming', 'Oordoppen', 'Wonen & vrije tijd', 'Outdoor en vrije tijd', 'Outdoor en vrije tijd', 'Sportartikelen', 'Woonaccessoires', 'Kaarsen', 'Woonaccessoires', 'Lampen', 'Feestartikelen', 'Feestartikelen', 'Seizoenen', 'Kerst', 'Vakantie', 'Carnaval', 'Halloween', 'Pasen', 'Valentijn', 'Tuinartikelen', 'Tuinartikelen', 'Boeken & tijdschriften', 'Boeken', 'Kaarten', 'Kantoor benodigdheden', 'Kantoor benodigdheden', 'Knutselen en hobby', 'Knutselen en hobby', 'Muziek', 'Muziek', 'Films', 'Dvd en blue-ray', 'Wonen', 'Meubels', 'Games', 'Bordspellen', 'Elektronica & media', 'Elektronica & media', 'Batterijen', 'Beeld en geluid', 'Media', 'Tablets en computers', 'Verlichting', 'Elektronica accessoires', 'Persoonlijke verzorging', 'Cartridges', 'Foto en film', 'Huishoudelijke apparaten', 'Overige elektronika', 'Telefonie', 'Huishouden', 'Toilet en keuken', 'Toiletblokken', 'Luchtverfrissers', 'Toiletpapier en vochtige doekjes', 'Tissues en zakdoekjes', 'Keukenpapier', 'Toiletreinigers', 'Keuken artikelen', 'Wassen en schoonmaken', 'Schoonmaken', 'Afwasmiddel', 'Wasverzachter', 'Wasmiddel', 'Vaatwastabletten', 'Reiniging vaatwasser', 'Vlekkenverwijderaars', 'Overig huishoudelijk', 'Overige huishoudelijke artikelen', 'Huishoudelijk textiel', 'Insectenbestrijding', 'Textielverf', 'Dierverzorging', 'Kat', 'Overige dierverzorging', 'Hond', 'Kleding & sieraden', 'Dames', 'Panties en sokken', 'Dames kleding', 'Dames ondergoed', 'Patty Brard Collectie', 'Dames accessoires', 'Dames nachtmode', 'Heren', 'Sokken', 'Heren ondergoed', 'Heren accessoires', 'Heren nachtmode', 'Kleding accessoires', 'Tassen', 'Koffers', 'Schoenen, slippers en sloffen', "Baby's en kinderen", 'Babykleding', 'Kinderkleding', 'Baby- en kinderaccessoires', 'Sieraden & bijoux', 'Sieraden & bijoux', 'Eten & drinken', 'Koude dranken', 'Overige dranken', 'Energy drank', 'Snacks en snoep', 'Snacks en snoep', 'Mondverfrissers', 'Chips', 'Koffie en thee', 'Koffie', 'Thee', 'Make-up & geuren', 'Make-up accessoires', 'Wattenschijfjes en wattenstaafjes', 'Nagellakremovers', 'Make-up remover & reiniging', 'Make-up accessoires', 'Kunstnagels', 'Geuren en geschenkset', 'Geschenksets', 'Damesgeuren', 'Herengeuren', 'Make-up', 'Foundation & concealer', 'Mascara', 'Wenkbrauwproducten', 'Highlighters en bronzers', 'Lipstick', 'Nagellak', 'Oogschaduw', 'Lipliner', 'Blush', 'Poeder', 'Lipgloss', 'Baby & kind', 'Luiers en verschonen', 'Luiers', 'Babydoekjes', 'Zwemluiers', 'Luierbroekjes en pyjamabroekjes', 'Babyverzorging', 'Baby huidverzorging', 'Babyhaartjes, bad en douche', 'Mama verzorging', 'Baby accessoires', 'Baby accessoires', 'Flessen en flessenspenen', 'Fopspenen', 'Baby speelgoed', 'Anti-lekbekers', 'Kinderbestek', 'Speelgoed', 'Speelgoed', 'Babyvoeding', 'Flesvoeding', 'Opruiming', 'Black Friday', 'Cadeau ideeën', 'Cadeau ideeën mannen', 'Cadeau ideeën kinderen', 'op=opruiming', '50% korting', 'Nieuw', 'Extra Deals', 'Folder artikelen']

def encode_category(c):
    """ This helper function encodes any category name into a URL-friendly
    string, making sensible and human-readable substitutions. """
    c = c.lower()
    c = c.replace(" " ,"-")
    c = c.replace("," ,"")
    c = c.replace("'" ,"")
    c = c.replace("&" ,"en")
    c = c.replace("ë" ,"e")
    c = c.replace("=" ,"-is-")
    c = c.replace("%" ,"-procent-")
    c = c.replace("--" ,"-")
    c = urllib.parse.quote(c)
    return c

def decode_category(c ,category):
    """ This helper function encodes any category name into a URL-friendly
    string, making sensible and human-readable substitutions. """
    c = c.lower()
    c = c[:1].upper() + c[1:]
    # c = c.replace("-", " ")
    # c = c.replace("", ",")
    # c = c.replace("", "'")
    c = c.replace("-en-", " & ")
    c = c.replace("eee", "eeë")
    c = c.replace(" is ", " = ")
    c = c.replace("-procent-", "% ")
    c = c.replace("-", " ")

    # c = c.replace("-", "--")
    c = urllib.parse.unquote(c)
    return c


encoded_cats = [encode_category(c) for c in cats]
decoded_cats = [decode_category(c) for c in encoded_cats]

incorrect_dec = []
for w1, w2 in zip(cats, decoded_cats):
    if w1 != w2:
        incorrect_dec.append([w1, w2])
        print(f"\n{w1} != {w2}")

print(f"{len(incorrect_dec)} words not the same out of the {len(cats)}")

test_str = "hello waarom en dit 50%"

print(f"initial string = {test_str}")
encoded = encode_category(test_str)
print(encoded, type(encoded))

decoded = decode_category(encoded)
print(decoded, type(decoded))


