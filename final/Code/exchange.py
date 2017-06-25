import requests

#country12 are string
def exchange(country1, country2):
    r=requests.get('https://tw.rter.info/capi.php')
    currency=r.json()
    if country1 == 'USD':
        q = country1 + country2
        if currency.get(q) == None:
            return str("No "+q+"in exchange dict")
        return float(currency[q]['Exrate'])
    elif country2 == 'USD':
        q = country2 + country1
        if currency.get(q) == None:
            return str("No "+q+"in exchange dict")
        return 1 / float(currency[q]['Exrate'])
    else:
        q1 = 'USD' + country1
        q2 = 'USD' + country2
        if currency.get(q1) == None:
            return str("No "+q1+"in exchange dict")
        if currency.get(q2) == None:
            return str("No "+q2+"in exchange dict")
        return float(currency[q2]['Exrate']) / float(currency[q1]['Exrate'])

exchange('EUR', 'USD')