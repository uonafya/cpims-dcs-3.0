# Fool proofing
from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib import messages
from cpovc_ovc.models import OVCRegistration


def validate_ovc(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        url_parts = request.path_info.split('/')
        # e.g /forms/f1a/new/4052597/
        person_id = url_parts[4] if len(url_parts) >= 4 else None
        print(len(url_parts), url_parts)
        ovc = get_ovc(person_id)
        if person_id and ovc:
            if ovc.is_active:
                return function(request, *args, **kwargs)
            else:
                # Inactive OVC take back to view page
                msg = 'Service provision to exited OVC not allowed.'
                messages.error(request, msg)
                url = '/ovcare/view/%s/' % (person_id)
                return HttpResponseRedirect(url)
        else:
            msg = 'Invalid URL or OVC Record.'
            messages.error(request, msg)
            return HttpResponseRedirect('/ovcare/')

    return wrap


def get_ovc(cpims_id):
    """Method to get ovc."""
    try:
        ovc = OVCRegistration.objects.get(person_id=cpims_id)
    except Exception:
        return False
    else:
        return ovc
