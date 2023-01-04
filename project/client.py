import requests

""" URL = "http://127.0.0.1:8000/api/v1/reviews"
HEADERS = {"accept": "application/json"}
QUERYSET = {"page": 1, "limit": 2}

response = requests.get(URL, headers=HEADERS, params=QUERYSET)

if response.status_code == 200:
    print("😎 OK")

    if response.headers.get("content-type") == "application/json":
        reviews = response.json()
        for review in reviews:
            print(f"score: {review['score']} - {review['review']}")
 """

""" URL = "http://127.0.0.1:8000/api/v1/reviews"
REVIEW = {"user_id": 1, "movie_id": 4,
          "review": "Creada con request", "score": 5}

response = requests.post(URL, json=REVIEW)

if response.status_code == 200:
    print("OK 😜")

print(response.content) """

""" REVIEW_ID = 10
URL = f"http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}"
REVIEW = {"review": "review actualizada en requests", "score": 1}

response = requests.put(URL, json=REVIEW)

if response.status_code == 200:
    print("OK 😎")
    print(response.json()) """

""" REVIEW_ID = 9
URL = f"http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}"

response = requests.delete(URL)

if response.status_code == 200:
    print("OK 😎") """

URL = "http://127.0.0.1:8000/api/v1/users/"
USER = {"username": "oscar26", "password": "123456"}

response = requests.post(URL + "login", json=USER)

if response.status_code == 200:
    print("😎 OK")

    user_id = response.cookies.get_dict().get("user_id")

    cookies = {"user_id": user_id}
    response = requests.get(URL + "reviews", cookies=cookies)

    if response.status_code == 200:
        for review in response.json():
            print(f"{review['review']} - {review['score']}")
