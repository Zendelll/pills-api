# pills api
Личный проект, в котором впервые подняла свою апишку
Идея для проекта мне пришла, когда мне понадобилось пить несколько разных лекарств очень долгое время, но кончались они в разное время. Чтобы не забывать купить их и не было надобности считать в уме, я решила автоматизировать эту проблему с:

Фактически это бэкенд, который реализует всю логику. Интерфейс я реализовала в соседнем проекте - https://github.com/Zendelll/pills-bot, где он представляет из себя телеграм бота, но реализация может быть абсолютно любой, пока она ходит в эту апишку

## Описание методов
### GET /pills/get_me
Получить всю информацию о пользователей
login - логин юзера
### PUT /pills/user_state
Изменить user_state - статус юзера в тг боте
login - логин юзера
state - новый стейт
### GET /pills/pills_count
Посчитать до какого числа осталось таблеток
login - логин юзера
### GET /pills/pills_safe_count
Посчитать до какого числа хватит таблеток, если добавить add_pills таблеток к текущим
login - логин юзера
name - название препарата
add_pills - сколько таблеток добавится
### PUT /pills/set_med
Добавить новый препарат
login - логин юзера
name - название препарата
count - количество таблеток
pills_use - количество таблеток в день
### POST /pills/add_pills
Добавить таблетки
login - логин юзера
name - название препарата
count - количество новых таблеток
### DELETE /pills/delete_med
Удалить препарат
login - логин юзера
name - название препарата
