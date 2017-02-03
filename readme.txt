Lab1.py contains the brute force cracking of a MT seeded with a unix epoch timestamp.

MT19937-password-reset contains the admin password reset code. Almost all of the work is done in crack.py. Simply boot up the web server. Sign up for an account (has to have username 'minnal'). Then run crack.py to request 78 tokens, recreate the MT and ask for the next token. Once that is done, request an admin reset and navigate to the forgot password url with the new token as part of the query string and you should be prompted to input the admin's new password!
