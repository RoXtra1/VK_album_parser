Бесплатный рабочий парсер для скачивания альбомов с фотографиями из ВК с возможностью работы с неограниченным списком ссылок.
A free working parser for downloading photo albums from VK with the ability to work with an unlimited list of links. 
if you need the English version, use your browser's auto-translator, or pm me.

Для авторизации использовался рекомендуемый ВК способ через VK_ID и получение токена доступа из зарегистрированного приложения
(да, по другому, к сожалению, никак).

Инструкция по работе с программой:
1) Регистрируем приложение https://dev.vk.com/ru/mini-apps/getting-started#Регистрация%20мини-приложения%20ВКонтакте
2) Получаем публичный токен в настройках приложения
3) Запускаем программу в первый раз. Не выбирая ничего прерываем выполнение.
4) Открываем созданный файл конфига в папке с программой и вписываем в него свой токен вместо token после "="
   и полный адрес корневой папки для скачивания (в ней будут появляться все папки и альбомы) вместо root после "=".
   В адресе не нужно дублировать слеши для экранирования. Сохраняем файл
5) запускаем программу и выбираем необходимую опцию: 0 - сохранение по ссылке на конкретный альбом
                                                     1 - сохранение из файла
5.0) вставляете ссылку и получаете в корневой папке альбом
5.1) вставляете название текстового файла вместе с раширением (пример - links_list.txt)
6) получаете папку с альбомами

Для работы с файлом его нужно правильно подготовить:
Он должен содержать все названия и ссылки на отдельных строках, 
названия крупных разделов должны быть в виде обычного текста ("Название"), 
названиия подразделов должны быть в виде "-Название", 
ссылки на альбомы никак отдельно помечать не надо,
ссылкина альбомы, которые должны лежать в папке раздела, а не подраздела, должны располагаться до первого названия подраздела
разделы отделяются друг от друга пустой строкой.

итоговый файл будет выглядеть примерно так:
*links_list.txt*
Название_раздела1
ссылка1
ссылка2
-Название_подраздела1
ссылка1
ссылка2
-Название_подраздела2
ссылка1

Название_раздела2
ссылка1
ссылка2
ссылка3
-Название_подраздела1
ссылка1
ссылка2
ссылка3

Название_раздела3
-Название_подраздела1
ссылка1
ссылка2