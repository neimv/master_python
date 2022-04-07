
import datetime

from django.urls.base import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    
    return Question.objects.create(question_text=question_text, pub_date=time)


# Create your tests here.
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """algo"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="soy una prueba", pub_date=time
        )
        self.assertIs(future_question.was_published_recently(), False)
        

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_question(self):
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
    def test_past_time(self):
        question = create_question("past question", days=-1000)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question]
        )
        
    def test_future_question_and_past_question(self):
        past_question = create_question("Past question", -30)
        future_question = create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [past_question]
        )
    
    def test_two_past_questions(self):
        past_question_1 = create_question("Past question", -30)
        past_question_2 = create_question("Past question", -40)
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question_1, past_question_2]
        )
        

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question", 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        past_question = create_question("Past question", -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        
        self.assertContains(response, past_question.question_text)