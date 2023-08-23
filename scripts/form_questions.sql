copy list_questions (id,question_text,question_code,form_type_id,answer_type_id,answer_field_id,answer_set_id,
form,question_required,the_order,timestamp_created,timestamp_updated,is_void)
FROM '/tmp/questions.csv' DELIMITER ',' CSV HEADER;

copy forms (id,form_guid,form_title,form_type_id,form_subject_id,form_area_id,date_began,date_ended,
date_filled_paper,person_id_filled_paper,org_unit_id_filled_paper,
capture_site_id,timestamp_created,user_id_created,timestamp_updated,user_id_updated,is_void)
FROM '/tmp/forms.csv' DELIMITER ',' CSV HEADER;

