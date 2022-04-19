import requests
import string, random

def rnd_str():
    alph = string.hexdigits
    return "".join([random.choice(alph) for i in range(10)]).lower()

images = [
    [
        "679046356",
        "https://www.freeopenvpn.org/img/password.php?iPUfU7505", 
        "https://www.freeopenvpn.org/premium.php?cntid=Germany&lang=en"
    ],
    [
        "966187942",
        "https://www.freeopenvpn.org/img/password.php?3Ymspt528",
        "https://www.freeopenvpn.org/premium.php?cntid=USA&lang=en"
    ]
]


i = 0
while 1:
    try:
        ans, url, referer = images[i % 2]
        # ans, url, referer = images[0]
        page = requests.get(url, headers={"referer": referer}, timeout=2)
        with open(f"data/{ans}/{rnd_str()}.png", "wb") as f:
            f.write(page.content)
        i += 1
        print(i)
    except KeyboardInterrupt:
        break
    except:
        pass
