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

* Installing Python3 libraries

  ```sh
  pip install -r requirements.txt
  ```

* Downloading pretrained [FastText](https://fasttext.cc/) model
  1. Download word vector binary file from <https://fasttext.cc/docs/en/crawl-vectors.html>.
  2. Move the downloaded binary (e.g., cc.ko.300.bin.gz) under NewsAnalyzer/fasttext/.

## Running NewsAnalyzer

## Author

Jinchan Hwang - jchwang@yonsei.ac.kr
