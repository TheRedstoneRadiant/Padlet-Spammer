import requests, json
from bs4 import BeautifulSoup


BASE_URL = "https://padlet.com/"
PADLET_LINK = "kzezxhghus/cns0m5vgy7flm1cl"

soup = BeautifulSoup(requests.get(BASE_URL + PADLET_LINK).text, "html.parser")

user = json.loads(soup.select("[name=verify-v1]")[0].find("script").text.split("= ")[1])

print(
    f"""
Logged in as: {user["userRegistration"]} ({user["userId"]})
"""
)

padlet = requests.get(
    BASE_URL + soup.select("#starting-state-preload")[0]["href"]
).json()

print(
    f"""
"{padlet["wall"]["headline"]}" ({padlet["wall"]["id"]})
{padlet["wall"]["namespace"]} - {padlet["wall"]["name"]}

"""
)

padlet["wall"]["id"]
user["userId"]
