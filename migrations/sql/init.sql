CREATE SCHEMA bot;

CREATE TABLE bot."user" (
	id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	telegram_id int4 NOT NULL,
	"name" text NULL,
	email text NULL,
	CONSTRAINT user_pk PRIMARY KEY (id),
	CONSTRAINT user_unique UNIQUE (telegram_id)
);

CREATE TABLE bot.note (
	id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	user_id int4 NOT NULL,
	"text" text NULL,
	reminder_time timestamp NULL,
	notification_sent bool DEFAULT false NOT NULL,
	CONSTRAINT notes_pk PRIMARY KEY (id),
	CONSTRAINT notes_user_fk FOREIGN KEY (user_id) REFERENCES bot."user"(id)
);
