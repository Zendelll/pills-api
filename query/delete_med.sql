DELETE FROM pill_users
WHERE user_login = %(login)s AND med_name = %(med_name)s
RETURNING TRUE;