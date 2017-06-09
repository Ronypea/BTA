import requests
import csv
import http.client


def get_ticket_(iata_dep, iata_ar,time_dep, time_ar):
    connection = http.client.HTTPConnection("api.travelpayouts.com")
    connection.request("GET", '/v1/prices/direct?origin={}&destination={}&depart_date={}&return_date={}&currency=EUR&token=742810434e3235cf223d8039ac5d8401'.format(
                                                                                        iata_dep, iata_ar,
                                                                                         time_dep, time_ar,))
    data = connection.getresponse()
    tickets = data.read()
    return tickets

def get_ticket(i,iata_dep, iata_ar, time_dep, time_ar):

    api_token = '742810434e3235cf223d8039ac5d8401'
    domain = ['http://api.travelpayouts.com/v1/prices/cheap',
              'http://api.travelpayouts.com/v1/prices/direct']

    query_params = {
        'domain': domain[i],
        'fields': 'origin={}&destination={}&depart_date={}&return_date={}&currency=EUR'.format(iata_dep, iata_ar,
                                                                                         time_dep, time_ar),
        'access_token': api_token
    }
    query = '{domain}?{fields}&token={access_token}'.format(**query_params)
    response = requests.get(query)

    tickets = response.json()['data']['{}'.format(iata_ar)]
    suitable_fl = 'None'
    for item in tickets.keys():
        if suitable_fl == 'None':
            suitable_fl = tickets[item]
        elif tickets[item]['price'] < suitable_fl['price']:
            suitable_fl = tickets[item]

    return suitable_fl

def check(city): 
    with open('IATA.csv') as data: 
        reader = csv.DictReader(data) 
        iata_codes = list(reader) 
    for i in range(len(iata_codes)): 
        if city == iata_codes[i]['name']: 
            return True 
    return False

def start(resp):
    with open('IATA.csv') as data:
        reader = csv.DictReader(data)
        iata_codes = list(reader)

    iata_dep, iata_ar = '', ''
    for i in range(len(iata_codes)):
        if iata_codes[i]['name'] == resp['departure']:
            iata_dep = iata_codes[i]['code']
        elif iata_codes[i]['name'] == resp['arrival']:
            iata_ar = iata_codes[i]['code']
        elif iata_dep != '' and iata_ar != '':
            break

    i = 0

    ticket = get_ticket(resp['status'],iata_dep, iata_ar, resp['time_dep'], resp['time_ar'])
    return ticket


