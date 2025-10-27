import requests
from download import download_file

token = "y0__xCU6tyZBhje-AYgtI-e6xTu4ghvMYZaGLWvVdt-jNBssdvh7Q" #Ваш Oauth токен, где его взять: https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781

if token == "YOU_TOKEN" or "":
    print('Замените token = "YOU_TOKEN" в main.py на ваш Oauth токен, где его взять? -> https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781')
    exit()

#print("Название трека: это называется любовь")
print("Скрипт from MEL0NCHICKС ищет преимущественно именно по названию трека, и скачивает песню полностью)))")
#search_text=input("Введите название трека или исполнителя: ")
#search_count=input("Введите кол-во результатов поиска (сколько будет найдено): ")

def search(search_text: str, search_count):
    search_url=f"https://api.music.yandex.ru/search/instant/mixed?text={search_text}&type=track&page=0&pageSize={search_count}"
    result = requests.get(url=search_url).json()

    text_for_ai = ""
    tracksid = []
    tracksnames = []
    q=1
    print("   Название - Автор ")
    for i in result['result']['results']:
        trackid = i['track']['id']
        text_for_ai += f"{"-" * 50}\n"
        text_for_ai += f"{q, 'Найдено: ', i}\n"
        name=i['track']['title'] + " - " + i['track']['artists'][0]['name']
        text_for_ai +=  name + "\n"
        tracksnames.append(name)
        tracksid.append(trackid)
        q+=1
    return [tracksid, tracksnames, text_for_ai]

results = search(input("Введите название трека или исполнителя: "), input("Введите кол-во результатов поиска (сколько будет найдено): "))

print(results[2])

choise_track = int(input("Выберите номер трека который будет скачан: "))-1

actual_track = results[0][choise_track]
filename = (results[1][choise_track]+".mp3")

invalid_chars = '<>:"/\\|?*'

for char in invalid_chars:
    filename = filename.replace(char, " ")

print("Скачиваем: ", actual_track, filename)
download_file(actual_track, filename, token)
