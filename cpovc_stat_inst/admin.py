from django.contrib import admin
from .models import SI_Admission, SI_NeedRiskAssessment, SI_NeedRiskScale, SI_SocialInquiry, SI_VacancyApp

# Register your models here.

class SI_AdmissionAdmin(admin.ModelAdmin):

    search_fields = ['person', 'institution_type']
    list_display = ['type_of_entry']
    list_filter = ['referral_source_others']

    # def get_creator(self, obj):
    #     return obj.case.created_by


admin.site.register(SI_Admission, SI_AdmissionAdmin)