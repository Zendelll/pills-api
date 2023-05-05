INSERT INTO pill_users
(user_login, med_name, amount, daily_usage)
VALUES (%(login)s, %(med_name)s, %(amount)s, %(daily_usage)s)
ON CONFLICT ON CONSTRAINT unique_pill DO UPDATE
SET amount = %(amount)s, daily_usage = %(daily_usage)s, last_count_date = current_date
RETURNING TRUE;