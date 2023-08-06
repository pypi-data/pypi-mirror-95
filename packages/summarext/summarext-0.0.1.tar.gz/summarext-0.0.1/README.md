# Keyword-Extractor-for-Websites-with-NLP-application

A tool for Extracting keywords and finding the relevant words with cosine similarity, Textrank Algorithm and KeyBERT tranformer model.

# Keyword Extractor: A Smart, Automatic, Fast and Lightweight Keyword Extractor with Deep Learning Application with Python

![img](https://github.com/elvinaqa/Keyword-Extractor-for-Websites/blob/main/images/1_nHfayfdmxAApbg84iMrJqQ.gif)

This project is made for keyword extraction of the semantically similar words from websites and their meta data. Can be used in SEO, marketing and few other related applications. 
It gets a url or the html content of a web page and a list of sample data which we want to scrape from that page. **This data can be text, url or any html tag value of that page.**

## Installation

It's compatible with python 3.

- Install latest version from git repository using pip:
```bash
$ pip install git+https://github.com/elvinaqa/Keyword-Extractor-for-Websites.git

```
Also 
```
$ pip install -r requirements.txt 
```

## How to use

## How it seems?
![img](https://github.com/elvinaqa/Keyword-Extractor-for-Websites/blob/main/images/text.PNG)
![img](https://github.com/elvinaqa/Keyword-Extractor-for-Websites/blob/main/images/col.PNG)
### Results
![img](https://github.com/elvinaqa/Keyword-Extractor-for-Websites/blob/main/images/2nd%20oage.PNG)


## Example code from the project
```python
from gensim.summarization import keywords
from gensim.summarization.keywords import get_graph
import networkx as nx
import matplotlib.pyplot as plt
#
# if __name__ == "__main__":
#     text = "Keywords extraction is a subtask of the Information Extraction field which is responsible for extracting keywords from a given text or from a collection of texts to help us summarize the content. This is useful in the context of the huge amount of information we deal with every day. We need to index this information, to organise it and retrieve it later. Keywords extraction becomes more and more important these days and keywords extraction algorithms are researched and improved continuously."
#
#     print(keywords(text).split('\n'))

def displayGraph(textGraph):

    graph = nx.Graph()
    for edge in textGraph.edges():
        graph.add_node(edge[0])
        graph.add_node(edge[1])
        graph.add_weighted_edges_from([(edge[0], edge[1], textGraph.edge_weight(edge))])

        textGraph.edge_weight(edge)
    pos = nx.spring_layout(graph)
    plt.figure()
    nx.draw(graph, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in graph.nodes()})
    plt.axis('off')
    plt.show()

if __name__=="__main__":

    text = "Keywords extraction is a subtask of the Information Extraction field which is responsible for extracting keywords from a given text or from a collection of texts to help us summarize the content. This is useful in the context of the huge amount of information we deal with every day. We need to index this information, to organise it and retrieve it later. Keywords extraction becomes more and more important these days and keywords extraction algorithms are researched and improved continuously."
    displayGraph(get_graph(text))
```

The output is the summarizing version of the text while selecting the most important words from the list
```python
[
   
]
```


## Issues
Feel free to open an issue if you have any problem using the module.


## Support the project

<a href="https://ko-fi.com/eapresents" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-black.png" alt="Buy Me A Coffee" height="45" width="163" ></a>


#### Happy Coding  ♥️
