CREATE TABLE "user"
(
    id       SMALLSERIAL PRIMARY KEY,
    email    VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(128)        NOT NULL
);

CREATE TABLE category
(
    id       SMALLSERIAL PRIMARY KEY,
    name     VARCHAR(32) UNIQUE NOT NULL,
    color    VARCHAR(7)         NOT NULL,
    icon_svg VARCHAR(64)        NOT NULL
);

CREATE TABLE event
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(64) NOT NULL,
    description TEXT,
    graphic     VARCHAR(64),
    start_date  DATE        NOT NULL,
    end_date    DATE        NOT NULL,
    category_id SMALLINT REFERENCES category (id) ON DELETE RESTRICT,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES category (id),
    CHECK ( start_date <= end_date )
);
