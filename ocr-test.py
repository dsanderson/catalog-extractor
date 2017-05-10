from PIL import Image
import sys

import pyocr
import pyocr.builders

import copy

from collections import namedtuple
import pickle

Box = namedtuple("Box", ["position","content","norm_position"])

def get_ocr(image):
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
    im = Image.open(image)
    width, height = im.size
    width = float(width)
    height = float(height)
    word_boxes = tool.image_to_string(
        im,
        lang=lang,
        builder=pyocr.builders.WordBoxBuilder()
    )
    # list of box objects. For each box object:
    #   box.content is the word in the box
    #   box.position is its position on the page (in pixels)
    #
    # Beware that some OCR tools (Tesseract for instance)
    # may return empty boxes
    #print(len(word_boxes))
    # Print number of empty word boxes
    wb = [w for w in word_boxes if len(w.content.strip())>0]
    boxes = []
    for b in wb:
        content = b.content.strip()
        position = b.position
        norm_position = [(position[0][0]/width, position[0][1]/height),(position[1][0]/width, position[1][1]/height)]
        boxes.append(Box(content=content, position=position, norm_position=norm_position))

    #print(len(wb))
    #print(word_boxes[0].position)
    return boxes

def token_score(b1,b2):
    for t in b1.content.lower().split():
        if t in b2.content.lower():
            return 1.0
    return 0.0

def horizontal_aignment_score(b1,b2):
    c1 = (b1.norm_position[0][0]+b1.norm_position[1][0])/2.0
    c2 = (b2.norm_position[0][0]+b2.norm_position[1][0])/2.0
    if c1>=b2.norm_position[0][0] and c1<=b2.norm_position[1][0]:
        return 1.0
    elif c2>=b1.norm_position[0][0] and c2<=b1.norm_position[1][0]:
        return 1.0
    else:
        return 0.0

def vertical_aignment_score(b1,b2):
    c1 = (b1.norm_position[0][1]+b1.norm_position[1][1])/2.0
    c2 = (b2.norm_position[0][1]+b2.norm_position[1][1])/2.0
    if c1>=b2.norm_position[0][1] and c1<=b2.norm_position[1][1]:
        return 1.0
    elif c2>=b1.norm_position[0][1] and c2<=b1.norm_position[1][1]:
        return 1.0
    else:
        return 0.0

def score_boxes(boxes):
    scores = []
    for b1 in boxes:
        box_scores = []
        for b2 in boxes:
            score = token_score(b1,b2)+vertical_aignment_score(b1,b2)+horizontal_aignment_score(b1,b2)
            box_scores.append(score)
        scores.append(copy.deepcopy(box_scores))
    return scores

def draw_output(boxes, scores):
    print("Drawing boxes")
    from PIL import Image, ImageDraw
    im = Image.open("data/misumi-snippet.png")

    def center(box):
        return (int((box.position[0][0]+box.position[1][0])/2.0),int((box.position[0][1]+box.position[1][1])/2.0))

    draw = ImageDraw.Draw(im)
    for b in boxes:
        #try:
        #    print(b.content)
        #except:
        #    print("Error printing!")
        draw.rectangle(b.position, fill=None, outline=(255,0,0,128))
    print("Drawing score lines")
    for i,s in enumerate(scores):
        for j,val in enumerate(s):
            if val>0:
                print("Drawing line")
                draw.line([center(boxes[i]),center(boxes[j])], fill=(0,255,0,10), width=int(3*val))
    del draw

    im.save("data/misumi-snippet-markup.png", "PNG")

def write_boxes(boxes, file="data/boxes.pckl"):
    with open(file, "wb") as data:
        pickle.dump(boxes, data)

if __name__ == '__main__':
    boxes = get_ocr('data/misumi-snippet.png')
    print len(boxes)
    write_boxes(boxes)
    #scores = score_boxes(boxes)
    #draw_output(boxes,scores)
