from core.API import API
from kink import inject


@inject
class Olympiad:
    def __init__(self, api: API):
        self.api = api

    def get_question(self, olympiad_id: int, student_id: int, question_number: int) -> dict:
        return self.api.get(f"olympiad/{olympiad_id}/student/{student_id}/question/{question_number}")

    def send_answer(self, question_id: int, answer_id: int, student_id: int) -> dict:
        return self.api.put("olympiad/answer", {
            "question_id": question_id,
            "answer_id": answer_id,
            "student_id": student_id
        })

    def start(self, olympiad_id: int, student_id: int) -> dict:
        return self.api.put("olympiad/start", {
            "olympiad_id": olympiad_id,
            "student_id": student_id
        })
