import os
import re
import time

from playwright.sync_api import sync_playwright

start_time = time.time()

class HowLongToBeatAutomation:
    def __init__(self, chrome_path, username, password):
        self.chrome_path = chrome_path
        self.username = username
        self.password = password
        self.browser = None
        self.page = None
        # Exception titles to be handled, Key is the wrong title and Value is the correct title
        self.exception_titles = {
            "Fallout Classic Collection": "Fallout Classic",
            "Fallout 2 A Post Nuclear Role Playing Game": "Fallout 2",
            "Saints Row IV ReElected": "Saints Row IV Re-Elected",
            "YookaLaylee": "Yooka-Laylee",
            "Heroes & Generals WWII": "Heroes & Generals",
            "Trackmania Starter Access": "Trackmania",
            "YookaLaylee and the Impossible Lair": "Yooka-Laylee and the Impossible Lair",
            "Lacuna A Sci Fi Noir Adventure": "Lacuna",
            "Tomb Raider 1": "Tomb Raider",
            "Mortal Kombat 2": "Mortal Kombat II",
        }
        
        self.checkbox_map = {
            "Replays": "lists.replay",
            "Backlog": "lists.backlog",
            "Playing": "lists.playing",
            "Custom Tab": "lists.custom",
            "Completed": "lists.completed",
            "Retired": "lists.retired"
        }

    def setup(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(executable_path=self.chrome_path, headless=False)
        self.page = self.browser.new_page()

    def login(self):
        self.page.goto("https://howlongtobeat.com/login")
        self.page.wait_for_url("https://howlongtobeat.com/login", timeout=10000)

        self.page.fill('input[name="user_name"]', self.username)
        self.page.fill('input[name="password"]', self.password)

        print("Please solve the reCAPTCHA manually and press Enter to continue...")
        input("Press Enter once reCAPTCHA is completed...")

        self.page.click('input[type="submit"].form_button.back_blue')
        self.page.wait_for_url("https://howlongtobeat.com/user/" + self.username, timeout=10000)
        print("Login successful!")

    def search_game(self, game_name):
        self.page.goto("https://howlongtobeat.com/submit")
        self.page.wait_for_load_state('domcontentloaded')
        
        game_name = re.sub(r'(\(.*?\)|Deluxe Edition.*|HD.*|Gold Edition.*|GOTY.*|GOG Cut.*|Standard Edi.*|HISTORY EDITION.*|History Edition.*|Sovereign Edition.*|Definitive Edition.*|Digital Edit.*|Celebration Edi.*|Game of the Year.*|Special Edition.*|GAME OF THE YEAR EDITION.*|Plus Edition.*|Legacy Collection.*|Enhanced Plus Edition.*|Premier Edition.*|Complete Edition.*|ULTIMATE BUNDLE.*|Classic Edition.*|[^\w\s.,&]|(?<!\w)\.(?!\w)|\.{2,})', ' ', game_name)
        
        game_name = re.sub(r'\s{2,}', ' ', game_name).strip()

        game_name = self.exception_titles.get(game_name.strip(), game_name.strip())
        
        if any(keyword in game_name for keyword in ['Bundle', 'DLC', 'Pack', 'Kit', 'Skulls Digital Goodies', 'Goodies Collection', 'Playable Teaser', 'Alpha Version']):
            print("It's Not a Game! ---> ", game_name)
            return 'Not Game'
        
        self.page.fill('input.back_form.form_text[aria-label="Submission Search"]', game_name)
        
        try:
            self.page.wait_for_selector("div.in.spreadsheet", state="visible", timeout=5000)
            first_element = self.page.locator("div.in.spreadsheet").first
            
            if first_element.count() > 0:
                first_element.locator("a").click()
                print("Game found! ---> ", game_name)
                return 'Found'
            else:
                raise ValueError("Game not found in the list.")
        except Exception as e:
            print(f"No game found (error): {e} ---> {game_name}")
            return 'Not Found'
    
    def add_game_to_list(self, game_data):
        platform_select = self.page.locator('select[aria-label="Platform"]')
        platform_select.select_option(game_data['platform'])
        
        storefront_select = self.page.locator('select[aria-label="Storefront"]')
        storefront_select.select_option(game_data['store'])
        
        checkbox_name = self.checkbox_map[game_data['list']]
        self.page.click(f"input[name='{checkbox_name}']")
        self.page.click("input[name='playthrough-submit']")

        self.page.wait_for_url("https://howlongtobeat.com/submit?mode=new", timeout=5000)
        print("Game added to list ---> ", game_data['name'])

    def cleanup(self):
        if self.browser:
            self.browser.close()

if __name__ == "__main__":
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # Replace with your path
    username = "YOUR USER"  # Replace with your username
    password = "YOUR PASSWORD"  # Replace with your password
    game_list_path = "game_list.txt"  # Replace with the path to your file
    temp_file_path = game_list_path + ".tmp" # Temporary file path
    
    hltb = HowLongToBeatAutomation(chrome_path, username, password)
    try:
        hltb.setup()
        hltb.login()
        
        # Read and process the file into a list of dictionaries
        with open(game_list_path, encoding="utf-8") as file, open(temp_file_path, 'w', encoding="utf-8") as temp_file:
            games = [{"name": name, "platform": platform, "store": store, "list": list_name} for line in file if line.strip() for name, platform, store, list_name in [line.strip().split("|")]]
            
            for game in games:
                existence = hltb.search_game(game['name'])
                temp_file.write(f"{game['name']}|{game['platform']}|{game['store']}|{game['list']}|{existence}\n")
                
                if existence == 'Found':
                    hltb.add_game_to_list(game)
        os.replace(temp_file_path, game_list_path)
    finally:
        hltb.cleanup()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken: {execution_time:.2f} seconds")
