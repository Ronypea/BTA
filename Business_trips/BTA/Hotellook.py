import requests
from geopy.geocoders import Nominatim

def get_hotels(coordinates): #нахождение всех подходящих отелей
    token = '742810434e3235cf223d8039ac5d8401'
    query = 'http://engine.hotellook.com/api/v2/lookup.json?query={}&lookFor=hotel&limit=15&token={}'.format(coordinates,
                                                                                                            token)
    response = requests.get(query)
    hotels = response.json()['results']['hotels']
    return hotels

def info_hotels(check_in, check_out, city, id_hotel): #информация по всем найденным отелям
    data = {'data': 'None'}
    info = []
    api_token = '742810434e3235cf223d8039ac5d8401'
    domain = ['http://engine.hotellook.com/api/v2/cache.json', # вывод стоимости проживания
              'http://engine.hotellook.com/api/v2/static/hotels.json'] # информация об отеле

    fields = ['location={}&checkIn={}&checkOut={}&hotelId={}&currency=eur&adults=1'.format(city, check_in,
                                                                            check_out, id_hotel),
              'locationId={}'.format(id_hotel)]
    for i in range(2):
        query_params = {
            'domain': domain[i],
            'fields': fields[i],
            'access_token': api_token
        }
        query = '{domain}?{fields}&token={access_token}'.format(**query_params)
        response = requests.get(query)
        if response.json() == None:
            break
        else:
            info.append(response.json())
    data['data'] = info
    return data

def choose_hotel(hotels, status): #выборка отеля
    this_one_comfort, this_one_cheap = hotels[0], hotels[0]
    for i in range(1, len(hotels)):
        try:
            if hotels[i]['data'][0]['stars'] > this_one_comfort['data'][0]['stars']:
                this_one_comfort = hotels[i]
            elif hotels[i]['data'][0]['stars'] == this_one_comfort['data'][0]['stars'] and hotels[i]['data'][0]['priceAvg'] < this_one_comfort['data'][0]['priceAvg']:
                this_one_comfort = hotels[i]
                this_one_cheap = hotels[i]
            elif hotels[i]['data'][0]['priceAvg'] < this_one_comfort['data'][0]['priceAvg']:
                this_one_cheap = hotels[i]
        except IndexError:
            pass
    if status == 1:
        return this_one_comfort
    else:
        return this_one_cheap


def check(adress): 
    try: 
        location = geolocator.geocode(adress) 
        return True 
    except: 
        return False

def start(data):
    geolocator = Nominatim()
    location = geolocator.geocode(data['adress'])
    coordinate = '{}'.format(location.latitude) +','+ '{}'.format(location.longitude)
    all_hotels = get_hotels(coordinate)

    for i in range(len(all_hotels)):
        resp = info_hotels(data['time_dep'], data['time_ar'], data['arrival'], all_hotels[i]['id'])
        all_hotels[i].update(resp)
    hotel = choose_hotel(all_hotels, data['status'])
    return hotel

