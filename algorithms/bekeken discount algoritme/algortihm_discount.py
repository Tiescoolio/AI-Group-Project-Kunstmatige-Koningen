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



def get_correct_query():
    popular_query = """
                    SELECT t1.id
                    FROM products AS t1
                    JOIN profiles AS t2 ON t1.profile_id = t2.id
                    WHERE t1.category = %s
                    AND t1.viewed_before = %s 
                    AND t1.similars = %s
                    ORDER BY t2.aanbiedingen IS NOT NULL DESC
                    LIMIT %s;
                """
    return popular_query


def get_recommendations(cursor, count: int) -> tuple:

    # Query to get recommended items
    query = get_correct_query()

    #De data is ongefilterd op beschikbaarheid van similars en viewed_before, dus moet het via de get_availibity functie nog gecheckt worden

    query_prod_ids = """select products id from products"""
    prod_ids = cursor.fetchall()



    #MongoDB_gebeuren/query_statements/mongodb_data/products_data.py
    from MongoDB_gebeuren import get_availability
    get_availability()

    # Execute the SQL query with the given value as parameters
    cursor.execute(query)

    # Fetch all the rows returned by the query
    ids = cursor.fetchall()
    recommended_products = tuple([_id[0] for _id in ids])

    return recommended_products[:count]
