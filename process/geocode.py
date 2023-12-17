import os
import googlemaps


def get_lat_log_from_addres(add,key=None):
    '''get lat long in graus decimal thourt geocoding
    
    Args
        add (str): Adress      
    return 
        tuple: (lat, long) 
    '''
    API_KEY_GOOGLE_MAPS = key or os.getenv('API_KEY_GOOGLE_MAPS')
    gmaps = googlemaps.Client(key=API_KEY_GOOGLE_MAPS)
    res = gmaps.geocode(add)
    return tuple(res[0]['geometry']['location'].values())    

def get_distance_matrix(origin,destination, key=None):
    """_summary_

    Args:
        origin (tuple): tuple lat,long
        destination (tuple): tuple lat,long

    Returns:
        int: time i seconds
    """
    API_KEY_GOOGLE_MAPS = key or os.getenv('API_KEY_GOOGLE_MAPS')
    gmaps = googlemaps.Client(key=API_KEY_GOOGLE_MAPS)
    res = gmaps.distance_matrix(origin,destination)
    return res['rows'][0]['elements'][0]['duration']['value']