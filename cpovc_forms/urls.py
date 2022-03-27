from django.urls import re_path
from . import views
# This should contain urls related to registry ONLY
urlpatterns = [
    # Forms Registry
    # 'cpovc_forms.views,
    re_path(r'^$', views.forms_home, name='forms'),
    re_path(r'^followups/$', views.forms_registry, name='forms_registry'),

    # Documents Manager
    re_path(r'^documents_manager/$', views.documents_manager, name='documents_manager'),
    re_path(r'^documents_manager_search/$', views.documents_manager_search, name='documents_manager_search'),

    # Case Record Sheet Urls
    re_path(r'^crs/$', views.case_record_sheet, name='case_record_sheet'),
    re_path(r'^crs/new/(?P<id>\d+)/$', views.new_case_record_sheet, name='new_case_record_sheet'),
    re_path(r'^crs/view/(?P<id>\w+)/$', views.view_case_record_sheet, name='view_case_record_sheet'),
    re_path(r'^crs/edit/(?P<id>\w+)/$', views.edit_case_record_sheet, name='edit_case_record_sheet'),
    re_path(r'^crs/delete/(?P<id>\w+)/$', views.delete_case_record_sheet, name='delete_case_record_sheet'),

    # Alternative Family Care Urls
    re_path(r'^afc/$', views.alternative_family_care, name='alternative_family_care'),
    re_path(r'^afc/new/(?P<id>\d+)/$', views.new_alternative_family_care, name='new_alternative_family_care'),
    re_path(r'^afc/edit/(?P<id>\w+)/$', views.edit_alternative_family_care, name='edit_alternative_family_care'),
    re_path(r'^afc/view/(?P<id>\w+)/$', views.view_alternative_family_care, name='view_alternative_family_care'),

    # Residential Placement
    re_path(r'^placement/save/$', views.save_placement, name='save_placement'),
    re_path(r'^placement/view/(?P<id>\w+)/$', views.view_placement, name='view_placement'),
    re_path(r'^placement/edit/(?P<id>\w+)/$', views.edit_placement, name='edit_placement'),
    re_path(r'^placement/delete/$', views.delete_placement, name='delete_placement'),
    re_path(r'^placement/$', views.residential_placement, name='residential_placement'),
    re_path(r'^placement/(?P<id>\d+)/$', views.placement, name='placement'),

    # Residential Placement FollowUp
    re_path(r'^placement_followup/(?P<id>\d+)/$', views.placement_followup, name='placement_followup'),
    re_path(r'^save_placementfollowup/$', views.save_placementfollowup, name='save_placementfollowup'),
    re_path(r'^view_placementfollowup/$', views.view_placementfollowup, name='view_placementfollowup'),
    re_path(r'^edit_placementfollowup/$', views.edit_placementfollowup, name='edit_placementfollowup'),
    re_path(r'^delete_placementfollowup/$', views.delete_placementfollowup, name='delete_placementfollowup'),

    # Case Events (Encounters/Court Sessions/Referrals/Case
    # Closure/Summons)
    re_path(r'^case_events/(?P<id>\w+)/$', views.case_events, name='case_events'),
    # ---------------------------------------------------------
    re_path(r'^save_encounter/$', views.save_encounter, name='save_encounter'),
    re_path(r'^view_encounter/$', views.view_encounter, name='view_encounter'),
    re_path(r'^edit_encounter/$', views.edit_encounter, name='edit_encounter'),
    re_path(r'^delete_encounter/$', views.delete_encounter, name='delete_encounter'),
    # ----------------------------------------------------------
    re_path(r'^save_court/$', views.save_court, name='save_court'),
    re_path(r'^view_court/$', views.view_court, name='view_court'),
    re_path(r'^edit_court/$', views.edit_court, name='edit_court'),
    re_path(r'^delete_court/$', views.delete_court, name='delete_court'),
    # ----------------------------------------------------------
    re_path(r'^save_summon/$', views.save_summon, name='save_summon'),
    re_path(r'^edit_summon/$', views.edit_summon, name='edit_summon'),
    re_path(r'^view_summon/$', views.view_summon, name='view_summon'),
    re_path(r'^delete_summon/$', views.delete_summon, name='delete_summon'),
    # ----------------------------------------------------------
    re_path(r'^save_closure/$', views.save_closure, name='save_closure'),
    re_path(r'^edit_closure/$', views.edit_closure, name='edit_closure'),
    re_path(r'^view_closure/$', views.view_closure, name='view_closure'),
    re_path(r'^delete_closure/$', views.delete_closure, name='delete_closure'),

    # Referrals
    re_path(r'^delete_referral/$', views.delete_referral, name='delete_referral'),

    # Management Urls
    re_path(r'^manage_refferal/$', views.manage_refferal, name='manage_refferal'),
    re_path(r'^manage_refferal001/$', views.manage_refferal001, name='manage_refferal001'),
    re_path(r'^manage_refferal002/$', views.manage_refferal002, name='manage_refferal002'),
    re_path(r'^manage_refferal003/$', views.manage_refferal003, name='manage_refferal003'),
    re_path(r'^manage_casecategory001/$', views.manage_casecategory001, name='manage_casecategory001'),
    re_path(r'^manage_casecategory002/$', views.manage_casecategory002, name='manage_casecategory002'),
    re_path(r'^manage_casecategory003/$', views.manage_casecategory003, name='manage_casecategory003'),
    re_path(r'^manage_casecategory004/$', views.manage_casecategory004, name='manage_casecategory004'),
    re_path(r'^manage_encounters001/$', views.manage_encounters001, name='manage_encounters001'),
    re_path(r'^manage_encounters004/$', views.manage_encounters004, name='manage_encounters004'),
    re_path(r'^manage_case_events/$', views.manage_case_events, name='manage_case_events'),
    re_path(r'^manage_placementfollowup/$', views.manage_placementfollowup, name='manage_placementfollowup'),
    re_path(r'^manage_schools/$', views.manage_schools, name='manage_schools'),
    re_path(r'^manage_countries/$', views.manage_countries, name='manage_countries'),
    re_path(r'^manage_casehistory/$', views.manage_casehistory, name='manage_casehistory'),
    re_path(r'^manage_service_category/$', views.manage_service_category, name='manage_service_category'),
    re_path(r'^manage_form_type/$', views.manage_form_type, name='manage_form_type'),
    # ---------------------------------------------------------------
    re_path(r'^userorgunits_lookup/$', views.userorgunits_lookup, name='userorgunits_lookup'),
    re_path(r'^usersubcounty_lookup/$', views.usersubcounty_lookup, name='usersubcounty_lookup'),
    re_path(r'^userward_lookup/$', views.userward_lookup, name='userward_lookup'),
    re_path(r'^generate_serialnumber/$', views.generate_serialnumber, name='generate_serialnumber'),
    re_path(r'^getJsonObject001/$', views.getJsonObject001, name='getJsonObject001'),

    # Search Urls
    re_path(r'^ovc_search/$', views.ovc_search, name='ovc_search'),

    # School & Bursary Urls
    re_path(r'^education/$', views.background_details, name='background_details'),
    re_path(r'^education/new/(?P<id>\d+)/$', views.new_education_info, name='new_education_info'),
    re_path(r'^education/edit/(?P<id>\w+)/$', views.edit_education_info, name='edit_education_info'),
    re_path(r'^education/view/(?P<id>\w+)/$', views.view_education_info, name='view_education_info'),
    re_path(r'^education/delete/(?P<id>\w+)/$', views.delete_education_info, name='delete_education_info'),
    # -----------------------------------------------------------------
    re_path(r'^school/$', views.new_school, name='new_school'),
    # ------------------------------------------------------------------
    re_path(r'^bursary/new/$', views.new_bursary_info, name='new_bursary_info'),
    re_path(r'^bursary/edit/$', views.edit_bursary_info, name='edit_bursary_info'),
    re_path(r'^bursary/view/$', views.view_bursary_info, name='view_bursary_info'),
    re_path(r'^bursary/delete/$', views.delete_bursary_info, name='delete_bursary_info'),
    re_path(r'^bursary/followup/(?P<id>\d+)/$', views.bursary_followup, name='bursary_followup'),
    re_path(r'^bursary/manage/$', views.manage_bursary, name='manage_bursary'),
    # OVC Care - CSI
    re_path(r'^csi/$', views.csi, name='csi'),
    re_path(r'^csi/new/(?P<id>\d+)/$', views.new_csi, name='new_csi'),
    re_path(r'^csi/edit/(?P<id>\w+)/$', views.edit_csi, name='edit_csi'),
    re_path(r'^csi/view/(?P<id>\w+)/$', views.view_csi, name='view_csi'),
    re_path(r'^csi/delete/(?P<id>\w+)/$', views.delete_csi, name='delete_csi'),
    # OVC Care - Form1A
    re_path(r'^form1a/new/(?P<id>\d+)/$', views.form1a_events, name='form1a_events'),
    re_path(r'^form1a/save/$', views.save_form1a, name='save_form1a'),
    re_path(r'^form1a/edit/$', views.edit_form1a, name='edit_form1a'),
    re_path(r'^form1a/view/$', views.view_form1a, name='view_form1a'),
    re_path(r'^form1a/delete/$', views.delete_form1a, name='delete_form1a'),
    re_path(r'^form1a/manage/$', views.manage_form1a_events, name='manage_form1a_events'),
    # OVC Care - Form1B
    re_path(r'^form1b/new/(?P<id>\d+)/$', views.new_form1b, name='new_form1b'),
    # OVC Care - HHVA
    re_path(r'^hhva/new/(?P<id>\d+)/$', views.new_hhva, name='new_hhva'),
    re_path(r'^hhva/edit/(?P<id>\w+)/$', views.edit_hhva, name='edit_hhva'),
    re_path(r'^hhva/view/(?P<id>\w+)/$', views.view_hhva, name='view_hhva'),
    re_path(r'^hhva/delete/(?P<id>\w+)/$', views.delete_hhva, name='delete_hhva'),
    # Presidential Bursary
    re_path(r'^bursary/new/(?P<id>\d+)/$', views.new_bursary, name='new_bursary'),
    re_path(r'^case/(?P<case_id>[0-9A-Za-z_\-{32}\\Z]+)/$', views.case_info, name='case_info'),
]
