CREATE TABLE samples
(
  id character varying(32) NOT NULL,
  f0 double precision,
  jitter double precision,
  f1 double precision,
  f2 double precision,
  f3 double precision,
  f1b double precision,
  shimmer double precision,
  intensity double precision,
  hnr double precision,
  speaker character varying(16),
  duration double precision,
  CONSTRAINT samples_pkey PRIMARY KEY (id),
  CONSTRAINT samples_speaker_fkey FOREIGN KEY (speaker)
      REFERENCES public.speakers (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)

CREATE TABLE speakers
(
  id character varying(16) NOT NULL,
  gender character varying(16),
  speaker_role character varying(1),
  CONSTRAINT speakers_pkey PRIMARY KEY (id)
)