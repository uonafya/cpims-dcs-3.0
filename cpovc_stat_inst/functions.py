from datetime import datetime

from cpovc_registry.models import RegOrgUnit

def convert_date(date_string):
    # Parse the input date string using the specified format
    date_object = datetime.strptime(date_string, "%d-%b-%Y")

    # Convert the date object to the desired format "yyyy-mm-dd"
    converted_date = date_object.strftime("%Y-%m-%d")

    return converted_date


def convertYesNo(val):
    if (val == 'AYES'):
        return 'yes'
    elif (val == 'ANNO'):
        return 'no'
    else:
        return 'no'
    
def get_si_reg_list(fields):
    l_tupple = ()
    list = []
    org_units = RegOrgUnit.objects.filter(is_void=False)
    filt_org_units = org_units.filter(org_unit_type_id__in = fields)
    for filt_org_unit in filt_org_units:
        list.append((filt_org_unit.org_unit_id_vis,filt_org_unit.org_unit_name))

    l_tupple = tuple(list)

    return l_tupple