copy list_questions (id,question_text,question_code,form_type_id,answer_type_id,answer_field_id,answer_set_id,
form,question_required,the_order,timestamp_created,timestamp_updated,is_void)
FROM '/tmp/SI_questions.csv' DELIMITER ',' CSV HEADER;