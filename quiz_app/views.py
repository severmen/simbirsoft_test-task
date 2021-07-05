from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.template.defaulttags import register
# Create your views here.
from quiz.dto import *
from quiz.services import *
import re
import copy
@register.filter
def get_answer_with_uuid(value):
    uuid = 1
    result = []
    for a in value:
        result.append({"answer":a,"uuid":uuid})
        uuid+=1
    return result


@register.filter
def check_old_answer(uuid,cookies):
    for a in cookies:
        print(a)
        if a == "uuid"+str(uuid):
            b = cookies.get(a).split(" ")
            buffer = []
            for a in b:
                try:
                    buffer.append(int(a))
                except Exception:
                    pass
            return buffer


def start(request):

    ren = render(request, "start.html")
    for a in request.COOKIES:
        ren.delete_cookie(a)
    return ren


def questions(request, number):
    def save_result():
        '''
        Записывает переданные пользователем значения в cookie
        '''
        def get_form_request_get():
            '''
                функция возврощает результат ответа пользователя
            '''
            result = ""
            if request.GET.get("previous") != None:
                return result
            result = " "
            for a in request.GET:
                if a != "previous":
                    result += str(a)+" "
            return result
        if get_form_request_get() != "":
            questions_render.set_cookie("uuid"+str(int(number)-1), get_form_request_get())
    new_question_url = {"have": False, "url": ""}
    old_question_url = {"have": False, "url": ""}
    def check_new_question_url(new_question_url):
        '''
        функция возвращает  url на новый вопрос если такое возможно
        '''
        try:
            Question.objects.get(uuid=int(number)+1)
            return {"have": True, "url":"/questions_"+str(int(number)+1), }
        except Exception:
            pass

    def check_old_question_url(old_question_url):
        '''
          функция возвращает  url на старый вопрос если такое возможно
        '''
        try:
            Question.objects.get(uuid=int(number)-1)
            return  {"have": True, "url":"/questions_"+str(int(number)-1),}
        except Exception:
            pass

    try:
        question = Question.objects.get(uuid = int(number))
        answer = Choice.objects.filter(Question = question)
        new_question_url = check_new_question_url(new_question_url)
        old_question_url = check_old_question_url(old_question_url)
    except Exception as e:
        def check_last_number():
            '''
                функция возвращает в виде числа последний
                 записанный uuid ответа пользователя
            '''
            last_count = ""
            max = 0
            for b in request.COOKIES:
                last_count = re.findall(r"[0-9]{1,3}", b)
                if int(last_count[0])>int(max):
                    max = copy.copy(last_count[0])
            return int(max)
        result_user = ""
        for a in request.GET:
            result_user += a + " "
        count = check_last_number() + 1
        request.COOKIES['uuid' + str(count)] = result_user
        return result(request)


    context = {
        "question":question,
        "answer":answer,
        "new_question_url":new_question_url,
        "old_question_url":old_question_url,
        'cookies':request.COOKIES
    }
    questions_render = render(request, 'questions.html', context)
    save_result()
    return questions_render

def result(request):
    def answer():
        '''
        функция возвращает словарь типа AnswersDTO
        с ответами пользователя считанного из куки
        '''
        list_AnswersDTO = []
        #записываем последний ответ на вопрос
        for a in request.COOKIES:
            try:
                number = re.findall(r"[0-9]{1,3}", a)
                one_answer = request.COOKIES.get("uuid"+number[0])
                list_AnswersDTO.append(AnswerDTO(question_uuid=number,
                                                 choices = re.findall(r"[0-9]{1,3}", one_answer)))
            except Exception:
                pass
        return list_AnswersDTO

    def question():
        '''
        функция возвращает словарь типа QuestionDTO
        с всеми вопросами
        '''
        # заполянме ChoiceDTO и Question
        list_QuestionDTO = []
        for a in Question.objects.all():
            list_ChoiceDTO = []
            count_list_ChoiceDTO = 1
            for b in Choice.objects.filter(Question = a):
                list_ChoiceDTO.append(ChoiceDTO(uuid = str(count_list_ChoiceDTO),
                                                text = b.text,
                                                is_correct=b.is_correct))
                count_list_ChoiceDTO += 1
            list_QuestionDTO.append(QuestionDTO(uuid = str(a.uuid),
                                    text = a.text,
                                    choices = list_ChoiceDTO))
        return list_QuestionDTO
    quiz = QuizResultService(QuizDTO(
            uuid = "1",
            title = "Тест по теме язык python",
            questions = question()),
        AnswersDTO(
            quiz_uuid = "1",
            answers = answer(),
        ))

    return render(request, "finish.html", {
      "result": str(quiz.get_result()),
    })