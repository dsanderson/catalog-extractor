from flask import Flask, request, redirect
import csv
import pickle
import random
from collections import namedtuple
from PIL import Image

app = Flask(__name__)

def load_data(file="data/boxes.pckl"):
    with open(file, "rb") as data:
        boxes = pickle.load(data)
    return boxes

def add_data(i1, i2, score, file="data/results.csv"):
    line = '{},{},{}\n'.format(i1,i2,score)
    with open(file, "a") as ouput:
        output.write(line)

def render_page(i1, i2, boxes, image="data/misumi-snippet.png"):
    #generate the image to display
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    draw.rectangle(boxes[i1].position, fill=None, outline=(255,0,0,128))
    draw.rectangle(boxes[i2].position, fill=None, outline=(255,0,0,128))
    im.save("data/web.png", "PNG")
    page = """<img src="web.png"></img>"""
    page = page+"""<form action="" method="post">
  <input type="hidden" name="i1" value="{}">
  <input type="hidden" name="i2" value="{}">
  <input type="submit" name="answer" value="No">
  <input type="submit" name="answer" value="Yes">
</form>""".format(i1,i2)
    return page

@app.route("/", methods = ["GET"])
def present():
    i1 = random.randint(0,len(boxes))
    i2 = random.randint(0,len(boxes))
    page = render_page(i1,i2,boxes)
    return page

@app.route("/", methods = ["POST"])
def recieve():
    i1 = int(request.form["i1"])
    i2 = int(request.form["i2"])
    answer = request.form["answer"]
    score = (1 if answer=="Yes" else 0)
    add_data(i1,i2,score)
    return redirect("/")

if __name__ == '__main__':
    Box = namedtuple("Box", ["position","content","norm_position"])
    boxes = load_data()
    print "{} datums, {} possible comparisons".format(len(boxes), len(boxes)**2)
    random.seed(100)
    app.run(host="0.0.0.0",port=int("2234"))
