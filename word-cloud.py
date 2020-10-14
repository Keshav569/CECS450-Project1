import ctypes
import re
from collections import Counter
import random
import numpy

# x = 200
# y = 200
# w = 300
# h = 50
# word = 'testing'
fill = 'white'
stroke = 'red'
stroke_width = 3
# size = 50
# rotate = 0
font = 'Times New Roman'
point = 50
svg_array = []
filename = 'alice.txt'
max_font = 50  # The max font will actually be this number added to mean_font_padding
mean_font_padding = 3
min_font = 10


"""
Returns the approximate pixel dimensions of a string of text while taking into account its font and font size

:param text: an english word as a string
:param points: the font size
:param font: the font family/ style
"""
def get_text_dimensions(text, points, font):

        class SIZE(ctypes.Structure):
                _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

        hdc = ctypes.windll.user32.GetDC(None)
        hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
        hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

        size = SIZE(0, 0)
        ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

        ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
        ctypes.windll.gdi32.DeleteObject(hfont)

        return (len(text) * points * 0.6 , size.cy)


"""
Returns a specified amount of the most common words from a specified file.

:param filename: the directory and location of the .txt file to be parsed 
:param n_highest: the amount of words to be returned, taking from the top n most common words
"""
def get_words_count(filename, n_highest=100):
    words = re.findall(r"[a-zA-Z]{4,}", open(filename).read().lower())
    total_words = len(words)
    if n_highest:
        return total_words, Counter(words).most_common(n_highest)
    else:
        return total_words, Counter(words).most_common(total_words)


"""
Creates an SVG element that inserts text of a specified font/ size into a rectangle of a specified
width/ height at a specified x/ y location. These SVG elements can then be inserted into HTML for viewing.

:param word: the English word that is being used
:param x: the absolute x positioning of the SVG element
:param y: the absolute y positioning of the SVG element
:param txt_dim: the pixel dimensions of the word, taking into account the font family/ font size
:param stroke: the color of the bounding box around the rectangle
:param stroke_width: the pixel size of the line ("stroke") that surrounds the rectangle
:param point: the font size of the text
:param rotate: the degree of rotation around the origin of the rectangle (0, 0)
"""
def createSVG(word, x, y, txt_dim, stroke, stroke_width, fill, point, rotate=0):
    return ('<svg class="_' + str(x) + '_' + str(y) + '"' 
            # 'transform="translate(' + str(x) + ',' + str(y) + ') '   # Set translation in x/ y directions
            # 'rotate(' + str(rotate) +')" ' # Set rotation from the origin (0,0)
            'width="' + str(int(txt_dim[0])) + 'px" height="' + str(int(txt_dim[1])) + 'px"><rect width="' + str(int(txt_dim[0])) + 'px" height="' + str(int(txt_dim[1])) + 'px" '  # Set width/ height
            'stroke="' + stroke + '" stroke-width="' + str(stroke_width) + 'px" '  # Set stroke/ stroke size (outline)
            'fill="' + fill + '"/>'  # Set the fill of the rectangle
            '<text font-size="' + str(point) + 'px" x="50%" y="50%" dominant-baseline="middle" '  # Set font size
            'text-anchor="middle">' + word + '</text></svg>')  # Set the text inside the rectangle


total_words, word_freq = get_words_count(filename, 500)

"""
Find the occurrences of words in the data set, find the mean amount of occurrences of words in the data set, and 
the max amount of times a word appears along with the minimum
"""
occurrences = [pair[1] for pair in word_freq]
mean = 0
for i in occurrences:
        mean += i
mean = mean / len(occurrences)
minOccurrence = min(occurrences)
maxOccurrence = max(occurrences)

"""
Convert occurrences to a ratio where the highest occurrence has font size of 'max_font' and the lowest has font size 
of 'min_font'. There is also a 'mean_padding_font' which adds a fixed font size increase to any word that appears
more than the mean amount of appearances for all words in the data set.
"""
word_font_size = []
for word in word_freq:
        font_size = int((float(word[1]) / maxOccurrence) * max_font)
        if font_size < min_font:
                font_size = min_font
        if word[1] > mean:
            font_size += mean_font_padding
        word_font_size.append((word[0], font_size))  # Change the number of occurrences to the relative font size to be displayed

"""
Pass all relative data to generate SVGs for each word along with their respective CSS attributes for positioning
"""
css_pos = '<style> svg { position: absolute; }'
random.shuffle(word_font_size)
dx = 0
dy = 0
for word in word_font_size:
    txt_dim = get_text_dimensions(word[0], word[1], font)
    svg_array.append(createSVG(word[0], dx, dy, txt_dim, stroke, stroke_width, fill, word[1]))
    css_pos += '._' + str(dx) + '_' + str(dy) + ' { left: ' + str(dx) + 'px; top: ' + str(dy) + 'px; } '
    print(word[0], txt_dim, stroke, stroke_width, fill, point)
    dx += 50
    if dx % 500 == 0:
        dy += 100
        dx -= 500
css_pos += '</style>'

"""
Input all CSS and SVGs into the HTML string for rendering
"""

html_final = '<!DOCTYPE html><html>' + css_pos + '<body><div>'
# Randomize the index of SVGs
for svg in svg_array:
        html_final += svg
html_final += '</div></body></html>'


f = open('test.html', 'w')
f.write(html_final)
f.close()
