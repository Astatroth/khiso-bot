from core.API import API
from kink import inject
import re


@inject
class Olympiad:
    def __init__(self, api: API):
        self.api = api

    def get_question(self, olympiad_id: int, student_id: int, question_number: int) -> dict:
        return self.api.get(f"olympiad/{olympiad_id}/student/{student_id}/question/{question_number}")

    @staticmethod
    def parse_answers(input_text: str) -> list[dict[str, int | str]] | None:
        lines = [line.strip() for line in re.split(r'\r?\n|\r', input_text.strip()) if line.strip()]
        parsed_answers = []

        for line in lines:
            match = re.match(r'^(\d+)\.([A-Za-z])$', line)
            if match:
                parsed_answers.append({
                    "question_number": int(match.group(1)),
                    "answer": match.group(2)
                })
            else:
                return None

        return parsed_answers

    def send_answer(self, olympiad_id: int, student_id: int, answers: list) -> dict:
        return self.api.put("olympiad/answer", {
            "olympiad_id": olympiad_id,
            "student_id": student_id,
            "answers": answers,
        })

    def start(self, olympiad_id: int, student_id: int) -> dict:
        return self.api.put("olympiad/start", {
            "olympiad_id": olympiad_id,
            "student_id": student_id
        })
