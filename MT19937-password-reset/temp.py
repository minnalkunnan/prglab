import json

s = """<html>
        <head>
                <link href='static/calpoly.css' type='text/css' rel='stylesheet' />
                <title>Cal Poly Authentication (not really)</title>
        </head>
        <body>
                <div id='topRow'></div>
                <div id='fakeContainer'> </div>
                <div id='centerContainer'>
                        <img src='static/CP_Logo_Transparent.png' style='height: 70px;'><p>
                        <center>
                        <form name ='main' method='post'>
                                    <p><font color='black'> <!--open_token-->localhost:8080/reset?token=NDE3MjA2OTc5NTozNDMyNzA4ODU4OjIzMjgyOTYwNTg6MjU4MjkzODcwNToxMjQzOTg5NDc6MzE2Njk3OTI2NToyMjQwOTE3NTYwOjQyMjYwMTg4MDg=<!--close_token--> </font></p>
                                <table>
    <tr><th><label for='forgotUser'>Username</label></th><td><input id='forgotUser' name='user' type='text' value='minnal'/></td></tr>
    <tr><th><label for='Reset'></label></th><td><button id='Reset' name='Reset'>Reset</button></td></tr>
</table>
                        </form>
                        </center>
                        <a href="/">Return</a>
                </div>
                <div id='bottomRow'>
                        <center>
                        <b>Disclaimer</b>: 'This is not the real Cal Poly Authentication portal. Its probably not safe to enter your real Cal Poly username and password.'
                        </center>
                </div>
        </body>
</html>"""

for item in s.split("\n"):
   if "token" in item:
      line = (item.split("token="))[1]
      token = (line.split("<!--close_token-->"))[0]
      print(token)
