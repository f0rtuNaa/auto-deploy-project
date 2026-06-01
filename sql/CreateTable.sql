-- public.sales определение

-- Drop table

-- DROP TABLE public.sales;

CREATE TABLE public.sales (
	doc_id varchar NULL,
	item varchar NULL,
	category varchar NULL,
	amount int4 NULL,
	price numeric NULL,
	discount numeric NULL,
	shop varchar NULL,
	cash varchar NULL,
	id serial4 NOT NULL,
	CONSTRAINT sales_pk PRIMARY KEY (id)
);