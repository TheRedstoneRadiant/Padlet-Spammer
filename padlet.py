import requests, json, random
from bs4 import BeautifulSoup


BASE_URL = "https://padlet.com/"
PADLET_LINK = "kzezxhghus/cns0m5vgy7flm1cl"


def post_padlet(token, wall_id, author_id, subject, body, index):
    return requests.post(
        "https://padlet.com/api/5/wishes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cid": "c_new4",
            "wall_id": wall_id,
            "published": True,
            "author_id": author_id,
            "width": 200,
            "body": body,
            "subject": subject,
            "attachment": "",
            "attachment_caption": None,
            "sort_index": index,
        },
    )


if __name__ == "__main__":
    with open("payload.json") as file:
        payload = json.load(file)

    soup = BeautifulSoup(requests.get(BASE_URL + PADLET_LINK).text, "html.parser")

    user = json.loads(
        soup.select("[name=verify-v1]")[0].find("script").text.split("= ")[1]
    )

    USER_ID = user["userId"]

    padlet = requests.get(
        BASE_URL + soup.select("#starting-state-preload")[0]["href"]
    ).json()

    WALL_ID = padlet["wall"]["id"]

    wishes = requests.get(
        f"https://api.padlet.com/api/5/wishes?wall_id={WALL_ID}"
    ).json()["data"]

    OAUTH_TOKEN = padlet["arvoConfig"]["token"]["oauthToken"]

    print(
        f"""
"{padlet["wall"]["headline"]}" ({padlet["wall"]["id"]})
{padlet["wall"]["namespace"]} - {padlet["wall"]["name"]}

Logged in as: {user["userRegistration"]} ({user["userId"]})
Token: {padlet["arvoConfig"]["token"]["oauthToken"]}
    """
    )

    i = 0
    while True:
        print(f"Count: {i}, Delivering payload", end="\r")

        r = post_padlet(
            OAUTH_TOKEN,
            WALL_ID,
            USER_ID,
            payload["subject"],
            payload["body"],
            random.choice(wishes)["attributes"]["sort_index"],
        )
        r.raise_for_status()
        i += 1
