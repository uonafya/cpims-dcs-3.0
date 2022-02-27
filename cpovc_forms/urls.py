from django.urls import include, path
import views

# This should contain paths related to registry ONLY
urlpatterns = include(
    # Forms Registry
    'cpovc_forms.views',
    path('/$', views.forms_home, name='forms'),
    path('followups/', views.forms_registry,
         name='forms_registry'),
    # Documents Manager
    path('documents_manager/', views.documents_manager,
         name='documents_manager'),
    path('documents_manager_search/', views.documents_manager,
         name='documents_manager_search'),

    # Case Record Sheet paths
    path('crs/', views.case_record_sheet,
         name='case_record_sheet'),
    path('crs/new/<int:id>/', views.new_case_record_sheet,
         name='new_case_record_sheet'),
    path('crs/view/<int:id>/', views.view_case_record_sheet,
         name='view_case_record_sheet'),
    path('crs/edit/<int:id>/', views.edit_case_record_sheet,
         name='edit_case_record_sheet'),
    path('crs/delete/<int:id>/', views.delete_case_record_sheet,
         name='delete_case_record_sheet'),

    # Alternative Family Care paths
    path('afc/', views.alternative_family_care,
         name='alternative_family_care'),
    path('afc/new/<int:id>/', views.new_alternative_family_care,
         name='new_alternative_family_care'),
    path('afc/edit/<int:id>)/', views.edit_alternative_family_care,
         name='edit_alternative_family_care'),
    path('afc/view/<int:id>/', views.view_alternative_family_care,
         name='view_alternative_family_care'),

    # Residential Placement
    path('placement/save/', views.save_placement, name='save_placement'),

    path('placement/view/<int:id>', views.view_placement, name='view_placement'),

    path('placement/edit/<int:id>/', views.edit_placement, name='edit_placement'),

    path('placement/delete/', views.delete_placement, name='delete_placement'),

    path('placement/', views.residential_placement, name='residential_placement'),

    path('placement/<int:id>)/', views.placement, name='placement'),

    # Residential Placement FollowUp
    path('placement_followup/<int:id>/', views.placement_followup, name='placement_followup'),
    path('save_placementfollowup/', views.save_placementfollowup, name='save_placementfollowup'),
    path('view_placementfollowup/', views.view_placementfollowup, name='view_placementfollowup'),
    path('edit_placementfollowup/', views.edit_placementfollowup, name='edit_placementfollowup'),
    path('delete_placementfollowup/', views.delete_placementfollowup, name='delete_placementfollowup'),
    # Case Events (Encounters/Court Sessions/Referrals/Case
    # Closure/Summons)
    path('case_events/<int:id>', views.case_events, name='case_events'),
    # ---------------------------------------------------------
    path('save_encounter/', views.save_encounter, name='save_encounter'),
    path('view_encounter/', views.view_encounter, name='view_encounter'),
    path('edit_encounter/', views.edit_encounter, name='edit_encounter'),
    path('delete_encounter/', views.delete_encounter, name='delete_encounter'),
    # ----------------------------------------------------------
    path('save_court/', views.save_court, name='save_court'),
    path('view_court/', views.view_court, name='view_court'),
    path('edit_court/', views.edit_court, name='edit_court'),
    path('delete_court/', views.delete_court, name='delete_court'),
    # ----------------------------------------------------------
    path('save_summon/', views.save_summon, name='save_summon'),
    path('edit_summon/', views.edit_summon, name='edit_summon'),
    path('view_summon/', views.view_summon, name='view_summon'),
    path('delete_summon/', views.delete_summon, name='delete_summon'),
    # ----------------------------------------------------------
    path('save_closure/', views.save_closure, name='save_closure'),
    path('edit_closure/', views.edit_closure, name='edit_closure'),
    path('view_closure/', views.view_closure, name='view_closure'),
    path('delete_closure/', views.delete_closure, name='delete_closure'),

    # Referrals
    path('delete_referral/', views.delete_referral, name='delete_referral'),

    # Management paths
    path('manage_refferal/', views.manage_reffera, name='manage_refferal'),
    path('manage_refferal001/', views.manage_refferal001, name='manage_refferal001'),
    path('manage_refferal002/', views.manage_refferal002, name='manage_refferal002'),
    path('manage_refferal003/', views.manage_refferal003, name='manage_refferal003'),
    path('manage_casecategory001/', views.manage_casecategory001, name='manage_casecategory001'),
    path('manage_casecategory002/', views.manage_casecategory002, name='manage_casecategory002'),
    path('manage_casecategory003/', views.manage_casecategory003, name='manage_casecategory003'),
    path('manage_casecategory004/', views.manage_casecategory004, name='manage_casecategory004'),
    path('manage_encounters001/', views.manage_encounters001, name='manage_encounters001'),
    path('manage_encounters004/', views.manage_encounters004, name='manage_encounters004'),
    path('manage_case_events/', views.manage_case_events, name='manage_case_events'),
    path('manage_placementfollowup/', views.manage_placementfollowup, name='manage_placementfollowup'),
    path('manage_schools/', views.manage_schools, name='manage_schools'),
    path('manage_countries/', views.manage_countries, name='manage_countries'),
    path('manage_casehistory/', views.manage_casehistory, name='manage_casehistory'),
    path('manage_service_category/', views.manage_service_category, name='manage_service_category'),
    path('manage_form_type/', views.manage_form_type, name='manage_form_type'),
    # ---------------------------------------------------------------
    path('userorgunits_lookup/', views.userorgunits_lookup, name='userorgunits_lookup'),
    path('usersubcounty_lookup/', views.usersubcounty_lookup, name='usersubcounty_lookup'),
    path('userward_lookup/', views.userward_lookup, name='userward_lookup'),
    path('generate_serialnumber/', views.generate_serialnumber, name='generate_serialnumber'),
    path('getJsonObject001/', views.getJsonObject001, name='getJsonObject001'),
    # Search paths
    path('ovc_search/', views.ovc_search, name='ovc_search'),

    # School & Bursary paths
    path('education/', views.background_details, name='background_details'),
    path('education/new/<int:id>/', views.new_education_info, name='new_education_info'),
    path('education/edit/<int:id>/', views.edit_education_info, name='edit_education_info'),
    path('education/view/<int:id>/', views.view_education_info, name='view_education_info'),
    path('education/delete/<int:id>/', views.delete_education_info, name='delete_education_info'),
    # -----------------------------------------------------------------
    path('school/', views.new_schoo, name='new_school'),
    # ------------------------------------------------------------------
    path('bursary/new/', views.new_bursary_info, name='new_bursary_info'),
    path('bursary/edit/', views.edit_bursary_info, name='edit_bursary_info'),
    path('bursary/view/', views.view_bursary_info, name='view_bursary_info'),
    path('bursary/delete/', views.delete_bursary_info, name='delete_bursary_info'),
    path('bursary/followup/<int:id>/', views.bursary_followup, name='bursary_followup'),
    path('bursary/manage/', views.manage_bursary, name='manage_bursary'),
    # OVC Care - CSI
    path('csi/', views.csi, name='csi'),
    path('csi/new/<int:id>/', views.new_csi, name='new_csi'),
    path('csi/edit/<int:id>/', views.edit_csi, name='edit_csi'),
    path('csi/view/<int:id>/', views.view_csi, name='view_csi'),
    path('csi/delete/<int:id>/', views.delete_csi, name='delete_csi'),
    # OVC Care - Form1A
    path('form1a/new/<int:id>/', views.form1a_events, name='form1a_events'),
    path('form1a/save/', views.save_form1a, name='save_form1a'),
    path('form1a/edit/', views.edit_form1a, name='edit_form1a'),
    path('form1a/view/', views.view_form1a, name='view_form1a'),
    path('form1a/delete/', views.delete_form1a, name='delete_form1a'),
    path('form1a/manage/', views.manage_form1a_events, name='manage_form1a_events'),
    # OVC Care - Form1B
    path('form1b/new/<int:id>)/$', views.new_form1b, name='new_form1b'),
    # OVC Care - HHVA
    path('hhva/new/<int:id>/', views.new_hhva, name='new_hhva'),
    path('hhva/edit/<int:id>/', views.edit_hhva, name='edit_hhva'),
    path('hhva/view/<int:id>/', views.view_hhva, name='view_hhva'),
    path('hhva/delete/<int:id>/', views.delete_hhva, name='delete_hhva'),
    # Presidential Bursary
    path('bursary/new/<int:id>)/', views.new_bursary, name='new_bursary'),
    path('case/<uuid:case_id>/$', views.case_info, name='case_info'),
)
