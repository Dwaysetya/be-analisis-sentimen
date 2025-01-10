from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import random
from database import DatabaseConnectionPool

class TestingModel:
    def __init__(self, ratio, k):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool
        self.data_split = {'created_at': [], 'raw_data': [], 'clean_data': [], 'label': []}
        self.test_data = {'created_at': [], 'raw_data': [], 'clean_data': [], 'label': []}
        self.ratio = ratio  # Ratio of training data (e.g., 0.8 means 80% training, 20% testing)
        self.k = k
        self.fetch_data_clean()

    def fetch_data_clean(self):
        label_mapping = {'positive': 1, 'negative': 0}  # Define label mapping
        try:
            with self.connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = '''
                        SELECT dataset.created_at, dataset.raw_data, clean_data.clean_data, label.label
                        FROM tugas_akhir.dataset
                        JOIN tugas_akhir.clean_data ON dataset.id = clean_data.id
                        JOIN tugas_akhir.label ON dataset.id = label.id
                        WHERE label.label IN ('positive', 'negative')  -- Exclude neutral class
                    '''
                    cursor.execute(query)
                    data = cursor.fetchall()

                    for row in data:
                        created_at, raw_data, clean_data, label = row
                        self.data_split['created_at'].append(created_at)
                        self.data_split['raw_data'].append(raw_data)
                        self.data_split['clean_data'].append(clean_data)
                        self.data_split['label'].append(label_mapping[label])  # Map label to binary value

        except Exception as e:
            print("Error retrieving data:", str(e))

    def process_data(self):
        combined_data = list(zip(self.data_split['created_at'], self.data_split['raw_data'],
                                 self.data_split['clean_data'], self.data_split['label']))

        # Shuffle the data randomly before splitting
        random.shuffle(combined_data)

        # Print the label distribution before splitting
        label_distribution_before = [item[3] for item in combined_data]
        print("Label Distribution Before Splitting:")
        print("Positive:", label_distribution_before.count(1))
        print("Negative:", label_distribution_before.count(0))

        # Split data into training and testing sets based on the ratio
        train_size = int(len(combined_data) * self.ratio)
        train_data = combined_data[:train_size]  # Data latih
        test_data = combined_data[train_size:]  # Data uji

        # Print the label distribution after splitting
        train_label_distribution = [item[3] for item in train_data]
        test_label_distribution = [item[3] for item in test_data]
        print("Label Distribution in Train Data:")
        print("Positive:", train_label_distribution.count(1))
        print("Negative:", train_label_distribution.count(0))
        print("Label Distribution in Test Data:")
        print("Positive:", test_label_distribution.count(1))
        print("Negative:", test_label_distribution.count(0))

        # Assign data latih ke self.data_split
        train_created_at, train_raw_data, train_clean_data, train_label = zip(*train_data)
        self.data_split['created_at'] = list(train_created_at)
        self.data_split['raw_data'] = list(train_raw_data)
        self.data_split['clean_data'] = list(train_clean_data)
        self.data_split['label'] = list(train_label)

        # Assign data uji ke self.test_data
        test_created_at, test_raw_data, test_clean_data, test_label = zip(*test_data)
        self.test_data['created_at'] = list(test_created_at)
        self.test_data['raw_data'] = list(test_raw_data)
        self.test_data['clean_data'] = list(test_clean_data)
        self.test_data['label'] = list(test_label)

        # Vectorize data latih
        tfidf_vectorizer = TfidfVectorizer()
        X_train_tfidf = tfidf_vectorizer.fit_transform(self.data_split['clean_data'])

        # Train the KNN model
        knn_model = KNeighborsClassifier(n_neighbors=self.k)
        knn_model.fit(X_train_tfidf, self.data_split['label'])

        # Transform and predict data uji
        X_test_tfidf = tfidf_vectorizer.transform(self.test_data['clean_data'])
        predicted_labels = knn_model.predict(X_test_tfidf)

        # Calculate metrics
        accuracy = accuracy_score(self.test_data['label'], predicted_labels)
        cm = confusion_matrix(self.test_data['label'], predicted_labels)
        precision = precision_score(self.test_data['label'], predicted_labels)
        recall = recall_score(self.test_data['label'], predicted_labels)
        f1 = f1_score(self.test_data['label'], predicted_labels)

        return accuracy, cm, precision, recall, f1, predicted_labels

    def evaluate_model(self):
        accuracy, cm, precision, recall, f1, predicted_labels = self.process_data()
        return {
            'accuracy': accuracy,
            'confusion_matrix': cm.tolist(),
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
