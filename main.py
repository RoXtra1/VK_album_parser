import math
import os
import requests
import vk_api
from configparser import ConfigParser


def create_config():
    """ Создание и чтение файла конфигурации """
    cfg = ConfigParser()
    config_file = "Configuration.ini"

    if not os.path.exists(config_file):
        cfg.add_section("Configuration")
        cfg.set("Configuration", "Token", "token")  # публичный токен-ключ для авторизации
        cfg.set("Configuration", "Root", "root")  # адрес корневой папки, куда требуется скачивать

        with open(config_file, "w") as config_file:
            cfg.write(config_file)
    cfg.read("Configuration.ini", encoding='utf-8')

    return cfg


def authorization():
    """ Авторизация в вк через токен """
    try:
        vk_session = vk_api.VkApi(token=TOKEN)
        print('Авторизован!')

        return vk_session.get_api()
    except vk_api.AuthError as error_msg:
        print(error_msg)

    return None


def link_read(link: str, path: str):
    """ Функция обработки ссылки и создания папок под альбом """
    global VK   # для повторной авторизации
    print(f'Обрабатываю ссылку {link}')
    group_id = link.split('/')[-1].split('_')[0].replace('album', '')
    album_id = link.split('/')[-1].split('_')[1]

    try:
        album = VK.photos.getAlbums(owner_id=group_id, album_ids=album_id)['items'][0]
    except requests.exceptions.ConnectionError:  # после скачивания 3-4х альбомов апи отключается
        print('Попытка переподключения...')
        VK = authorization()  # повторная авторизация
        album = VK.photos.getAlbums(owner_id=group_id, album_ids=album_id)['items'][0]

    photos_count = album['size']

    album_dir = f"{path}\\{album['title'].rstrip('.').replace('/', '-')}"  # В названии папок нельзя использовать . и /
    if not os.path.exists(album_dir):
        os.mkdir(album_dir)

    print(f"Скачиваю {album['title']} ({photos_count} шт.)...")

    # Подсчитываем, сколько раз нужно получать список фото, т.к. 1000 фото - максимум для одного запроса.
    # Число получится не целое - округляем в большую сторону
    for j in range(math.ceil(photos_count / 1000)):
        try:
            photos = VK.photos.get(owner_id=group_id, album_id=album_id, count=1000,
                                   offset=j * 1000)['items']  # Получаем 1000 фото
        except requests.exceptions.ConnectionError:  # на случай, если фото больше 1000 и между подходами был дисконект
            print('Переподключение...')
            VK = authorization()  # повторная авторизация
            photos = VK.photos.get(owner_id=group_id, album_id=album_id, count=1000,
                                   offset=j * 1000)['items']
        counter = 1 + j * 1000

        for photo in photos:
            biggest = 0
            biggest_src = ''

            if counter % 10 == 0 or counter == photos_count:
                print(f'Загружаю {counter} из {photos_count}...')

            for size in photo['sizes']:  # Получаем наибольшее разрешение
                if size['width'] > biggest:
                    biggest = size['width']
                    biggest_src = size['url']  # сохраняем ссылку на фото с наибольшим разрешением
            content = requests.get(biggest_src).content

            try:
                with open(f"{album_dir}\\{str(counter)}.jpg", "wb") as f:
                    f.write(content)
            except (FileNotFoundError, NotADirectoryError, OSError) as e:
                print(f"Ошибка с файлом - {e}")
                continue

            counter += 1
    print(f'Альбом полностью загружен в {path}\n')


def file_work(file_name: str):
    """ Функция считывания списка ссылок из файла """
    with open(file_name, "r", encoding='utf-8') as f:  # открываем файл, сохраняем список строк из него
        content = f.readlines()

    res = []
    start = 0
    for i in range(len(content)):
        if content[i] == '\n':
            end = i  # start и end это границы разделов, которые объединятся в папки
            res.append(content[start:end])

            if end + 1 <= len(content):
                start = end + 1
        elif i == len(content) - 1:
            res.append(content[start:])
        content[i] = content[i].rstrip()  # очистка от знаков переноса строки

    for dr in res:  # проходимся по каждому разделу
        base_dir = ''
        sub_dir = ''

        for line in dr:  # затем по каждой линии в разделе
            if line.startswith('http'):  # если ссылка
                path = f'{ROOT}{base_dir}{sub_dir}'
                link_read(line, path)
            elif line.startswith('-'):  # если название подраздела
                sub_dir = '\\' + line[1:]
            else:  # если название раздела
                base_dir = '\\' + line


def main():
    if VK:
        ans = int(input('Выбери способ ввода:\n0 - вставить ссылку\n1 - читать список ссылок из файла\n->'))
        if ans == 0:
            link = input('Вставь ссылку на альбом: ')
            link_read(link, ROOT)
        else:
            file = input('Вставь название файла или путь к нему: ')
            file_work(file)
    else:
        print("Не авторизован :( Попробуй еще раз")
    print('Загрузка завершена')


if __name__ == "__main__":
    config = create_config()
    TOKEN = config.get("Configuration", "Token")
    ROOT = config.get("Configuration", "Root")
    VK = authorization()
    main()
