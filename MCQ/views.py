from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question, Answer, Category
from django.urls import reverse
import random

def Question_View(request):
    """Display all questions with their answers"""
    questions = Question.objects.select_related('category').prefetch_related('question_answer').all()
    context = {
        'questions': questions,
    }
    return render(request, 'MCQ.html', context)

def quiz(request):
    """Handle quiz taking functionality"""
    questions = Question.objects.select_related('category').prefetch_related('question_answer').all()
    error_message = None

    if request.method == 'POST':
        selected_answers = {}
        score = 0
        total_possible = 0

        for question in questions:
            selected_answer = request.POST.get(f'question_{question.uid}')
            total_possible += question.marks

            if selected_answer:
                selected_answers[str(question.uid)] = selected_answer
                
                correct_answer = question.question_answer.filter(is_correct=True).first()
                if correct_answer and str(correct_answer.uid) == selected_answer:
                    score += question.marks
       
        if not selected_answers:
            error_message = "Please answer at least one question."
            return render(request, 'quiz.html', {
                'questions': questions, 
                'error_message': error_message
            })

        request.session['selected_answers'] = selected_answers
        request.session['score'] = score
        request.session['total_possible'] = total_possible
        
        return redirect(reverse('quiz:quiz_results'))

    return render(request, 'quiz.html', {'questions': questions})

def quiz_results(request):
    """Display quiz results"""
    selected_answers = request.session.get('selected_answers', {})
    score = request.session.get('score', 0)
    total_possible = request.session.get('total_possible', 0)

    if not selected_answers:
        messages.error(request, "No quiz answers found. Please take the quiz first.")
        return redirect(reverse('quiz:quiz'))

    questions = Question.objects.select_related('category').prefetch_related('question_answer').all()
    results = []

    for question in questions:
        user_answer_uid = selected_answers.get(str(question.uid))
        correct_answer = question.question_answer.filter(is_correct=True).first()
        
        if user_answer_uid:
            user_answer = question.question_answer.filter(uid=user_answer_uid).first()
            is_correct = correct_answer and str(correct_answer.uid) == user_answer_uid
            
            results.append({
                'question': question.question,
                'category': question.category.category_name,
                'user_answer': user_answer.answer if user_answer else 'Not answered',
                'correct_answer': correct_answer.answer if correct_answer else 'No correct answer defined',
                'is_correct': is_correct,
                'marks': question.marks
            })

    percentage = (score / total_possible * 100) if total_possible > 0 else 0
    
    context = {
        'results': results,
        'total_questions': questions.count(),
        'score': score,
        'total_possible': total_possible,
        'percentage': round(percentage, 2),
        'passed': percentage >= 70,  
    }

    request.session.pop('selected_answers', None)
    request.session.pop('score', None)
    request.session.pop('total_possible', None)

    return render(request, 'quiz_results.html', context)