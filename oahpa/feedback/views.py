from django.template import Context, loader
from forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.utils.translation import ugettext as _


def feedback(request):

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST) # A form bound to the POST data
        if feedback_form.is_valid():
            message = feedback_form.cleaned_data['message']
            name = feedback_form.cleaned_data['name']
            email = feedback_form.cleaned_data['email']
            place = feedback_form.cleaned_data['place']
            confirmation = feedback_form.cleaned_data['confirmation']
            #print message, name, email, place

            feedback = Feedback.objects.create(message=message, name=name, email=email, place=place, \
                                               confirmation = confirmation)
            feedback.save()

        c = Context({
            'form': feedback_form,
            })
        
        return render_to_response('thankyou.html', c)

    else:
        feedback_form = FeedbackForm()

        c = Context({
            'form': feedback_form,
            })

        return render_to_response('feedback.html', c)
