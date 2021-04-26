import random
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_pie(x, labels):
    # colors = random.choices(list(mcolors.CSS4_COLORS.values()),k = len(labels))
    # explode = [0, 0, 0, 0, 0, 0]
    # # plt.title('category-wise orders selling')
    # plt.figure(figsize=(3, 4))
    # plt.pie(x, labels=labels, autopct='%.2f%%')
    # plt.tight_layout()
    # graph = get_graph()

    colors = ['#ff9999','#66b3ff','#4b977b','#c61857','#03989E']
    explode = (0.05,0.05,0.05,0.05,0.05)
    plt.figure(figsize=(3,4))
    plt.pie(x, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explode)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)  
    plt.tight_layout()
    # plt.title("Top 5 Countries with Confirmed Cases")
    graph = get_graph()
    return graph

def get_pieI(x, labels):
    # colors = random.choices(list(mcolors.CSS4_COLORS.values()),k = len(labels))
    # explode = [0, 0, 0, 0, 0, 0]
    # # plt.title('category-wise orders selling')
    # plt.figure(figsize=(3, 4))
    # plt.pie(x, labels=labels, autopct='%.2f%%')
    # plt.tight_layout()
    # graph = get_graph()

    colors = ['#ff9999','#66b3ff','#4b977b','#c61857','#03989E']
    explode = (0.05,0.05,0.05,0.05,0.05)
    plt.figure(figsize=(3.5,3))
    plt.pie(x, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explode)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)  
    plt.tight_layout()
    # plt.title("Top 5 Countries with Confirmed Cases")
    graph = get_graph()
    return graph

    