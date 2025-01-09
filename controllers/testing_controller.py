from app import app
from flask import request, jsonify
from models.testing_model import TestingModel

@app.route('/testing', methods=['POST'])
def run_testing():
    data = request.get_json()
    print("booookk")
    print(data)

    # 9:1
    # 9.1
    # atau hasilnya 9:1

    ratio = float(data['ratio']) if data.get('ratio') is not None else None
    k = int(data['k']) if 'k' in data else None

    if ratio is None:
        return jsonify({'error': 'Ratio value is required.'}), 400

    testing_model = TestingModel(ratio, k)
    accuracy, cm, precision, recall, f1, predicted_labels = testing_model.process_data()

    # Map labels to "positive" and "negative" for clarity
    testing_model.data_split['label'] = ['positive' if label == 1 else 'negative' for label in testing_model.data_split['label']]
    testing_model.test_data['label'] = ['positive' if label == 1 else 'negative' for label in testing_model.test_data['label']]
    predicted_labels = ['positive' if label == 1 else 'negative' for label in predicted_labels]

    positive_count = testing_model.test_data['label'].count('positive')
    negative_count = testing_model.test_data['label'].count('negative')

    response = {
        'accuracy': accuracy,
        'confusion_matrix': cm.tolist(),
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'training_data': [
            {
                'raw_data': tweet,
                'label': label
            }
            for tweet, label in zip(
                testing_model.data_split['clean_data'],
                testing_model.data_split['label']
            )
        ],
        'testing_data': [
            {
                'raw_data': tweet,
                'actual_label': actual_label,
                'predicted_label': predicted_label
            }
            for tweet, actual_label, predicted_label in zip(
                testing_model.test_data['clean_data'],
                testing_model.test_data['label'],
                predicted_labels
            )
        ]
    }

    return jsonify(response)
