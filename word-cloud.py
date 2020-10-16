import re
from collections import Counter
import random
import math

fill = 'white'
stroke = 'white'
stroke_width = 0
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
"""
def get_text_dimensions(text, points):
        return (math.ceil(len(text) * points * 0.6) , points)


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


"""
Using spiral motion (derivative of the equation of a spiral), check every step with all bounding boxes that exist
in the set of SVGs so far. Once there is no collision, return the coordinates.
:param bounds: an array that stores all 4 corners of text boxes
:param x: x coordinate where the text is trying to be placed
:param y: y coordinate where the text is trying to be placed
:param width: width of the rectangle surrounding the text
:param height: height of the rectangle surrounding the text
"""
def nearestNonCollision(bounds, x, y, width, height):
    flag = True
    left, right, top, bottom = x, x + width, y, y + height
    dx, dy = 0, 0
    count = 0
    direction = len(bounds) % 4
    while True:
        if dx != len(bounds) and dy != len(bounds):
            dx, dy = count, count
        for box in bounds:
            # print('and: ' + str(right > box[0] and left < box[1] and top < box[3] and bottom > box[2]))
            if right > box[0] and left < box[1] and top < box[3] and bottom > box[2]:  # If collision
                if count % 4 == 2:
                    dx += 1
                    dx = -dx
                elif count % 4 == 3:
                    dy = -dy
                    dy += 1
                top += int(dy)
                bottom += int(dy)
                left += int(dx)
                right += int(dx)
                print(dx, dy)
                print('count: ' + str(count))
                print('mod: ' + str(count % 2))

                print('collision')
                # if dx < 0:
                #     dx -= width / 2
                # if dy < 0:
                #     dy -= height / 2
                count += 1  # Update the amount of collisions
                print(dx, dy)
                print(left, right)
                flag = True  # Set flag to true, so that all potential collisions are checked again
        if not flag:
            return left, top  # Return the new x/y (left, right)
        flag = False  # Reset the collision flag so that if there are no collisions in next iteration, return x/y

"""
Checks if there
"""
def isCollision():
    pass

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
Pass all relative data to generate SVGs for each word while generating the CSS position for each word
"""
css_pos = '<style> svg { position: absolute; }'
bounds = []
startx, starty = 700, 300
padding = 50
random.shuffle(word_font_size)  # Randomize the word/ font size indices
x = startx
y = starty
for i in range(len(word_font_size)):
    txt_dim = get_text_dimensions(word_font_size[i][0], word_font_size[i][1])
    # if i == 0:
    #     x = startx
    #     y = starty
    # else:
    x, y = nearestNonCollision(bounds, x, y, txt_dim[0], txt_dim[1])
    print('new coords: ' + str(x) + ', ' + str(y))
    svg_array.append(createSVG(word_font_size[i][0], x, y, txt_dim, stroke, stroke_width, fill, word_font_size[i][1]))
    css_pos += '._' + str(x) + '_' + str(y) + ' { left: ' + str(x) + 'px; top: ' + str(y) + 'px; } '
    print(word_font_size[i][0], txt_dim, stroke, stroke_width, fill, point)
    bounds.append((x, x + txt_dim[0], y, y + txt_dim[1]))
    x, y = startx, starty

css_pos += '</style>'
print(bounds)
"""
Input all CSS and SVGs into the HTML string for rendering
"""

html_final = '<!DOCTYPE html><html>' + css_pos + '<body><div>'
for svg in svg_array:
        html_final += svg
html_final += '</div></body></html>'


f = open('test.html', 'w')
f.write(html_final)
f.close()
