from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                   from genre g
                   order by g.Name """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(idGenre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct(a.ArtistId) as ArtistId,a.Name as Name
                    from artist a,album al,track t
                    where t.GenreId=%s and t.AlbumId=al.AlbumID and al.ArtistID=a.ArtistId
                    order by a.Name """

        cursor.execute(query,(idGenre,))

        for row in cursor:
            result.append(Artist(row["ArtistId"],row["Name"]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllEdges(idMap, genreID):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct(ar.ArtistId) as ArtistId,i.CustomerId as customer ,sum(il.Quantity) as somma
                    from invoiceline il,invoice i, track t, album a, artist ar
                    where il.InvoiceId=i.InvoiceId and il.TrackId=t.TrackId 
                    and t.AlbumId=a.AlbumId and a.ArtistId=ar.ArtistId
                    and t.GenreId=%s
                    group by  a.ArtistId ,i.CustomerId
                    order by i.CustomerId """

        cursor.execute(query,(genreID,))

        for row in cursor:
            artist_id=row["ArtistId"]
            
            if artist_id in idMap:
                customer=row["customer"]
                quantita=row["somma"]
                artist=idMap[artist_id]
                if artist_id not in result:
                    result[artist_id]={"artist":artist,"customer":set(),"popolarita":0}
                result[artist_id]["customer"].add(customer)
                result[artist_id]["popolarita"]+=quantita

        cursor.close()
        conn.close()
        return result
    
    #menu a tendina di country
    @staticmethod
    def getAllCountries():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT Country
        FROM Customer
        ORDER BY Country
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()

        return result
    
    #I vertici sono i clienti residenti nel paese selezionato. 
    #bisogna costruire una dataclass di tipo customer
    @staticmethod
    def getAllNodes(country):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT c.CustomerId,
            c.FirstName,
            c.LastName,
            c.Country,
            SUM(i.Total) as spesaTotale

        FROM Customer c
            LEFT JOIN Invoice i
            ON c.CustomerId=i.CustomerId

        WHERE c.Country=%s

        GROUP BY c.CustomerId
        """

        cursor.execute(query,(country,))

        for row in cursor:

            if row["spesaTotale"] is None:
                row["spesaTotale"]=0

            result.append(Customer(**row))

        cursor.close()
        conn.close()

        return result
    
    #Esiste un arco tra due clienti se hanno acquistato almeno un brano dello stesso artista.
    @staticmethod
    def getArtistsByCustomer(idMap,country):

        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT c.CustomerId,
            ar.ArtistId

        FROM Customer c,
            Invoice i,
            InvoiceLine il,
            Track t,
            Album al,
            Artist ar

        WHERE c.CustomerId=i.CustomerId
        AND i.InvoiceId=il.InvoiceId
        AND il.TrackId=t.TrackId
        AND t.AlbumId=al.AlbumId
        AND al.ArtistId=ar.ArtistId
        AND c.Country=%s
        """

        cursor.execute(query,(country,))

        for row in cursor:

            customerId=row["CustomerId"]

            if customerId not in result:
                result[customerId]=set()

            result[customerId].add(row["ArtistId"])

        cursor.close()
        conn.close()

        return result
    #menu a tendina organizzato su mediatype, 
    # costruire una dataclass mediatype
    @staticmethod
    def getAllMediaTypes():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM MediaType
        ORDER BY Name
        """

        cursor.execute(query)

        for row in cursor:
            result.append(MediaType(**row))

        cursor.close()
        conn.close()

        return result
    #I vertici sono gli artisti che hanno almeno un brano del media type selezionato.
    #popolarità di A=(numero totale di brani acquistati)
    #aggiungere voce popolarità agli artisti
    @staticmethod
    def getAllNodes(mediaTypeId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT ar.ArtistId,
            ar.Name,
            SUM(il.Quantity) as popolarita

        FROM Artist ar,
            Album al,
            Track t,
            MediaType mt,
            InvoiceLine il

        WHERE ar.ArtistId=al.ArtistId
        AND al.AlbumId=t.AlbumId
        AND t.MediaTypeId=mt.MediaTypeId
        AND il.TrackId=t.TrackId
        AND mt.MediaTypeId=%s

        GROUP BY ar.ArtistId
        """
        cursor.execute(query,(mediaTypeId,))
        for row in cursor:
            result.append(
                Artist(**row)
            )
        cursor.close()
        conn.close()
        return result
    #L'utente inserisce un range di prezzo unitario (UnitPrice) tramite due menu a tendina
    @staticmethod
    def getAllPrices():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT UnitPrice
        FROM Track
        ORDER BY UnitPrice
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row["UnitPrice"])

        cursor.close()
        conn.close()

        return result
    # I vertici sono gli artisti che hanno almeno un brano con UnitPrice nel range selezionato.
    @staticmethod
    def getAllNodes(minPrice,maxPrice):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT ar.*

        FROM Artist ar,
            Album al,
            Track t

        WHERE ar.ArtistId=al.ArtistId
        AND al.AlbumId=t.AlbumId
        AND t.UnitPrice >= %s
        AND t.UnitPrice <= %s
        """

        cursor.execute(query,(minPrice,maxPrice))

        for row in cursor:

            result.append(
                Artist(**row)
            )

        cursor.close()
        conn.close()

        return result
    #Esiste un arco tra due artisti se almeno un cliente ha acquistato brani di entrambi nella stessa Invoice
    
    @staticmethod
    def getAllEdges(idMap,minPrice,maxPrice):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT
            i.InvoiceId,
            ar.ArtistId

        FROM Invoice i,
            InvoiceLine il,
            Track t,
            Album al,
            Artist ar

        WHERE i.InvoiceId=il.InvoiceId
        AND il.TrackId=t.TrackId
        AND t.AlbumId=al.AlbumId
        AND al.ArtistId=ar.ArtistId
        AND t.UnitPrice >= %s
        AND t.UnitPrice <= %s
        """
        cursor.execute(query,(minPrice,maxPrice))
        for row in cursor:
            invoiceId = row["InvoiceId"]
            artistId = row["ArtistId"]
            if artistId in idMap:
                artist = idMap[artistId]
                if invoiceId not in result:
                    result[invoiceId] = set()
                result[invoiceId].add(artist)
        cursor.close()
        conn.close()
        return result
    #L'utente seleziona un impiegato (Employee, tabella employee) dal menu a tendina 
    #creare classe employe in questo caso
    @staticmethod
    def getAllEmployees():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT *
        FROM Employee
        ORDER BY LastName
        """
        cursor.execute(query)
        for row in cursor:
            result.append(Employee(**row))
        cursor.close()
        conn.close()
        return result
    #i vertici saranno i clienti seguiti da quell'impiegato
    #costruisco la classe costumer aggiungendoci spesa totale e n acquisti
    @staticmethod
    def getAllNodes(employeeId):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT c.CustomerId,
            c.FirstName,
            c.LastName,
            c.SupportRepId,
            SUM(i.Total) as spesaTotale,
            COUNT(i.InvoiceId) as nAcquisti

        FROM Customer c
            LEFT JOIN Invoice i
            ON c.CustomerId=i.CustomerId

        WHERE c.SupportRepId=%s

        GROUP BY c.CustomerId
        """

        cursor.execute(query,(employeeId,))

        for row in cursor:

            if row["spesaTotale"] is None:
                row["spesaTotale"]=0

            result.append(Customer(**row))

        cursor.close()
        conn.close()

        return result
    