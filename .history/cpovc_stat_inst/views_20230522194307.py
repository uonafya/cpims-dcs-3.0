from django.shortcuts import render

# Create your views here.
def home(request):

    form = OVCSearchForm(initial={'person_type': 'TBVC'})
    context = {
        
    }
    return render(request,'stat_inst/home.html',context)