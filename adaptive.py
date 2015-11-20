import json
from collections import defaultdict
from __future__ import division

DIFFICULTY_MULTIPLIER = 400

class Question(object):
    def __init__(self, question = None):
        if question is None:
            raise

        self._question_type = question.question_type
        self.difficulty     = question.difficulty
        self._topics        = question.topics
        self.question_text  = question.question_text
        self.choices        = question.choices
        self.hints          = question.hints
        self._answer        = question.answer
        self.attempts       = 0
        self.correct        = 0

    def is_answer(self, candidate):
        return candidate == self._answer

    def get_answer(self):
        return self._answer

    def get_accuracy(self):
        return self.correct/self.attempts

class QuestionEngine(object):
    def __init__(self, filename = "questions.json"):
        if filename is None:
            raise IOError
        else:
            self.questions = defaultdict(list)
            with open(filename, encoding="UTF-8") as f:
                data = json.load(f)
                for q in data:
                    question = Question(q)
                    self.questions[question._topics].append(question)

    def get_question(self, topic, topic_score):
        if topic in self.questions:
            self.questions[topic][0]
        else:
            raise

class Player(object):
    def __init__(self, firstname = "A", lastname = "Student", netid = None):
        self.firstname = firstname
        self.lastname = lastname
        self.netid = netid
        self.engine = QuestionEngine()
        self.topic_scores = defaultdict(float)

q = QuestionEngine("questions.json")
