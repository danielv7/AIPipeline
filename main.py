from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import os 
import time
import playsound
import speech_recognition as sr
from gtts import gTTS


def main():
    activeUser = True
    openingWebPage()

    while activeUser:
        googleSpeak("say command")

        voiceInput = listeningForInput()
        #voiceInput = "go back"
        parsedInput = parseVoiceInput(voiceInput)
        if "search" in parsedInput:
            listWithOutSearch = removeSearchWord(parsedInput)
            searchingForProduct(listWithOutSearch) 

        elif "basket" in parsedInput:
            googleSpeak("adding current item to basket")
            addToBasket()

        elif "press" in parsedInput:
            pressButton = removePressAndSelect(parsedInput)
            selectingElementByName(pressButton)

        elif "back" in parsedInput:
            goBack()

        elif "forward" in parsedInput:
            goForward()

        elif "click" in voiceInput:
            try:
                pressButton = removeClick(voiceInput)
                pressButton = '-'.join(pressButton)
                pressButton = str(pressButton)
                clickOptions = extractingAllUserInput()

                for i in clickOptions:
                    if i.__contains__(pressButton):
                        #print(i)
                        clickingElementByName(i)
                        break
                #googleSpeak("Could not find item")
            except:
                googleSpeak("Could not find item")

        else:
            googleSpeak("Unable to make out command please say again")

        #getCurrentURL()



def openingWebPage():
    global PATH
    global driver

    PATH = '/Users/danielvaughan/Desktop/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.sephora.com")

def getCurrentURL():
    currentURL = driver.current_url
    driver.get(currentURL)

def extractingAllUserInput():
    listOfActions = []
    try:
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                #print(href)
                listOfActions.append(href)       
        return listOfActions
    except:
        googleSpeak("Did not get list of all user actions")
        
def selectingElementByName(linkName):
    try:
        linkName = [x.capitalize()  for x in linkName] 
        linkName = ' & '.join(linkName)
        link = driver.find_element_by_link_text(linkName)
        linkName = str(linkName)
        command = "pressing" + linkName + "button"
        googleSpeak(command)
        link.click()
        link.click()
  
    except:
        googleSpeak("Button not found")
   
def clickingElementByName(linkName):
    try:
        googleSpeak("Clicking item")
        driver.get(linkName)
        #command = "clicking" + linkName 
        #googleSpeak(command)
        #googleSpeak("Clicking item")

    except:
        googleSpeak("could not click item")

def listeningForInput():
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        listening = True

        while listening:
            #r.adjust_for_ambient_noise(source)
            #print("Please Say Somthing...")
            #audio = r.listen(source)
            audio = r.listen(source, timeout=None, phrase_time_limit=10)
            # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
                # using google speech recognition
                userInput = r.recognize_google(audio)
                #print("Text: "+ userInput)
                #listening = False
                return userInput

            except:
                #googleSpeak("I did not understand. Please say that again.")
                listening = True

def parseVoiceInput(voiceInput):
    #st = LancasterStemmer()
    #voiceInput = "search for red lipstick"
  
    stop_words = set(stopwords.words('english')) 
  
    word_tokens = word_tokenize(voiceInput) 
  
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 

    return filtered_sentence
  
def searchingForProduct(searchInput):
    searchValue = ' '.join(searchInput)

    searchGiven = "searching for "
    searchText = str(searchValue)
    searchCombineText = searchGiven + searchText
    googleSpeak(searchCombineText)


    search = driver.find_element_by_id("site_search_input") #search is input field
    search.send_keys(searchValue)  #enter in test to search
    search.send_keys(Keys.RETURN) #Press the enter key to search value

    #print(driver.page_source) #extracting all page source code.

def goForward():
    try:
        driver.forward()
        googleSpeak("going forward")
        return

    except:
        googleSpeak("Could not go forward")
  
def goBack():
    try:
        driver.back()
        googleSpeak("going back")
        return 

    except:
        googleSpeak("Could not go back")

def removeSearchWord(parsedInput):
    #parsedInput = parsedInput.split(' ')
    stopwords = ['search','searching', 'for']
    for word in list(parsedInput):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            parsedInput.remove(word)
        return parsedInput

def removePressAndSelect(parsedInput):
    #parsedInput = parsedInput.split(' ')  
    stopwords = ['press', 'select','button','click']
    for word in list(parsedInput):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            parsedInput.remove(word)
    return parsedInput

def removeClick(voiceInput):
    voiceInput = voiceInput.split(' ')  
    stopwords = ['click']
    for word in list(voiceInput):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            voiceInput.remove(word)
    return voiceInput

def addToBasket():
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-x04nfy"))
        )
        element.click()

    except:
        googleSpeak("Item not added to basket")

def googleSpeak(vocieText):
    tts = gTTS(text=vocieText,lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    

if __name__ == "__main__": 
    main()
