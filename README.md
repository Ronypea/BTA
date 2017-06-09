# BTA
Business trip assistant: We make business easier

### Суть проекта
Мы разработали помощника по планированию командировок. 
В нашем приложении пользователю необходимо зарегистрироваться, подтвердить регистрацию, перейдя по ссылке на почте, после чего ему предоставляется возможность ввести данные по командировкам: время поездки, города, встречи и многое другое. После этого программа обрабатывает данные и присылает пользователю информацию об удобном ему авиарейсе и отеле (в зависимости от его предпочтений и расположения офиса, который вбит в базу), а также автоматически заполняется Google календарь данными событиями. 

### Реализация

#### Веб-интерфейс приложения
Приложение, с которым работает пользователь, находится на платформе Django REST. 
Была прописана куча шаблонов с использованием html и css (как с сайта maxcdn.bootstrapcdn.com для форм, так и собственного для всего остального).

#### Поиск авиабилетов
Авиабилеты (как и отели) находятся с помощью Travelpayouts – туристической партнерской сети. После регистрации на данном ресурсе предоставляется токен API доступа к данным.
Билет ищется либо по удобству (без пересадок), либо по цене (самый дешевый) и находится в режиме реального времени. Билет можно находить с помощью requests, а можно с помощью http.client (в работе реализовано и так, и так).

К сожалению, для API поиска билетов (что является более удобной базой) требуется писать заявку в поддержку ресурса, объясняя цель получения такого токена. Нам, конечно же, его никто не дал… Поэтому не удалось отправлять пользователю ссылку на покупку билета.

Еще одна проблема, с которой мы столкнулись: для запросов требуется знать IATA городов, но никаких полных готовых баз, нет. И с помощью интернет-ресурса http://iatacodes.org/  мы её создали сами: получив на их сайте токен API, можно сделать request запрос и получить такую базу, что представлена ниже. После чего мы её построчно преобразовали в csv файл (см. get_IATA.py).
![](https://github.com/Ronypea/BTA/raw/master/База.png)

#### Поиск отеля
Для поиска отеля требуется тот же токен API, что и для поиска авиабилетов. Отель находится в 3 этапа:
1)	В зависимости от адреса офиса находятся все удобные отели (поиск отелей по координатам через request запрос).
Адреса в координаты переводятся с помощью библиотеки geopy. 
Пример перевода адреса в координаты:
Если координаты адреса невозможно определить, то определяются координаты города (его центр) и отель ищется по ним.
2)	С помощью двух других request запросов мы находим всю информацию про данные отели (количество звёзд, цена, некоторые имеют фотографии и ссылку на сайт).
3)	В зависимости от предпочтений пользователя находится один наиболее подходящий отель.

#### Google календарь
Перед началом работы с токенами Google API надо создать свой проект на Google Platform и связанные с ним учетные данные: идентификатор клиентов OAuth 2.0.
После этого мы получаем файл client_secret.json, в котором хранятся все данные по проекту (id клиента, проекта, токены и тд) и с помощью которого будет устанавливаться доступ приложения к календарю пользователя. 

Мы используем подбиблиотеку Oauth2client, которая обрабатывает все шаги протокола, необходимые для выполнения вызовов API. И вся программа делится на две ступени: получение доступа и работа с календарём. 
1)	Функция get_credentials(): получение полномочий для работы с google календарем. В ней используется класс Flow для приобретения учётных данных и авторизации приложения доступа к данным пользователя, вынимая данные из client_secret.json и преобразовывая их (создавая flow-объекты).  
2)	Функция main: непосредственное создание, удаление и редактирование событий, занесение их в google таблицу. 
Для работы с google таблицами создается service-объект (discovery.build()). А для создания события требуется словарь «event», в котором ключ – нужный параметр, а значение – его содержание. При создании события ему присваивается id, благодаря которому происходит удаление или редактирование конкретно этого события.

Когда новый аккаунт создает свою первую запись, то сначала надо разрешить доступ приложения к данным календаря, после чего это не требуется.

### Пример работы программы
![image_alt](https://user-images.githubusercontent.com/29158476/26972194-60b50cb6-4d19-11e7-9efd-4f439c7c8d94.jpg)
![image alt](https://user-images.githubusercontent.com/29158476/26972193-60b2f28c-4d19-11e7-900b-4bacb7cd5462.jpg)
![image_alt](https://user-images.githubusercontent.com/29158476/26972195-60b43dae-4d19-11e7-85bd-65300658c837.png)
![image_alt](https://user-images.githubusercontent.com/29158476/26972196-60bf7098-4d19-11e7-8d19-19b155c43bf4.png)


