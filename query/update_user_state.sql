INSERT INTO user_state
(user_login, user_state)
VALUES (%(login)s, %(state)s)
ON CONFLICT (user_login) DO UPDATE
SET user_state = %(state)s
RETURNING TRUE;