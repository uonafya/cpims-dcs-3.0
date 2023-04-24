-- public.rpt_inst_population definition

-- Drop table

-- DROP TABLE public.rpt_inst_population;

CREATE TABLE public.rpt_inst_population (
	id serial4 NOT NULL,
	case_serial varchar(40) NOT NULL,
	admission_number varchar(40) NOT NULL,
	org_unit_name varchar(250) NULL,
	org_unit_type_id varchar(4) NULL,
	org_unit_type varchar(250) NULL,
	sex_id varchar(4) NOT NULL,
	sex varchar(10) NOT NULL,
	dob date NULL,
	age int4 NULL,
	age_now int4 NULL,
	age_range varchar(20) NULL,
	knbs_age_range varchar(20) NULL,
	admission_date date NOT NULL,
	admission_type_id varchar(4) NOT NULL,
	admission_type varchar(250) NOT NULL,
	admission_reason_id varchar(4) NOT NULL,
	admission_reason varchar(250) NOT NULL,
	case_status_id int4 NOT NULL,
	case_status varchar(20) NOT NULL,
	case_category_id varchar(4) NOT NULL,
	case_category varchar(250) NOT NULL,
	sub_category_id varchar(4) NOT NULL,
	sub_category varchar(250) NOT NULL,
	discharge_date date NULL,
	discharge_type_id varchar(4) NULL,
	discharge_type varchar(250) NULL,
	county_id int4 NOT NULL,
	county varchar(250) NULL,
	sub_county_id int4 NOT NULL,
	sub_county varchar(250) NULL,
	system_date date NULL,
	system_timestamp timestamptz NULL,
	is_void bool NOT NULL,
	case_id uuid NOT NULL,
	org_unit_id int4 NOT NULL,
	person_id int4 NOT NULL,
	CONSTRAINT rpt_inst_population_pkey PRIMARY KEY (id)
);
CREATE INDEX rpt_inst_population_658c6cff ON public.rpt_inst_population USING btree (org_unit_id);
CREATE INDEX rpt_inst_population_7f12ca67 ON public.rpt_inst_population USING btree (case_id);
CREATE INDEX rpt_inst_population_a8452ca7 ON public.rpt_inst_population USING btree (person_id);


-- public.rpt_inst_population foreign keys

ALTER TABLE public.rpt_inst_population ADD CONSTRAINT rpt_inst_pop_case_id_fa31113f2c89b9c_fk_ovc_case_record_case_id FOREIGN KEY (case_id) REFERENCES public.ovc_case_record(case_id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE public.rpt_inst_population ADD CONSTRAINT rpt_inst_populat_org_unit_id_dbe42566b1f70c3_fk_reg_org_unit_id FOREIGN KEY (org_unit_id) REFERENCES public.reg_org_unit(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE public.rpt_inst_population ADD CONSTRAINT rpt_inst_population_person_id_25d6541eb7cf1ba1_fk_reg_person_id FOREIGN KEY (person_id) REFERENCES public.reg_person(id) DEFERRABLE INITIALLY DEFERRED;