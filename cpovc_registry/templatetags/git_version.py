"""Method to create template tag."""
from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def git_version(context):
    """Hard coded version numbering."""
    try:
        git_short = '1.4.3'
<<<<<<< HEAD
    except Exception as e:
        print (str(e))
=======
    except Exception, e:
        print str(e)
>>>>>>> origin/main
        return '1.3.6'
    else:
        return git_short
