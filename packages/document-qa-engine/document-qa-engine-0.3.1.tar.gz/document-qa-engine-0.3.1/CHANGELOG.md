# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [0.2.0] – 2023-10-31

### Added
+ Selection of chunk size on which embeddings are created upon
+ Mistral model to be used freely via the Huggingface free API 

### Changed
+ Improved documentation, adding privacy statement 
+ Moved settings on the sidebar
+ Disable NER extraction by default, and allow user to activate it
+ Read API KEY from the environment variables and if present, avoid asking the user
+ Avoid changing model after update



## [0.1.3] – 2023-10-30

### Fixed

+ ChromaDb accumulating information even when new papers were uploaded 

## [0.1.2] – 2023-10-26

### Fixed

+ docker build

## [0.1.1] – 2023-10-26

### Fixed

+ Github action build 
+ dependencies of langchain and chromadb 


## [0.1.0] – 2023-10-26

### Added

+ pypi package
+ docker package release

## [0.0.1] – 2023-10-26

### Added

+ Kick off application
+ Support for GPT-3.5
+ Support for Mistral + SentenceTransformer
+ Streamlit application 
+ Docker image 
+ pypi package

<!-- markdownlint-disable-file MD024 MD033 -->
