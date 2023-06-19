from django.shortcuts import render

from cpovc_forms.forms import (
    OVCSearchForm
    

# Create your views here.
def home(request):

    form = OVCSearchForm(initial={})
    context = {
        
    }
    return render(request,'stat_inst/home.html',context)