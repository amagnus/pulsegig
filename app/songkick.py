import requests
import json
from django.conf import settings


# Returns array of maximum 50 indices
def array_maker(length):
    indices = []
    i = 0
    while i < length:
        indices.append(i)
        i += 1
        if i == 50:
            break
    return indices


def artist_search(artist):
    endpoint = 'http://api.songkick.com/api/3.0/search/artists.json?query=%s&apikey=%s' % (artist, settings.SONGKICK_KEY)

    r = requests.get(endpoint)
    artists = json.loads(r.text)

    if artists['resultsPage']['totalEntries'] == 0:
        return 0

    result = dict()
    for x in array_maker(len(artists['resultsPage']['results']['artist'])):
        result[artists['resultsPage']['results']['artist'][x]['id']] = artists['resultsPage']['results']['artist'][x]['displayName']
        if len(result) == 5:
            break

    return result


def find_metroareaID(ipaddr):
    endpoint = 'http://api.songkick.com/api/3.0/search/locations.json?location=ip:%s&apikey=%s' % (ipaddr, settings.SONGKICK_KEY)

    r = requests.get(endpoint)
    areas = json.loads(r.text)
    result = dict()

    for x in array_maker(len(areas['resultsPage']['results']['location'])):
        result[areas['resultsPage']['results']['location'][x]['metroArea']['id']] = areas['resultsPage']['results']['location'][x]['metroArea']['displayName']
        if len(result) == 5:
            break

    return result


def event_search(artistID, metroareaID):
    endpoint = 'http://api.songkick.com/api/3.0/events.json?apikey=%s&artist_id=%s&location=sk:%s' % (settings.SONGKICK_KEY, artistID, metroareaID)

    r = requests.get(endpoint)
    raw = json.loads(r.text)
    result = dict()

    for x in array_maker(raw['resultsPage']['totalEntries']):
        result['eventskID'] = raw['resultsPage']['results']['event'][x]['id']
        result['eventURL'] = raw['resultsPage']['results']['event'][x]['uri']
        result['date'] = raw['resultsPage']['results']['event'][x]['start']['date']

    return result


# Returns array of bands on tour similar to input band
def search_similar_bands(artistID):
    endpoint = 'http://api.songkick.com/api/3.0/artists/%s/similar_artists.json?apikey=%s' % (artistID, settings.SONGKICK_KEY)

    r = requests.get(endpoint)
    raw = json.loads(r.text)
    result = dict()

    for x in array_maker(raw['resultsPage']['totalEntries']):
        if raw['resultsPage']['results']['artist'][x]['onTourUntil'] != None:
            result[raw['resultsPage']['results']['artist'][x]['id']] = raw['resultsPage']['results']['artist'][x]['displayName']

    return result

