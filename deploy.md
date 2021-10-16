ALTER ROLE octopus SET client_encoding TO 'utf8';
ALTER ROLE octopus SET default_transaction_isolation TO 'read committed';
ALTER ROLE octopus SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE kahraba_7000 TO octopus;
