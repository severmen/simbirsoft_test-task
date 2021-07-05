from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        result = 0
        count_answer = 0
        for a in self.quiz_dto.questions:
            count_answer += 1

        for a in self.quiz_dto.questions:
            list_good_result = []
            for b in a.choices:
                if b.is_correct == True:
                    list_good_result.append(b.uuid)
            global_virgin = True
            z = self.answers_dto.answers[int(a.uuid) - 1]
            for c in list_good_result:
                virgin = True
                for f in range(int(count_answer)):
                    for b in range(len(z.choices)):
                        if z.choices[b] == c:
                            virgin = False
                            del z.choices[b]
                            break
                if virgin == True:
                    global_virgin = False
            if global_virgin == True and len(z.choices) == 0:
                result += round((100/count_answer)*0.01,2)
        return result
        # your code here
