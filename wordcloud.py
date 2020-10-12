import sys
import random
import re
import string
import webbrowser
from collections import Counter

exclude = set(string.punctuation)

def get_words_count(filename, n_highest=100):
    words = re.findall(r"\w+", open(filename).read().lower())
    total_words = len(words)
    if n_highest:
        return total_words, Counter(words).most_common(n_highest)
    else:
        return total_words, Counter(words).most_common(total_words)

def create_word_cloud_html(
    count_dict,
    outfile="output.html",
    minfont=1,
    maxfont=6,
    hovercolor="red",
    width="1000px",
    height="1000px",
    fontfamily="calibri",
    colorlist=["#607ec5", "#002a8b", "#86a0dc", "#4c6db9"],
):
    if not outfile.endswith(".html"):
        print("Please Enter Output File with extension .html")
        sys.exit(0)

    random.shuffle(count_dict)
    frequencies = [pair[1] for pair in count_dict]
    minFreq = min(frequencies)
    maxFreq = max(frequencies)

    span = ""

    css = (
        """#box{font-family:'"""
        + fontfamily
        + """';border:2px solid black;width:"""
        + width
        + """;height:"""
        + height
        + """}
        #box a{text-decoration : none}
        a{
      text-decoration:none !important;
    }
    .tooltip {
      position: relative;
    }
  .tooltip .tooltiptext {
    visibility: hidden;
    color: blue;
    top:30px;
    left:80px;
    /* Position the tooltip */
    position: absolute;
    z-index: 1;
    border:1px solid #ddd;
    padding:10px;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
color:black
}"""
    )

    colors = colorlist
    colsize = len(colors)
    index = 0
    k = 0
    for tag, freq in count_dict:
        index += 1

        # span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">&nbsp;' + tag + "&nbsp;</span></a>\n"
        span += (
            '<a href=""><span class="word'
            + str(index)
            + ' tooltip", id="tag'
            + str(index)
            + '">'
            + "&nbsp;"
            + tag
            + "&nbsp;"
            + '<span class = "tooltiptext">'
            + str(freq)
            + " times\n"
            + str(round(freq / total_words * 100, 3))
            + "%"
            + "</span></a>\n"
        )

        try:
            fontMax = maxfont
            fontMin = minfont
            K = (freq - minFreq) / (maxFreq - minFreq)
            frange = fontMax - fontMin
            C = 4

            K = float(freq - minFreq) / (maxFreq - minFreq)
            size = fontMin + (C * float(K * frange / C))
        except:
            print("!!! Please input a text with more number of words !!!")
            sys.exit(0)

        css += (
            "#tag"
            + str(index)
            + "{font-size: "
            + str(size)
            + "em;color: "
            + colors[int(k % colsize)]
            + "}\n"
        )
        css += "#tag" + str(index) + ":hover{color:" + hovercolor + "}\n"
        k += 1

    """ Write the HTML and CSS into seperate files """

    with open(outfile, "w") as f:
        message = (
            """
        <style type="text/css">
        """
            + css
            + """
        </style>
        <div id='box'>
            """
            + span
            + """
        </div>
        """
        )
        f.write(message)
    print("Successfully generated word cloud in '" + outfile + "' file.")


if __name__ == "__main__":
    file_name = "alice.txt"
    #file_name = "beemovie.txt"
    output_file = "result.html"
    total_words, word_co = get_words_count(file_name, n_highest=250)
    # print(word_co)
    create_word_cloud_html(word_co, output_file)
    webbrowser.open(output_file)
