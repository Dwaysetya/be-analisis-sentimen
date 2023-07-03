from database import DatabaseConnectionPool
from flask import make_response, json
from models.dataset_model import database_model
from models.slangword_model import slangword_model
from models.stopword_model import stopword_model
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import re
import nltk
nltk.download('punkt')
from nltk.tokenize  import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class preprocessing_model():
    def __init__(self):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool
        self.raw_headers = ['id', 'created_at', 'raw_tweet', 'username']
        self.awal_data = []
        self.caseFolding_data = []
        self.cleansing_data = []
        self.normalization_data = []
        self.stopwordsRemoval_data = []
        self.stemming_data = []
        self.tokenizing_data = []
        self.data_akhir = []
        self.slang_headers = ['id', 'kata_baku', 'kata_slang']
        self.stopwords_headers = ['id', 'kata_stop']
    def retrieve_raw_tweets(self):
        try:
            obj = database_model()
            data = obj.get_dataset()

            data_raw = []
            for result in data:
                rs = [str(result['id']), result['created_at'], result['raw_tweet'], result['username']]
                data_raw.append(dict(zip(self.raw_headers, rs)))

            return data_raw
        except Exception as e:
            error_message = f"An error occurred while retrieving raw tweets: {str(e)}"
            # You can log the error or print it for debugging purposes
            print(error_message)
            return []
    def retrieve_slangwords(self):
        try:
            obj = slangword_model()
            slangwords = obj.getall_slangword()

            data_slang = []
            for result in slangwords:
                rs = [str(result['id']), result['kata_baku'], result['kata_slang']]
                data_slang.append(dict(zip(self.slang_headers, rs)))

            return data_slang
        except Exception as e:
            error_message = f"An error occurred while retrieving slang words: {str(e)}"
            # You can log the error or print it for debugging purposes
            print(error_message)
            return []
    def retrieve_stopwords(self):
        try:
            obj = stopword_model()
            stopwords = obj.getall_stopword()

            data_stopwords = []
            for result in stopwords:
                rs = [str(result['id']), result['kata_stop']]
                data_stopwords.append(dict(zip(self.stopwords_headers, rs)))

            return data_stopwords
        except Exception as e:
            error_message = f"An error occurred while retrieving stop words: {str(e)}"
            # You can log the error or print it for debugging purposes
            print(error_message)
            return []
    def normalize_text(self, text):
        # Replace multiple occurrences of specific characters or character patterns
        normalized_text = re.sub(r'(.)\1{2,}', r'\1', text)  # Replacing repeating characters
        normalized_text = re.sub(r'(\w)\1{2,}', r'\1', normalized_text)  # Replacing repeating word characters
        # Add more normalization patterns as needed

        return normalized_text
    def preprocess_data(self, data_raw, data_slang, data_stopwords) :
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            instance_stemming = StemmerFactory()
            stemmer = instance_stemming.create_stemmer()

            for index, data in enumerate(data_raw):
                self.awal_data.append(data['raw_tweet'])

                # Case Folding: Mengubah huruf menjadi huruf kecil
                casefolded_data = data['raw_tweet'].lower()
                self.caseFolding_data.append(casefolded_data)

                # === Menghapus Tautan ===
                cleaned_data = re.sub("\w+:\/\/\S+", " ", casefolded_data)

                # === Menghapus karakter selain huruf ===
                # Menghilangkan mention, hashtag, character reference
                cleaned_data = re.sub('[@#&][A-Za-z0-9_]+', " ", cleaned_data)

                # Menghilangkan tanda baca
                cleaned_data = re.sub('[()!?;,]', ' ', cleaned_data)
                cleaned_data = re.sub('\[.*?\]', ' ', cleaned_data)

                # Menghilangkan tanda selain huruf
                cleaned_data = re.sub("[^a-z]", " ", cleaned_data)

                # === Menghapus 1 karakter ===
                cleaned_data = re.sub(r"\b[a-z]\b", "", cleaned_data)

                # Menghilangkan spasi lebih dari 1
                cleaned_data = ' '.join(cleaned_data.split())
                self.cleansing_data.append(cleaned_data)

                # Merubah slang word ke kata aslinya
                for slang in data_slang:
                    cleaned_data = re.sub(r'\b{}\b'.format(slang['kata_slang']), slang['kata_baku'], cleaned_data)
                self.normalization_data.append(cleaned_data)

                # Menghapus stop word
                for stop in data_stopwords:
                    if stop['kata_stop'] in cleaned_data:
                        cleaned_data = re.sub(r'\b{}\b'.format(stop['kata_stop']), '', cleaned_data)
                self.stopwordsRemoval_data.append(cleaned_data)

                stemmed_data = stemmer.stem(cleaned_data)
                self.stemming_data.append(stemmed_data)

                # Tokenisasi kata
                tokenized_data = word_tokenize(stemmed_data)
                self.tokenizing_data.append(tokenized_data)

                self.data_akhir.append(stemmed_data)

                print(index+1)

            # Move appending operations outside the loop
            for cleaned_tweet in self.data_akhir:
                query = "INSERT INTO clean_data (clean_tweet) VALUES (%s)"
                cursor.execute(query, (cleaned_tweet,))
                connection.commit()

            cursor.close()
            connection.close()

            # Rest of the code remains the same
            response_data = []
            for index, tweet in enumerate(self.awal_data):
                row = {
                    'awal_data': self.awal_data[index],
                    'caseFolding_data': self.caseFolding_data[index],
                    'cleansing_data': self.cleansing_data[index],
                    'normalize_data': self.normalization_data[index],
                    'stopwordsRemoval_data': self.stopwordsRemoval_data[index],
                    'stemming_data': self.stemming_data[index],
                    'tokenizing_data': self.tokenizing_data[index],
                }
                response_data.append(row)

            response = make_response(json.dumps(response_data), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            error_message = f"An error occurred during data preprocessing: {str(e)}"
            # You can log the error or print it for debugging purposes
            print(error_message)
            response_data = {
                'message': 'Error occurred during data preprocessing',
                'status': 501,
                'data': None
            }
            response = make_response(json.dumps(response_data), 500)
            return response
    def preprocessing(self):
        data_raw = self.retrieve_raw_tweets()
        data_slang = self.retrieve_slangwords()
        data_stopwords = self.retrieve_stopwords()
        preprocessed_data = self.preprocess_data(data_raw, data_slang, data_stopwords)
        return preprocessed_data
        