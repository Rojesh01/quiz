import uuid
from django.db import models


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Category(BaseModel):
    category_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category_name

class Question(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    marks = models.IntegerField(default=8)

    def __str__(self) -> str:
        return self.question

    def get_answers(self):
        answer_objs = Answer.objects.filter(question = self)
        data = []
        for answer_obj in answer_objs:
            data.append({
                'answer' : answer_obj.answer,
                'is_correct' : answer_obj.is_correct

            })

        return data
    
    

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer =   models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer
    
    def MCQ(request, question_id):
        question = Question.objects.get(id=question_id)
        if request.method =="POST":
            submitted_answer_id = request.POST.get('option')
            submitted_answer = Answer.objects.get(id=submitted_answer_id)

            
    
    from django.contrib.auth.models import User

class QuizResult(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    passed = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.user.username} - {self.question} - {'Passed' if self.passed else 'Failed'}"
