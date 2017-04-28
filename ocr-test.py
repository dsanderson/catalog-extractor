from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
print("Available tools: %s" % ", ".join([t.get_name() for t in tools]))
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
#lang = langs[0]
lang = 'eng'
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.

word_boxes = tool.image_to_string(
    Image.open('data/misumi-snippet.png'),
    lang=lang,
    builder=pyocr.builders.WordBoxBuilder()
)
# list of box objects. For each box object:
#   box.content is the word in the box
#   box.position is its position on the page (in pixels)
#
# Beware that some OCR tools (Tesseract for instance)
# may return empty boxes
print(len(word_boxes))
# Print number of empty word boxes
wb = [w for w in word_boxes if len(w.content.strip())>0]
print(len(wb))
print(word_boxes[0].position)

print("Drawing boxes")

from PIL import Image, ImageDraw

im = Image.open("data/misumi-snippet.png")

draw = ImageDraw.Draw(im)
for b in wb:
    try:
        print(b.content)
    except:
        print("Error printing!")
    draw.rectangle(b.position, fill=None, outline=(255,0,0,128))
del draw

im.save("data/misumi-snippet-markup.png", "PNG")
