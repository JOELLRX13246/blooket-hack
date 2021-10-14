import datetime
import requests
import time

authToken = "blooket token here"  # add your blooket token in string


def getName(token):
    r = requests.get('https://api.blooket.com/api/users/verify-token',
                     params={"token": f"{token}"})

    return r.json()["name"]


blooketName = getName(authToken)


def getLastTokenDate():
    r = requests.get(f"https://api.blooket.com/api/users?name={blooketName}")
    last_token_date = datetime.datetime.strptime(
        r.json()["lastTokenDay"], "%Y-%m-%dT%H:%M:%S.%fZ")
    date_now = datetime.datetime.strptime(
        datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%dT%H:%M:%SZ")
    account_created_date = r.json()["dateCreated"]

    return (last_token_date, date_now, account_created_date)


def getCreatedDate():
    r = requests.get(f"https://api.blooket.com/api/users?name={blooketName}")
    return datetime.datetime.strptime(r.json()["dateCreated"], "%Y-%m-%dT%H:%M:%SZ")


def addTokens():
    getData = getLastTokenDate()
    blooketName = getName(authToken)

    request_url = "https://api.blooket.com/api/users/add-rewards"
    request_data = {
        "name": blooketName,
        "addedTokens": 500,
        "addedXp": 300
    }

    if getData[0].day == getData[1].day + 1:
        try:
            r = requests.put(request_url, request_data, headers={
                             "authorization": authToken})
            print(f"Rewarded {blooketName} 500 tokens")
        except Exception as e:
            print(e)
    elif getData[0].day != getData[1].day + 1:
        print(f"{blooketName} has already earned max tokens in the past 24 hours!")
    elif (getCreatedDate().year, getCreatedDate().month, getCreatedDate().day) == (getData[1].year, getData[1].month, getData[1].day):
        try:
            r = requests.put(request_url, request_data, headers={
                             "authorization": authToken})
            print(f"Rewarded {blooketName} 500 tokens")
        except Exception as e:
            print(e)


while True:
    addTokens()
    time.sleep(86400000)
