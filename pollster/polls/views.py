from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Question

# Create your views here.

def mama(request):
    content = Question.objects.order_by("pub_date")
    return render(request, "index.html", {"dataPoll": content})

def toDetails(request, question_id):
    data = Question.objects.get(pk=question_id)
    for dat in data.choice_set.all():
        print(dat.choice_text)
    return render(request, "details.html", {"data": data})

def toResults(request, question_id):
    data = Question.objects.get(pk=question_id)
    return render(request, "results.html", {"data": data})

def toVote(request, question_id, choice_id):
    selected_question = Question.objects.get(id=question_id)
    selected_option = selected_question.choice_set.get(id=choice_id)
    selected_option.votes += 1
    selected_option.save()
    return HttpResponseRedirect("/%s/results" % question_id)

def getChart(request, question_id):
    selected_question = Question.objects.get(id=question_id)
    choices = selected_question.choice_set.all()
    valueSeries = []
    for choice in choices:
        valueSeries.append({"choice_txt": choice.choice_text, "choice_votes": choice.votes})
    
    return JsonResponse(valueSeries, safe=False)
    
