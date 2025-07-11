import urllib.request

for i in range(0,50,1):
    data=''
    with urllib.request.urlopen(f"https://mercaapi.sgn.space/api/products/?limit=100&skip={i*100}") as url:
        data=url.read().decode('utf-8')
    with open(f"/local/products_backup/products{("0"+str(i))[-2:]}.json", "w") as file:
        file.write(data)