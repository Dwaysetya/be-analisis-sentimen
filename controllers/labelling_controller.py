from app import app
from flask import jsonify, request
from models.labelling_model import LabelingService
from database import DatabaseConnectionPool

@app.route('/labelling', methods=['GET'])
def get_labelling():
    connection_pool = DatabaseConnectionPool.get_instance().connection_pool
    labeling_service = LabelingService(connection_pool)

    try:
        clean_tweet = labeling_service.get_clean_tweet()

        # Load positive and negative lexicons
        negative_lexicon = labeling_service.load_lexicon('negative.tsv')
        positive_lexicon = labeling_service.load_lexicon('positive.tsv')

        # Label the tweets
        labeled_tweets = labeling_service.label_tweets(clean_tweet, negative_lexicon, positive_lexicon)

        # Save the labels to the database
        labeling_service.save_labels(labeled_tweets)

        # Count total data positive and negative
        labeling_service.count_dataset()
        return "Successfully labeled tweets"
    except Exception as e:
        error_message = {"message": "Error processing request", "error": str(e)}
        return jsonify(error_message), 500
    finally:
        labeling_service.close_connection()
@app.route('/label/update/<id>', methods=['PUT'])
def update_label(id):
    connection_pool = DatabaseConnectionPool.get_instance().connection_pool
    labeling_service = LabelingService(connection_pool)
    data = request.get_json()
    return labeling_service.update_label(id, data)