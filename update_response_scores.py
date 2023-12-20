from database import DbContext

db = DbContext("ResponseScoresDb.sqlite")

def update_response_scores(question_text, picked_response_text, other_response_text):
    print(question_text, picked_response_text, other_response_text)

    question = db.get_question_by_name(question_text)
    if question is not None:
        question_id = question[1]
    else:
        question_id = db.add_question(question_text)

    picked_response = db.get_response_by_question_id_and_text(question_id, picked_response_text)
    if picked_response is None:
        db.add_response(question_id, picked_response_text, 1)
    else:
        db.update_response_score(picked_response[0], picked_response[2] + 1)

    other_response = db.get_response_by_question_id_and_text(question_id, other_response_text)
    if other_response is None:
        db.add_response(question_id, other_response_text, -1)
    else:
        db.update_response_score(other_response[0], other_response[2] - 1)


def normalize_response_scores(question_id):
    responses = db.get_responses_by_question_id(question_id)
    print (responses)
    normalized_responses = []

    max_abs = max(abs(response[3]) for response in responses)

    if max_abs != 0:
        normalized_responses = [(response[3] / max_abs) for response in responses]
    else:
        normalized_responses = [0 for _ in responses]

    print(normalized_responses)
    return normalized_responses

