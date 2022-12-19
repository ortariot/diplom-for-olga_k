import random
from n_token import*
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot_function import*
import requests
from database import*


translator = { 'relation': 'семейное положение',
               'bdate': 'возраст',
               'city': 'город'
              }



def gender_convert(gender):
    return 1 if gender == 2 else 2

def age_range(bdate, params = 'from'):
    year = int(bdate.split('.')[2])
    '''пишу здесь 2022, вапм нужно функцию сделать которая сама будет год определять'''
    return 2022 - year - 5 if params == 'from' else 2022 - year + 5


bot="start"
requaries = []
params = {}
profile_list = []


def photo_process(user_id, profile_id):
    photos = get_foto(profile_id)
    print(photos)
    cnt = 0
    for photo in photos:
        cnt += 1
        link = f'photo{profile_id}_{photo["id"]}'
        write_msg(user_id, f"фото {cnt}", attachment=link)
        
        if cnt == 3:
            break


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        if bot == "relation":
            if msg.isdigit():
                write_msg(event.user_id, f"Семейное положение - {msg} ")
                params["relation"] = msg
                if requaries:
                    bot = "cheking_params"
                    write_msg(user_id, f"В вашем профиле недостаточно парамтеров для поиска,")
                    write_msg(user_id, f"Введите {translator[requaries[0]]} ,")
                else:
                    bot = "params_ok"

        if bot == "bdate":
            if msg.isdigit():
                write_msg(event.user_id, f"Год рождения {msg} записан")
                params["bdate"] = msg
            else:
                write_msg(event.user_id, "Укажи год рождения цифрами")
            if requaries:
                bot = "cheking_params"
                write_msg(user_id, f"В вашем профиле недостаточно парамтеров для поиска,")
                write_msg(user_id, f"Введите {translator[requaries[0]]} ,")
            else:
                bot = "params_ok"

        if bot == "city":
            if msg:
                write_msg(event.user_id, f"Город {msg} записан")
                params["city"] = msg
            if requaries:
                bot = "cheking_params"
                write_msg(user_id, f"В вашем профиле недостаточно парамтеров для поиска,")
                write_msg(user_id, f"Введите {translator[requaries[0]]} ,")
            else:
                bot = "params_ok"

        if bot == "photo_process":
            if msg == "далее":
                profile_id = profile_list.pop()['id']
                if profile_id:
                    photo_process(user_id, profile_id)
                    write_msg(user_id, f"что бы ппосмотреть следующую анкету напишите 'далее'")
                    bot = "photo_process"
                else:
                    bot = "start"
                    write_msg(user_id, f"найденные анкеты подошли к концу, что бы искать ещё пиши 'да'")


        if bot == "start":
            if msg == "привет":
                write_msg(user_id, "Чат-бот VKinder приветствует тебя. Давай найдем тебе пару! Чтобы начать, напиши - да")
                continue
            if msg == "да":
                write_msg(user_id,"Отлично! Начнем поиск!")
                informathion = user_info(user_id)
                print(informathion)
                if "relation" not in informathion.keys():
                    requaries.append("relation")
                else:
                    bot = "cheking_params"

                if "bdate" not in informathion.keys():
                    requaries.append("bdate")
                else:
                    bot = "cheking_params"

                if "city" not in informathion.keys():
                    requaries.append("city")
                else:
                    bot = "cheking_params"
                
                if requaries:
                    write_msg(user_id, f"В вашем профиле недостаточно парамтеров для поиска,")
                    write_msg(user_id, f"Введите {translator[requaries[0]]}")
                else:
                    profile_list = user_aggregation(informathion['city']['id'],
                                                    gender_convert(informathion['sex']),
                                                    age_range(informathion['bdate']),
                                                    age_range(informathion['bdate'], params = 'to'),
                                                    6)
                    '''ставлю статус 6, вы можете придумать какую-нибудь функцию для определения статуса'''
                    if len(profile_list) > 0:
                        profile_id = profile_list.pop()['id']
                        photo_process(user_id, profile_id)
                        write_msg(user_id, f"что бы ппосмотреть следующую анкету напишите 'далее")
                        bot = "photo_process"


        if bot == "cheking_params":
            if requaries:
                param = requaries.pop()
                write_msg(user_id, f"Укажите {param}")
                bot = param
                continue
            else:
                bot = "params_ok"
                continue


        if bot == "params_ok":
            profile_list = user_aggregation(informathion['city']['id'],
                                            gender_convert(informathion['sex']),
                                            age_range(informathion['bdate']),
                                            age_range(informathion['bdate'], params = 'to'),
                                            6)
            '''ставлю статус 6, вы можете придумать какую-нибудь функцию для определения статуса'''
            if len(profile_list) > 0:
                profile_id = profile_list.pop()['id']
                photo_process(user_id, profile_id)
                write_msg(user_id, f"что бы ппосмотреть следующую анкету напишите 'далее")
                bot = "photo_process"




            # write_msg(user_id, f"Получены данные для поиска {params}")
            # bot = "start"
            # print(params)
            # print(requaries)
            # city_user=1
            # status=0
            # data_y=2000
            # #city_user=city_id("")
            # sex_u = sex_change(informathion["sex"])
            # # #status= relation_check("")
            # searh_user= user_search(city_user, sex_u, data_y, status)
            # select_search= select_random(searh_user)
            # while check_form(conn, user_id,select_search):
            #     select_search= select_random(searh_user)
            # else:
            #     add = add_form(conn, user_id, select_search)
            #     foto = get_foto(select_search)
            #     foto_popular= popular_foto(foto)
            #     send_photo(user_id,select_search,foto_popular)
            #     write_msg(user_id, f"Хочешь познакомиться - лови ссылку  https://vk.com/id{select_search}")
            #     write_msg(user_id, f"Хочешь продолжить, напиши - да")
            # if msg == "нет":
            #     write_msg(event.user_id, "Пока")

