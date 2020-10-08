import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

ditLength = 0.5  # Length of a dot in seconds

# Characters-Morse euivalent pairs
morse = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "&": ".-...",
        "'": ".----.",
        "@": ".--.-.",
        ")": "-.--.-",
        "(": "-.--.",
        ":": "---...",
        ",": "--..--",
        "=": "-...-",
        "!": "-.-.--",
        ".": ".-.-.-",
        "-": "-....-",
        "+": ".-.-.",
        '"': ".-..-.",
        "?": "..--..",
        "/": "-..-.",
    }

# Checks if all the characters in a text
# can be converted to Morse code
def validate(text):
    for char in text:
        if char == " ":
            continue
        if char.lower() not in morse:
            return False
    return True


# This function translates a string to a morse form using dots, dashes, spaces and slashes.
def translateToMorse(text):
    
    translation = ""

    words = text.split(" ")
    wordsLength = len(words)

    for i in range(wordsLength):
        for char in words[i]:
            translation += morse[char.lower()]

            translation += " "
            
        # '/' is added after every word appropriately
        if wordsLength > 1 and i < wordsLength - 1:
            translation += "/ "

    return translation.strip()

def keepPlayingPrompt():
    question = "Would you like to play again? y/n  "
    choice = input(question)
    while True:
        if choice.lower() == "y":
            return True
        elif choice.lower() == "n":
            return False
        else:
            print()
            choice = input("Invalid input! " + question)
            print()    


def playLed(morse):
    for char in morse:
        if char == ".":
            GPIO.output(18, True)
            time.sleep(ditLength)
            GPIO.output(18, False)
            time.sleep(ditLength)
        elif char == "-":
            GPIO.output(18, True)
            time.sleep(3 * ditLength)
            GPIO.output(18, False)
            time.sleep(ditLength)
        elif char == " ":
            GPIO.output(18, False)
            time.sleep(3 * ditLength)
        elif char == "/":
            GPIO.output(18, False)
            time.sleep(7 * ditLength)
        else:
            pass


keepPlaying = True

while keepPlaying:
    textInput = input("Enter the text to be played as Morse code >>> ")
    
    if textInput == "":
        print("Empty input!")
        keepPlaying = keepPlayingPrompt()
        continue
    
    if not validate(textInput):
        print("Input cannot be converted to Morse code!")
        keepPlaying = keepPlayingPrompt()
        continue
    else:
        morseEquivalent = translateToMorse(textInput)
        
        print(f"Playing {textInput} in 6..", end = "")
        for i in range(5, 0, -1):
            time.sleep(1)
            print(f"{i}..")
            
        playLed(morseEquivalent)
        keepPlaying = keepPlayingPrompt()
        continue

GPIO.cleanup()
