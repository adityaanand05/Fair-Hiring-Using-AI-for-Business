# views.py
from django.shortcuts import render, redirect
from .forms import CandidateForm
from .models import Candidate
from AI_code import analyze_candidate  

def submit_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            
           
            ai_result = analyze_candidate(candidate)  
            candidate.ai_result = ai_result
            candidate.save()

            return render(request, 'result.html', {'result': ai_result})
    else:
        form = CandidateForm()
    
    return render(request, 'form.html', {'form': form})

