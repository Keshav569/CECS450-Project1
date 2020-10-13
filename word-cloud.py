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

def get_text_dimensions(text, points, font):
        class SIZE(ctypes.Structure):
                _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

        hdc = ctypes.windll.user32.GetDC(0)
        hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
        hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

        size = SIZE(0, 0)
        ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

        ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
        ctypes.windll.gdi32.DeleteObject(hfont)

        return (size.cx, size.cy)

def get_words_count(filename, n_highest=100):
    words = re.findall(r"[a-zA-Z]{4,}", open(filename).read().lower())
    total_words = len(words)
    if n_highest:
        return total_words, Counter(words).most_common(n_highest)
    else:
        return total_words, Counter(words).most_common(total_words)

def createSVG(word, x, y, txt_dim, stroke, stroke_width, fill, point, rotate=0):
    return ('<svg ' 
            'transform="translate(' + str(x) + ',' + str(y) + ') '   # Set translation in x/ y directions
            'rotate(' + str(rotate) +')" ' # Set rotation from the origin (0,0)
            'width="' + str(txt_dim[0]) + 'px" height="' + str(txt_dim[1]) + 'px"><rect width="' + str(txt_dim[0]) + 'px" height="' + str(txt_dim[1]) + 'px" '  # Set width/ height
            'stroke="' + stroke + '" stroke-width="' + str(stroke_width) + 'px" '  # Set stroke/ stroke size (outline)
            'fill="' + fill + '"/>'  # Set the fill of the rectangle
            '<text font-size="' + str(point) + '" x="50%" y="50%" dominant-baseline="middle" '  # Set font size
            'text-anchor="middle">' + word + '</text></svg>')  # Set the text inside the rectangle



total_words, word_freq = get_words_count(filename, 500)


# random.shuffle(word_freq)

# Find the min/ max occurrences of words in the text
frequencies = [pair[1] for pair in word_freq]

# print(int(len(frequencies) / 2))
# print(frequencies[:int(len(frequencies) / 2)])
# print(frequencies[int(len(frequencies) / 2)])
# print(numpy.std(frequencies))
mean = 0
for i in frequencies:
        mean += i
mean = mean / len(frequencies)
print(mean)
minFreq = min(frequencies)
maxFreq = max(frequencies)

# Convert occurrences to a ratio where the highest occurrence has font size 100 and the lowest has font size 1
word_font_size = []
for word in word_freq:
        font_size = int((float(word[1]) / maxFreq) * max_font)
        if font_size < min_font:
                font_size = min_font
        if word[1] > mean:
            font_size += mean_font_padding
        word_font_size.append((word[0], font_size))  # Change the number of occurrences to the relative font size to be displayed
        # print(word_font_size, font_size)

print(word_font_size)
# print(minFreq, maxFreq)
# print(total_words, word_freq)


# txt_dim = get_text_dimensions('word', point, font)
# print(txt_dim)

for word in word_font_size:
    txt_dim = get_text_dimensions(word[0], word[1], font)
    svg_array.append(createSVG(word[0], 300, 300, txt_dim, stroke, stroke_width, fill, word[1]))
    print(word[0], txt_dim, stroke, stroke_width, fill, point)
# txt_dim = get_text_dimensions()

"""
Input all svgs into the html for rendering
"""
html_final = '<!DOCTYPE html><html><body>'
for svg in svg_array:
        html_final += svg
html_final += '</body></html>'


f = open('test.html', 'w')
# f.write('<!DOCTYPE html><html><body>' + svg_array[0] + '</body></html>')
f.write(html_final)
f.close()

# f.write('<?xml version="1.0" encoding="utf-8" ?><svg height="100%" version="1.2" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />'
#         '<text transform="rotate(' + str(rotate) + ')" font-size="' + str(size) + '" fill="' + fill + '" x="' + str(x) + '" y="' + str(y) + '">' + word + '</text></svg>')
# svg_array.append('<svg width="' + str(w) + '" height="' + str(h) + '">'
#         '<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(w) + '" height="' + str(h) + '" stroke="' + stroke + '" stroke-width="3px" fill="' + fill + '"/>'
#         '</svg>')
# svg_array.append('<svg transform="translate(' + str(x2) + ',' + str(y2) + ') rotate(' + str(rotate2) +')" width="' + str(w) + 'px" height="' + str(h) + 'px"><rect width="' + str(w) + 'px" height="' + str(h) + 'px" stroke="red" stroke-width="3px" fill="white"/> <text font-size="' + str(getOptimalFontSize(word)) + '" x="' + str(50) + '%" y="50%" dominant-baseline="middle" text-anchor="middle">Text</text> </svg>')


# x = 333
# y = 333
# word = 'testing2'
# fill = 'red'
# size = 90
# rotate = 11
#
# f = open('test2.svg', 'w')
# f.write('<?xml version="1.0" encoding="utf-8" ?><svg height="100%" version="1.2" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />'
#         '<text transform="rotate(' + str(rotate) + ')" font-size="' + str(size) + '" fill="' + fill + '" x="' + str(x) + '" y="' + str(y) + '">' + word + '</text></svg>')
# f.close()
