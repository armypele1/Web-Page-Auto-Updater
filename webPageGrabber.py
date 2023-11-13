from selenium import webdriver
from PIL import Image, ImageTk
import time
import tkinter as tk
import argparse
import sys
from io import BytesIO

root = tk.Tk()
driver = webdriver.Chrome("C:/WebDrivers/chromedriver-win64/chromedriver.exe")

# Grab a screenshot of some url and return as PIL image
def takeScreenshot(url):
    browser = driver
    browser.get(url)

    # Take screenshot and convert to PIL image
    screenshot = browser.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))
    browser.quit()

    return image


def updateImage(label, url, interval):
    image = takeScreenshot(url)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo # ref to prevent GC

    # Keep running this function every n seconds
    label.after(interval * 1000, updateImage, label, url)

def closeWindow(event):  
    root.destroy() 

def main():
    # Get the command-line arguments
    parser = argparse.ArgumentParser(description="Take screenshots of a webpage.")
    parser.add_argument('url', type=str, help="the URL of the webpage to screenshot") 
    parser.add_argument('interval', type=int, help="the amount of time between screenshots (seconds)") 
    args = parser.parse_args()

    
    root.attributes('-fullscreen', True) # Make the window fullscreen

    # Create the label that will display the screenshot
    label = tk.Label(root) # For testing
    label.pack(expand=True, fill="both") # Make the label fill the window
    updateImage(label, args.url, args.interval)

    root.bind('<Escape>', closeWindow)  # Allow application to be closed via escape key
    root.mainloop()

if __name__ == "__main__":
    main();    
