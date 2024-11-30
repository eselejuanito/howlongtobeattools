# howlongtobeattools
Project to help to add your library from gog and epic games to howlongtobeat page

1. Register on HowLongToBeat and get user and password.
https://howlongtobeat.com/
2. Download python
https://www.python.org/downloads/
    pip install playwright
3. Download this project
4. Activate your virtual environment
    python -m venv venv
    .\venv\Scripts\activate
5. Install the playwright
    pip install playwright
6. You need to add your user, password and chrome path in the file app.py
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # Replace with your path
    username = "YOUR USER"
    password = "YOUR PASSWORD"
7. Get the games from gog and epic games or add games manually in the game_list.txt
    epic_games.js: Login in epic games page and then go to this page. Run the epic_games.js content in the console
https://www.epicgames.com/account/transactions?lang=en-US&productName=egs
    gog_games.js: Login in gog page and then go to this page. Run the gog.js content in the console
https://www.gog.com/en/account
8. Add the games to game_list.txt in the format
    Game Name|Where you play|Platform|List in howlongtobeat
9. Run the app.py. When the script add user and password, you need to fill the captcha, then return to the console and press enter to continue with the script