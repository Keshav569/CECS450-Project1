#!/usr/bin/env python
# coding: utf-8

# In[95]:


import sys
import random
import re
import string
import webbrowser
from collections import Counter
import nltk
from nltk.corpus import stopwords

exclude = set(string.punctuation)

def get_words_count(filename, n_highest=100):
    words = re.findall(r"\w+", open(filename).read().lower())
    total_words = len(words)
    print(total_words)
    nltk.download('stopwords')
    stops = set(stopwords.words("english"))
    filtered_words = [w for w in words if w not in stops]
    if n_highest:
        return total_words, dict(Counter(filtered_words).most_common(n_highest))
        print(total_words)
        print(Counter(words).most_common(n_highest))
    else:
        return total_words, dict(Counter(filtered_words).most_common(total_words))
        print(total_words)
        print(dict(Counter(words).most_common(total_words)))

def create_word_cloud_html(
    count_dict,
    outfile="output.html",
    minfont=1,
    maxfont=6,
    hovercolor="red",
    width="1000px",
    height="1000px",
    fontfamily="calibri",
    colorlist=["#607ec5", "#86a0dc", "#4c6db9","red","orange","cyan","green","yellow","magenta"],
):
    if not outfile.endswith(".html"):
        print("Please Enter Output File with extension .html")
        sys.exit(0)

    #random.shuffle(count_dict)
    frequencies = [count_dict[pair] for pair in count_dict.keys()]
    minFreq = min(frequencies)
    maxFreq = max(frequencies)
    l = list(count_dict.items())
    random.shuffle(l)
    count_dict = dict(l)
   

    span = ""

    css = (
        """#box{font-family:'"""
        + fontfamily
        + """';border:2px solid black;background: black;display: block;width:"""
        + width
        + """;height:"""
        + height
        + """}
        #box a{text-decoration : none}
        a{
        display:inline-block;
      text-decoration:none !important;
    }
    .tooltip {
      position: relative;
      display: inline-block;
    }
  .tooltip .tooltiptext {
    visibility: hidden;
    display: inline-block;
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
color:white
}
.button{
background-color: #FF8C00;
color: white;
}
.button2{
background-color: #000080;
color: white;
}
.button3{
background-color: #f44336;
color: white;
}

"""
    )
    
    script = (
    """function shuffle(e){
 var parent = $("#box");
    var spans = parent.children();
    while (spans.length) {
        parent.append(spans.splice(Math.floor(Math.random() * spans.length), 1)[0]);
    }
}

function col(e){
var colorlist=["#607ec5", "#86a0dc", "#4c6db9","red","orange","cyan","green","yellow","magenta"];
var parent = $("#box");
var spans = parent.children();
i=0;
while (i!=spans.length){
    span=spans[i];
    if (span)
    {
    span=span.firstElementChild
    var colorIndex = Math.floor(Math.random() * colorlist.length);
    span.setAttribute('style','color:'+colorlist[colorIndex]+'!important')
    }
    i++;
}
}

function pop(e){
var elements = document.getElementById('box').children;
  if(elements.length  == 1)
    return;

  elements[getRandom(elements.length-1)].remove();
  if(elements.length > 1){
    elements[getRandom(elements.length-1)].remove();
  }
  
  }
  function getRandom(max){
    return Math.floor(Math.random() * (max - 0 + 1)) + 0;
}
"""
)

    colors = colorlist
    colsize = len(colors)
    index = 0
    k = 0
    for tag, freq in count_dict.items():
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
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <style type="text/css">
        """
            + css
            + """
        </style>
        <button class ="button" onclick = "shuffle()">Shuffle</button>
        <button class ="button2" onclick = "col()">Color</button>
        <button class ="button3" onclick= "pop()">Pop</button>
        <div id='box'>
            """
            + span
            
            + """
            
        </div>
        
        <script>
        """
            +script
            +"""
        </script>
        """
        )
        f.write(message)
    print("Successfully generated word cloud in '" + outfile + "' file.")


if __name__ == "__main__":
    file_name = "beemovie.txt"
    output_file = "result.html"
    total_words, word_co = get_words_count(file_name, n_highest=100)
    print(word_co)
    isinstance(word_co,list)
    #print(sum(word_co.values()))
    print(len(word_co))
    print(total_words)
    create_word_cloud_html(word_co, output_file)
    webbrowser.open(output_file)


# In[ ]:




