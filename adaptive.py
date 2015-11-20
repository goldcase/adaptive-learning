from __future__ import division
import json, random
from collections import defaultdict

DIFFICULTY_MULTIPLIER = 400

class Question(object):
    def __init__(self, question = None):
        if question is None:
            raise

        self._question_type = question["question_type"]
        self.difficulty     = question["difficulty"]
        self._topics        = question["topics"]
        self.question_text  = question["question_text"]
        self.choices        = question["choices"]
        self.hints          = question["hints"]
        self._answer        = question["answer"]
        self.attempts       = 0
        self.correct        = 0

    def is_answer(self, candidate):
        return candidate == self._answer

    def get_answer(self):
        return self._answer

    def get_accuracy(self):
        return self.correct/self.attempts

    def seen(self):
        return self.attempts > 0

    def get_text(self):
        return self.question_text

    def get_choices(self):
        return self.choices

class QuestionEngine(object):
    def __init__(self, filename = None):
        if filename is None:
            raise
        else:
            self.difficulty_multiplier = 400
            self.questions = defaultdict(list)
            with open(filename) as f:
                data = json.load(f)
                for q in data:
                    question = Question(q)
                    for topic in question._topics:
                        self.questions[topic].append(question)

    def get_difficulty(self, q):
        return self.difficulty_multiplier * q.difficulty

    def get_question(self, topic, topic_score):
        if topic in self.questions:
            potential_questions = self.questions[topic]
            for q in potential_questions:
                if self.get_difficulty(q) > topic_score:
                    return q
        else:
            raise

    def get_topics(self):
        return self.questions.keys()

class Player(object):
    def __init__(self, firstname = "A", lastname = "Student", netid = None, filename = None):
        self.firstname    = firstname
        self.lastname     = lastname
        self.netid        = netid
        self.engine       = QuestionEngine(filename)
        self.topics       = self.engine.get_topics()
        self.topic_scores = defaultdict(float)

    def get_score(self, topic):
        return self.topic_scores[topic]

    def get_question(self, topic):
        return self.engine.get_question(topic, self.get_score(topic))

    def get_random_question(self):
        return self.get_question(random.choice(self.topics))

player = Player(filename = "questions.json")
question = player.get_question("Dubstep")
print question.get_text()
print "Choices:"
for c in question.get_choices():
    print c
