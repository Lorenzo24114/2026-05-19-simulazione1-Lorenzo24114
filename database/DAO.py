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