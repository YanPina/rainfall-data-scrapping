from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

class WebDriver:
    def __init__(
        self, 
        isHeadlessOn:bool=False, 
        isChangeDownloadFolder:bool=False, 
        newDownloadFolder:str=''
    ):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) #Remove unnecessary logs

        #User Agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
        self.options.add_argument(f'user-agent={user_agent}')

        if isHeadlessOn:
            self.options.add_argument('--headless') #Run Webdriver in background

        if isChangeDownloadFolder:
            prefs = {"download.default_directory" : f"{newDownloadFolder}"}
            self.options.add_experimental_option("prefs", prefs)

        self.__selenium_driver()


    def __selenium_driver(self): 
        service = Service(ChromeDriverManager().install())   
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.implicitly_wait(30)

        return self.driver
    
    def _get_url(self, url:str):
        self.driver.get(url)

    
    def _find_elements(self, element:str, find_method:str):
        match find_method:
            case 'ID':
                return self.driver.find_elements(By.ID, element)

            case 'NAME':
                return self.driver.find_elements(By.NAME, element)
        
            case 'XPATH':
                return self.driver.find_elements(By.XPATH, element)

            case 'TAG_NAME':
                return self.driver.find_elements(By.TAG_NAME, element)

            case 'LINK_TEXT':
                return self.driver.find_elements(By.LINK_TEXT, element)

            case 'CLASS_NAME':
                return self.driver.find_elements(By.CLASS_NAME, element)
        
            case 'CSS_SELECTOR':
                return self.driver.find_elements(By.CSS_SELECTOR, element)
        
            case 'PARTIAL_LINK_TEXT':
                return self.driver.find_elements(By.PARTIAL_LINK_TEXT, element)


    def _find_element(self, element:str, find_method:str):
        match find_method:
            case 'ID':
                return self.driver.find_element(By.ID, element)

            case 'NAME':
                return self.driver.find_element(By.NAME, element)
        
            case 'XPATH':
                return self.driver.find_element(By.XPATH, element)

            case 'TAG_NAME':
                return self.driver.find_element(By.TAG_NAME, element)

            case 'LINK_TEXT':
                return self.driver.find_element(By.LINK_TEXT, element)

            case 'CLASS_NAME':
                return self.driver.find_element(By.CLASS_NAME, element)
        
            case 'CSS_SELECTOR':
                return self.driver.find_element(By.CSS_SELECTOR, element)
        
            case 'PARTIAL_LINK_TEXT':
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, element)


    def _click_element(self, element:str, find_method:str) -> None:
        element = self._find_element(element, find_method)
        element.click()


    def _quit(self) -> None:
        self.driver.quit()

    
    def _send_text_in_element(self, element:str, find_method:str, text:str, submit:bool=False) -> None:
        element = self._find_element(element, find_method)
        element.send_keys(text)

        if submit:
            element.send_keys(Keys.ENTER)


    def _get_page_source(self):
        return self.driver.page_source
    
    
    def _get_text_from_element(self, element:str, find_method:str) -> str:
        element = self._find_element(element, find_method)
        return element.text
    

    def _get_text_from_elements(self, element:str, find_method:str) -> str:
        element = self._find_elements(element, find_method)
        return element.text
    

    def _open_new_tab(self) -> None:
        # Open a new window
        self.driver.execute_script("window.open('');")
        
        # Switch to the new window and open new URL
        self.driver.switch_to.window(self.driver.window_handles[1])


    def _back_to_old_tab(self):
        self.driver.close()
        # Switching to old tab
        self.driver.switch_to.window(self.driver.window_handles[0])


    def _screenshot_element(self, element:str, find_method:str, dest_folder:str, filename:str, format:str='png') -> None:
        element = self._find_element(element, find_method)

        with open(f'{dest_folder}\\{filename}.{format}', 'wb') as file:
            file.write(element.screenshot_as_png)
            