from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "localhost:9222"
available=[]
seedKey="manas"
def generateKeys():
    usernames = []

    usernames.append(seedKey)  
    usernames.append(seedKey.lower())  
    usernames.append(seedKey.upper())  

    for i in range(1, 6):  
        usernames.append(f"{seedKey}{i}") 
        usernames.append(f"{i}{seedKey}")  
    
    suffixes = ['_official', '_123', '_thegreat', '_xyz', '1234', '2024']
    prefixes = ['user_', 'member_', 'cool_', 'the_']
    
    for suffix in suffixes:
        usernames.append(f"{seedKey}{suffix}") 
    
    for prefix in prefixes:
        usernames.append(f"{prefix}{seedKey}") 
    from random import choice
    variations = [f"{seedKey}{choice(['123', 'xyz', 'abc'])}",
                  f"{choice(['super', 'mega'])}_{seedKey}"]
    
    usernames.extend(variations)  
    
    return list(set(usernames))  

    
def clearInput():
    input_field.clear()  
    input_field.send_keys(Keys.CONTROL + "a") 
    input_field.send_keys(Keys.BACKSPACE) 

def sendInput(input):
    input_field.send_keys(input)
    time.sleep(2)
def waitAndCheck(driver,input1):
    try:
        # Wait for up to 5 seconds for the element to be present
        parent_element=WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-component="slug-status"]'))
        )
        print("parent:",parent_element)
        child_div = parent_element.find_element(By.XPATH, './div') 
        print("child:",child_div)
        content = child_div.text
          
        print("Content found:", content)
        if content=='unavailable':
            available.append(input1)
            return available

        return content
    except Exception as e:
        print("Element not found within the given time.")
        print(str(e))
        return None
service = Service("/usr/bin/chromedriver")  

driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the page
driver.get("https://calendly.com/app/personal/link")

wait = WebDriverWait(driver, 20) #wait here max set to 20secs for worst case
input_field = wait.until(EC.presence_of_element_located((By.NAME, "slug")))

wait.until(EC.element_to_be_clickable((By.NAME, "slug")))
#cycle---> clear, send ,(wait 2secs and )check FOR ALL GENERATED KEYSSSS
unames=generateKeys()
for uname in unames:
    clearInput()
    sendInput(uname)
    print(waitAndCheck(driver,uname))
def mapTo(el):
    return "https://calendly.com/"+el
links=list(map(mapTo,available))
print(links)