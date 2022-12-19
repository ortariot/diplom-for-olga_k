import requests
from n_token import token_group, token_my
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json
import re



PROTOCOL_VERSION: str = "5.131"

session = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(session)

def write_msg(user_id, message, attachment=None):
    session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachment})

def user_info(user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
             "access_token": token_my,
             "v": PROTOCOL_VERSION,
             "fields": "sex,bdate,city,relation",
             "user_ids": user_id
    }
    response = requests.get(url, params=params)
    result = response.json()
    for i in result["response"]:
        return i


def user_aggregation(city_s, sex_s, age_from, age_to,relation_s):
    profiles = user_search(city_s, sex_s, age_from, age_to,relation_s)
    profile_list = []
    for profile in profiles:
        if profile['is_closed'] == False:
            profile_list.append(profile)
    return profile_list



def user_search(city_s, sex_s, age_from, age_to,relation_s):
    url = "https://api.vk.com/method/users.search"
    params = {
             "access_token": token_my,
             "v": PROTOCOL_VERSION,
             "sort": 0,
             "city": city_s,
             "sex": sex_s,
             'age_from': age_from,
             'age_to': age_to, 
             "status": relation_s,
             "has_photo": 1,
             "count": 100
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['response']['items']
    else:
        return None


def select_random(r):
    list = []
    result = r["response"]["items"]
    for item in result:
        list.append(item["id"])
    result2=random.sample(list, k=1)
    for i in result2:
        return i


def get_foto(id_user_search):
    url = "https://api.vk.com/method/photos.get"
    params = {
             "access_token": token_my,
             "v": PROTOCOL_VERSION,
             "owner_id": id_user_search,
             "album_id": "profile",
             "extended": "1",
             "need_like": "1"

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['response']['items']
    else:
        return None

def popular_foto(r):
    r.sort(reverse=True, key=lambda item: (item["likes"]["count"], item["comments"]["count"]))
    r1 = r[:3]
    list = []
    for item in r1:
        list.append(item["id"])
    return list

def data_year(n):
    search = re.search('(\d{4})', n)
    return search.group()


def send_photo(user_id, owner_id, r):
    for i in r:
        foto = f'photo{owner_id}_{i}'
        session.method('messages.send', {'user_id': user_id, 'attachment': foto, 'random_id': randrange(10 ** 7), })

def sex_change(n):
        if n == 2:
            result = 1
        else:
            result = 2
        return result

def relation_check(n):
    if n == "не женат" or n == "не замужем":
        status=1
    elif n=="есть друг" or n == "есть подруга":
        status = 2
    elif n=="помолвлен" or n == "помолвлена":
        status = 3
    elif n=="женат" or n == "замужем":
        status = 4
    elif n=="все сложно":
        status = 5
    elif n=="в активном поиске":
        status = 6
    elif n=="влюблён" or  n == "влюблена":
        status = 7
    elif n=="в гражданском браке":
        status = 8

def city_id(n):
    url = "https://api.vk.com/method/database.getCities"
    params = {
        "access_token": token_my,
        "v": PROTOCOL_VERSION,
        "country_id": 1,
        "q": n,
        "need_all": 0,
        "count": 1
    }
    response = requests.get(url, params=params)
    result = response.json()
    for i in result["response"]["items"]:
        result = i["id"]
        return result




