# --- LICENSE ---
# Copyright 2023 Slour
# author : Ali Crafty
# publish date : 20/11/2023
# YouTube Channel: https://www.youtube.com/@ali_crafty
# TikTok Account: https://www.tiktok.com/@tr6s_
# Instagarm Account: https://www.instagram.com/tr6s_i/

import json, sys
def color(style="no effect",textcolor="white",background="black"):
    data = json.loads(open("color/color.json",'r').read()) # get Data From 'color.json'
    args = {"style":str(style).lower(),"textcolor":str(textcolor).lower(),"background":str(background).lower()} # args To Json
    try:
        args["style"] = data["style"][args["style"]] # Search Color in Data
    except KeyError:
        args["style"] = data["style"]["no effect"] # If no Result in Data Set Defult Color
    try:
        args["textcolor"] = data["textcolor"][args["textcolor"]] # Search Color in Data
    except KeyError:
        args["textcolor"] = data["textcolor"]["white"] # If no Result in Data Set Defult Color
    try:
        args["background"] = data["background"][args["background"]] # Search Color in Data
    except KeyError:
        args["background"] = data["background"]["black"] # If no Result in Data Set Defult Color
    style = args["style"] # Set Values of Varible
    tc = args["textcolor"] # Set Values of Varible
    bg = args["background"] # Set Values of Varible
    return f"\033[{style};{tc};{bg}m" # Return Result
class ColorCustom:
    def __init__():
        pass
    def textcolor(color_code):
        data = json.loads(open("color/color.json",'r').read()) # get Data From 'color.json'
        try:
            color_code = "tc" + str(color_code)
            return data["tc"][color_code]
        except KeyError:
            return u"\u001b[0m"
    def background(color_code):
        data = json.loads(open("color/color.json",'r').read()) # get Data From 'color.json'
        try:
            color_code = "bg" + str(color_code)
            return data["bg"][color_code]
        except KeyError:
            return u"\u001b[0m"
    def help():
        for i in range(0, 16):
            for j in range(0, 16):
                code = str(i * 16 + j)
                sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")
        print("\n\n")
        for i in range(0, 16):
            for j in range(0, 16):
                code = str(i * 16 + j)
                sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")
brightgreen = color(textcolor="green",style="bold")
brightblack = color(textcolor="black",style="bold")
brightred = color(textcolor="red",style="bold")
brightyellow = color(textcolor="yellow",style="bold")
brightblue = color(textcolor="blue",style="bold")
brightpurple = color(textcolor="purple",style="bold")
brightcyan = color(textcolor="cyan",style="bold")
brightwhite = color(textcolor="white",style="bold")
brightreset = u'\u001b[0;1m'
grenn = color(textcolor="green")
black = color(textcolor="black")
red = color(textcolor="red")
yellow = color(textcolor="yellow")
blue = color(textcolor="blue")
purple = color(textcolor="purple")
cyan = color(textcolor="cyan")
white = color(textcolor="white")
reset = u'\u001b[0m'