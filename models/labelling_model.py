from flask import jsonify, make_response, json

class LabelingService:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def get_clean_tweet(self):
        try:
            with self.connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT clean_tweet FROM clean_data"
                    cursor.execute(query)
                    clean_tweet = [row[0] for row in cursor.fetchall()]
                    return clean_tweet
        except Exception as e:
            error_message = {"message": "Error getting clean tweets", "error": str(e)}
            return jsonify(error_message), 500

    def load_lexicon(self, lexicon_file):
        lexicon = {}

        with open(lexicon_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]  # Skip the header row

            for line in lines:
                word, weight = line.strip().split('\t')
                lexicon[word] = int(weight)

        return lexicon

    def label_tweets(self, clean_tweets, negative_lexicon, positive_lexicon):
        labeled_tweets = []

        for tweet in clean_tweets:
            label = self.calculate_label(tweet, negative_lexicon, positive_lexicon)
            labeled_tweets.append((tweet, label))

        return labeled_tweets

    def calculate_label(self, tweet, negative_lexicon, positive_lexicon):
        score = 0

        for word in tweet.split():
            if word in negative_lexicon:
                score += negative_lexicon[word]
            if word in positive_lexicon:
                score += positive_lexicon[word]
            
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'

    def save_labels(self, labeled_tweets):
        try:
            with self.connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    for _, label in labeled_tweets:
                        query = "INSERT INTO label (label) VALUES (%s)"
                        cursor.execute(query, (label,))
                connection.commit()
            print("Labels saved successfully")
        except Exception as e:
            print("Error saving label:", str(e))
    def count_dataset(self):
        try:
            with self.connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT label FROM label"
                    cursor.execute(query)
                    labels = [row[0] for row in cursor.fetchall()]
                    
                    positive_count = labels.count('positive')
                    negative_count = labels.count('negative')
                    neutral_count = labels.count('neutral')

                    print(positive_count, negative_count, neutral_count)
                    
                    return positive_count, negative_count
        except Exception as e:
            error_message = {"message": "Error counting dataset", "error": str(e)}
            return jsonify(error_message), 500

    def update_label(self, id, data):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Update the slangword in the table
            query = "UPDATE label SET label = %s WHERE id = %s"
            cursor.execute(query, (data['label'], id))
            connection.commit()
            return f'Label with ID {id} updated successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def close_connection(self):
        # No need for this method since connection is handled by the context manager
        pass
