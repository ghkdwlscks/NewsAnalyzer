<!-- Writer: Jinchan Hwang <jchwang@yonsei.ac.kr> -->

# NewsAnalyzer - Korean News Article Clustering

![execution_example](images/execution_example.png?raw=true)

**NewsAnalyzer** crawls and clusters NAVER news articles from given keywords.
While data preprocessing is the most essential and important part in natural language processing (NLP), since *news articles are well-structured documents*, NewsAnalyzer uses simple and intuitive preprocessing method, exploiting the characteristics of news articles.
It adopts [FastText](https://fasttext.cc/) model from [Gensim](https://radimrehurek.com/gensim/) in order to obtain word vectors and [HDBSCAN](https://github.com/scikit-learn-contrib/hdbscan) for clustering news articles.

NewsAnalyzer has following features:

* Unsupervised news article clustering
* Keyword-specific word vector model training
* Embedded Chromium web browser which shows selected news article

## Getting Started

### Prerequisites

* Python3 version: Python 3.9.1

### Executing NewsAnalyzer

* Downloading and setup NewsAnalyzer

    ```sh
    git clone https://github.com/ghkdwlscks/NewsAnalyzer.git
    cd NewsAnalyzer/fasttext
    ```

* Installing Python3 libraries

    ```sh
    pip3 install -r requirements.txt
    ```

* Downloading pretrained FastText model

    ```sh
    wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.bin.gz
    ```

* Executing NewsAnalyzer

    ``` sh
    # Execute NewsAnalyzer directly from Python3 interpreter.
    python3 src/main.py

    # Or install NewsAnalyzer executable.
    python3 build.py
    ```

### Configuring NewsAnalyzer

#### Keyword configurations

* Include: Keywords to include split by ","
* Exclude: Keywords to exclude split by ","

#### FastText Configurations

* FastText model path: Path of FastText model path (either Facebook pretrained model or trained model via NewsAnalyzer)
* Enable training: Whether to enable training or not
* Trained model name: Model name to be saved after training

## Author

Jinchan Hwang - jchwang@yonsei.ac.kr
