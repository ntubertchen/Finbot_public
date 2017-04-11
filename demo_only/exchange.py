import requests

#country12 are string
def exchange(country1, country2):
    r=requests.get('https://tw.rter.info/capi.php')
    currency=r.json()
    if country1 == 'USD':
        q = country1 + country2
        return float(currency[q]['Exrate'])
    elif country2 == 'USD':
        q = country2 + country1
        return 1 / float(currency[q]['Exrate'])
    else:
        q1 = 'USD' + country1
        q2 = 'USD' + country2
        return float(currency[q2]['Exrate']) / float(currency[q1]['Exrate'])

exchange('EUR', 'USD')