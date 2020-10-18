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
filename = 'text.txt'
max_font = 50  # The max font will actually be this number added to mean_font_padding
mean_font_padding = 3
min_font = 10
startx, starty = 0, 0
cloud_bounds = (0, 600, 0, 250)
top_words = 200

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
def createSVG(word, x, y, txt_dim, stroke, stroke_width, fill, point, percent_occurrence,
              colors=["#607ec5", "#002a8b", "#86a0dc", "#4c6db9"], rotate=0):
    return ('<svg class="_' + str(x) + '_' + str(y) + '"' 
            # 'transform="translate(' + str(x) + ',' + str(y) + ') '   # Set translation in x/ y directions
            # 'rotate(' + str(rotate) +')" ' # Set rotation from the origin (0,0)
            'width="' + str(int(txt_dim[0])) + 'px" height="' + str(int(txt_dim[1])) + 'px"><rect width="' + str(int(txt_dim[0])) + 'px" height="' + str(int(txt_dim[1])) + 'px" '  # Set width/ height
            'stroke="' + stroke + '" stroke-width="' + str(stroke_width) + 'px" '  # Set stroke/ stroke size (outline)
            'fill="' + fill + '"/>'  # Set the fill of the rectangle
            '<text fill=' + colors[random.randint(0, len(colors) - 1)] + ' font-size="' + str(point) + 'px" x="50%" y="50%" dominant-baseline="middle" '  # Set font size
            'text-anchor="middle">' + word + '</text><title>The word, ' + word + ', makes up ' + percent_occurrence + '% of the document</title></svg>')  # Set the text inside the rectangle


"""
Using random placement within the given range 'cloud-bounds', check every step with all bounding boxes that exist
in the set of SVGs so far. Once there is no collision, return the coordinates.
:param bounds: an array that stores all 4 corners of text boxes
:param x: x coordinate where the text is trying to be placed
:param y: y coordinate where the text is trying to be placed
:param width: width of the rectangle surrounding the text
:param height: height of the rectangle surrounding the text
"""
def nearestNonCollision(bounds, x, y, width, height, cloud_bounds):
    flag = True
    count = 0
    while True:
        count += 1
        if count > 25000:
            return -1, -1
        placement_attempt = (random.randint(cloud_bounds[0], cloud_bounds[1]), random.randint(cloud_bounds[2], cloud_bounds[3]))
        left, right, top, bottom = placement_attempt[0], placement_attempt[0] + width, placement_attempt[1], placement_attempt[1] + height
        for box in bounds:
            if right > box[0] and left < box[1] and top < box[3] and bottom > box[2]:  # If collision
                print('collision', str(len(bounds)))
                flag = True  # Set flag to true, so that all potential collisions are checked again
        if not flag:
            print(right, left, top, bottom)
            print(cloud_bounds)
            if not (right > cloud_bounds[0] and left < cloud_bounds[1] and top < cloud_bounds[3] and bottom > cloud_bounds[2]):
                print(str(right) + ',' + str(top) + ' not in bounds')
                # continue
            return left, top  # Return the new x/y (left, top)
        flag = False  # Reset the collision flag so that if there are no collisions in next iteration, return x/y

        # if count % 4 == 2:
        #     left += count
        #     right += count
        # elif count % 4 == 3:
        #     top += count
        #     bottom += count


total_words, word_freq = get_words_count(filename, top_words)

"""
Find the occurrences of words in the data set, find the mean amount of occurrences of words in the data set, and 
the max amount of times a word appears along with the minimum
"""
occurrences = [pair[1] for pair in word_freq]
n_total_words = 0
for i in occurrences:
        n_total_words += i
mean = n_total_words / len(occurrences)
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
        print(str(float(word[1] / n_total_words)))
        word_font_size.append((word[0], font_size, "{:.4f}".format(float(word[1] / n_total_words)))) # Change the number of occurrences to the relative font size to be displayed

"""
Pass all relative data to generate SVGs for each word while generating the CSS position for each word
"""
css_pos = '<style> svg { position: absolute; }'
bounds = []
top_3_words = [word_font_size[0], word_font_size[1], word_font_size[2]]
random.shuffle(word_font_size)  # Randomize the word/ font size indices

# Make the top 3 words to be placed first so that they are less likely to appear disproportionately on the right edge
# of the visualization
flags = [True, True, True]
for i in range(len(word_font_size)):
    if word_font_size[i] == top_3_words[0] and flags[0]:
        flags[0] = False
        word_font_size[i] = word_font_size[0]
        word_font_size[0] = top_3_words[0]
        print(word_font_size[i], word_font_size[0])
    if word_font_size[i] == top_3_words[1] and flags[1]:
        flags[0] = False
        word_font_size[i] = word_font_size[1]
        word_font_size[1] = top_3_words[1]
        print(word_font_size[i])
    if word_font_size[i] == top_3_words[2] and flags[2]:
        flags[0] = False
        word_font_size[i] = word_font_size[2]
        word_font_size[2] = top_3_words[2]
        print(word_font_size[i])

"""
Populate the word cloud
"""
while True:
    x = startx
    y = starty
    for i in range(len(word_font_size)):
        txt_dim = get_text_dimensions(word_font_size[i][0], word_font_size[i][1])
        x, y = nearestNonCollision(bounds, x, y, txt_dim[0], txt_dim[1], cloud_bounds)
        if x == -1 and y == -1:
            break
        print('new coords: ' + str(x) + ', ' + str(y))
        svg_array.append(createSVG(word_font_size[i][0], x, y, txt_dim, stroke, stroke_width, fill, word_font_size[i][1], word_font_size[i][2]))
        css_pos += '._' + str(x) + '_' + str(y) + ' { left: ' + str(x) + 'px; top: ' + str(y) + 'px; } '
        print(word_font_size[i][0], txt_dim, stroke, stroke_width, fill, point)
        bounds.append((x, x + txt_dim[0], y, y + txt_dim[1]))
        x, y = startx, starty
    if len(svg_array) == top_words:
        break
    else:
        svg_array = []
        bounds = []

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
