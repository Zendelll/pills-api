# test-api
Тестирую свои возможности по запуску личной апишки. Вдруг не заброшу)

## Pills
Апишка для того, чтобы следить за таблетками
### GET /pills/get_me
Получить всю информацию о пользователей 
login - логин юзера
### GET /pills/pills_count
Посчитать до какого числа осталось таблеток  
login - логин юзера
### GET /pills/pills_safe_count
Посчитать до какого числа хватит таблеток, если добавить add_pills таблеток к текущим  
login - логин юзера  
name - название препарата  
add_pills - сколько таблеток добавится
### POST /pills/set_pill
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