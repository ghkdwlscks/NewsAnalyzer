<!-- Writer: Jinchan Hwang <jchwang@yonsei.ac.kr> -->

# NewsAnalyzer

**NewsAnalyzer** crawls and clusters NAVER news articles from given keywords.
Data preprocessing is the most essential and important part in natural language processing (NLP); however, since *news articles are well-structured documents*, NewsAnalyzer uses simple and intuitive preprocessing method, exploiting the characteristics of news articles.

NewsAnalyzer has following features:

* Clustering news articles
* Training word vector model while clustering (TBU)

## Getting Started

### Prerequisites

* Python3 version: Python 3.9.1

### Executing NewsAnalyzer

* Downloading and setup NewsAnalyzer

    ```sh
    git clone https://github.com/ghkdwlscks/NewsAnalyzer.git
    cd NewsAnalyzer
    mkdir fasttext
    ```

* Installing Python3 libraries

    ```sh
    pip install -r requirements.txt
    ```

* Downloading pretrained [FastText](https://fasttext.cc/) model

    ```sh
    wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.bin.gz
    ```

* Executing NewsAnalyzer

    ``` sh
    python3 src/news_analyzer.py
    ```

## Author

Jinchan Hwang - jchwang@yonsei.ac.kr
