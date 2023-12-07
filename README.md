# Task 1 : Text - Classifier

This repository contains the notebooks and auxiliar functions to  build a document classifier.

- Data exploration notebook contains data exploration and dataset splitting
- Training read the splitted data and build a classifier using a simple LinearSVC classifier using TfidfVectorizer features


# Task 2: Identify conflicting text

1. While finding contradictions, we may not know what to compare with what. How
can we use topic modeling to identify pairs of conflicting text in Consigli
documents?

Topic modelling techniches (Latent Dirichlet Allocation, Non-Negative Matrix Factorization, Latent Semantic Analysis) will be used to identify the topics below a certain paragraph most probably is situated. Identified the paragraph topic, the paragraph will be compared with the other paragraphs of the document which threat the same topic using text similarity tecniches.


2. What kinds of NLP techniques can be used for recognizing pairs of conflicting text
and the measure their inconsistencies?

For topics identification will be used Latent Dirichlet Allocation, Non-Negative Matrix Factorization, Latent Semantic Analysis and for text embedding and posterior text similarity comparison will be used Word2vec, Glove, BERT embeddings, Universal Google Sentence Encoder.


3. Please suggest an outline of ML process where input is raw documents.
Discussion of pre-processing and feature extraction is welcomed, and tentative
model(s) should be proposed in the answer.

The ML process to solve this problem will be defined in the next steps:

- Preprocess the entire document to remove irrelevant information, such as stop words, punctuation, and special characters. Tokenize the text and convert it to lowercase.

- Identify the topic paragraphs using topic modelling techniques (Latent Dirichlet Allocation, Non-Negative Matrix Factorization, Latent Semantic Analysis)

- Encode the paragraphs using embedding techniques (Word2vec, Glove, BERT embeddings, Universal Google Sentence Encoder)

- Compare the similarity of the paragraphs which are below the same topic do decide if there are conflict information.

- Iterative Refinement, if the results are not satisfactory, consider refining the preprocessing steps, adjusting model parameters, or trying a different algorithm to improve the conflicting text process approach.

See in the below figure the described process.

