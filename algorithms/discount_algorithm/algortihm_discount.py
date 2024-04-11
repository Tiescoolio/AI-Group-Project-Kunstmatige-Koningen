"""
Aanbeveling op basis van producten die de gebruiker eerder bekeken heeft en een aanbieding hebben



Als gebruiker die de webshop bezoekt, wil ik gepersonaliseerde productaanbevelingen ontvangen op basis van artikelen die ik eerder bekeken heb en die een aanbieding hebben



    Gegevensverzameling:

    Houd een registratie bij van orders van elke gebruiker binnen de webshop.


    Identificatie van aanbiedingen:

    Identificeer producten met lopende aanbiedingen binnen het assortiment.

    Rangschik ze op de beste aanbiedingen vergeleken met de MRSP


    Bepalen van eerdere interactie:

    Analyseer de vorige orders van elke gebruiker om eerder bekeken items te identificeren.


    Productselectie:

    Selecteer de producten die de beste actie hebben die door de klant eerder gekocht zijn.

    Zorg voor diversiteit in de selectie om een verscheidenheid aan producten van de voorkeursmerken aan te bieden.


    Weergave van Aanbevelingen:

    Presenteer de aanbevolen producten op de startpagina/dashboard





User story

Als een gebruiker die regelmatig de webshop bezoekt, log ik in op mijn account om nieuwe aanbiedingen te bekijken. Bij het openen van mijn gepersonaliseerde dashboard zie ik een sectie met de titel "Aanbevolen aanbiedingen voor jou". Ik ben enthousiast om producten te zien die ik eerder heb bekeken en die nu een aanbieding hebben. Ik klik op een van de aanbevolen producten, profiteer van de aanbieding en voltooi mijn aankoop, waardoor ik zowel mijn interesse in de producten als mijn behoefte aan een goede deal vervul.





Smart analyse

    Specifiek:

    Het ontwikkelen van een algoritme dat gepersonaliseerde aanbiedingen genereert op basis van eerder bekeken producten met aanbiedingen.

    Meetbaar:

    De effectiviteit van het algoritme kan worden gemeten aan de hand van de mate waarin gebruikers op de aanbevolen producten klikken, toevoegen aan hun winkelwagen en daadwerkelijk aankopen.

    Acceptabel:

    Het doel is haalbaar met de aanbiedingen en de vorige orders.

    Relevant:

    Het algoritme is relevant omdat het inspeelt op de interesse en koopintentie van de gebruiker.

    Tijdgebonden:

    Het algoritme is binnen de tijd haalbaar met de beschikbare data en implementatietijd.
"""

# kijkt naar wat de gebruiker bekeken heeft, en geeft een aanbeveling als er een aanbieding is op die producten.
#
# Als een gebruiker, wil ik aanbevelingen ontvangen voor producten waar ik interesse in heb getoond, zodat ik op de hoogte ben van eventuele aanbiedingen op die producten en kan profiteren van mogelijke kortingen.
#
# Acceptatiecriteria:
#
#     Het systeem moet in staat zijn om producten te identificeren die de gebruiker heeft bekeken.
#     Het systeem moet vervolgens controleren of er op deze bekeken producten aanbiedingen beschikbaar zijn.
#     Als er aanbiedingen beschikbaar zijn, moeten deze worden opgenomen in de aanbevelingen aan de gebruiker.
#     Het systeem moet de aanbiedingen presenteren op een duidelijke en aantrekkelijke manier.

#
# SELECT id
#                     FROM products
#                     --JOIN profiles AS t2 ON t1.profile_id = t2.id
#                     INNER JOIN products on similars.id = products.id
#                     WHERE t1.viewed_before = %s
#                     OR t1.similars = %s
#                     ORDER BY t2.aanbiedingen IS NOT NULL DESC
#                     LIMIT %s;
from algorithms.utils import connect_to_db as connect



con = connect()
cur = con.cursor()
def get_correct_query(profiel_id):

    # Query to get similars items
    similars_query = f"""
                    SELECT similars.id, aanbiedingen, selling_price, price_discount FROM similars
                    INNER JOIN products on similars.id = products.id
                    WHERE aanbiedingen IS NOT NULL
                    AND profile_id = '{profiel_id}'
                    ORDER BY aanbiedingen DESC;
                """
    cur.execute(similars_query)
    similars_values = cur.fetchall()

    # Query to get viewed_before items
    viewed_before_query = f"""
                        SELECT viewed_before.id, aanbiedingen, selling_price, price_discount FROM viewed_before
                        INNER JOIN products on viewed_before.id = products.id
                        WHERE aanbiedingen IS NOT NULL
                        AND profile_id = '{profiel_id}'
                        ORDER BY aanbiedingen DESC;
                    """

    cur.execute(viewed_before_query)
    viewed_before_values = cur.fetchall()

    return similars_values, viewed_before_values

#Functie om de lijst te sorteren op de beste aanbiedingen
def get_correct_kwewie(profiel_id):
    # Get the values from the query
    similars_values, viewed_before_values = get_correct_query(profiel_id)

    print(similars_values[0:5], "\n")
    print(viewed_before_values[0:5])



    return similars_values, viewed_before_values

get_correct_kwewie("5e1f350dbb0c7a1b7f5e5d1f")
def main():
    pass

    # Calculates the ranking

