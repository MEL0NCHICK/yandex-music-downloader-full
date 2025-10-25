import requests
from download import download_file

token = "YOU_TOKEN" #Ваш Oauth токен, где его взять: https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781

if token == "YOU_TOKEN" or "":
    print('Замените token = "YOU_TOKEN" в main.py на ваш Oauth токен, где его взять? -> https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781')

#print("Название трека: это называется любовь")
print("Скрипт from MEL0NCHICKС ищет преимущественно именно по названию трека, и скачивает песню полностью)))")
search_text=input("Введите название трека или исполнителя: ")
search_count=input("Введите кол-во результатов поиска (сколько будет найдено): ")
search_url=f"https://api.music.yandex.ru/search/instant/mixed?text={search_text}&type=track&page=0&pageSize={search_count}"

result = requests.get(url=search_url).json()

tracksid = []
tracksnames = []
q=1
print("   Название - Автор ")
for i in result['result']['results']:
    trackid = i['track']['id']
    print("-"*50)
    print(q, "Найдено: ", i)
    name=i['track']['title'] + " - " + i['track']['artists'][0]['name']
    print(q, " ", name, "  |  ID трека: ", trackid, "  |  ID автора: ", i['track']['artists'][0]['id'])
    tracksnames.append(name)
    tracksid.append(trackid)
    q+=1


choise_track = int(input("Выберите номер трека который будет скачан: "))-1

actual_track = tracksid[choise_track]
filename = (tracksnames[choise_track]+".mp3")

invalid_chars = '<>:"/\\|?*'

for char in invalid_chars:
    filename = filename.replace(char, " ")

print("Скачиваем: ", actual_track, filename)

download_file(actual_track, filename, token)


