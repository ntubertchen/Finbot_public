import json
r=requests.get('https://tw.rter.info/capi.php')
currency=r.json()
kick = ['COPPERHIGHGRADE', 'GOLD1OZ', 'PALLADIUM1OZ', 'PLATINUM1UZ999', 'SILVER1OZ999NY']
Country = []
for a in currency:
    if a in kick:
        continue
    elif a == 'USD':
        Country.append(a)
        continue
    elif a.replace('USD','') == '':
        continue
    Country.append(a.replace('USD','')) 