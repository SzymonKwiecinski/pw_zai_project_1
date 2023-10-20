CREATE TABLE users
(
    id       SMALLSERIAL PRIMARY KEY,
    nick     VARCHAR(64)  NOT NULL,
    email    VARCHAR(64)  NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE icons
(
    id    SMALLSERIAL PRIMARY KEY,
    name  VARCHAR(64) NOT NULL,
    value TEXT        NOT NULL
);

CREATE TABLE categories
(
    id      SMALLSERIAL PRIMARY KEY,
    name    VARCHAR(32) NOT NULL,
    color   CHAR(7),
    icon_id SMALLINT REFERENCES icons (id) ON DELETE CASCADE,
    CONSTRAINT fk_icon FOREIGN KEY (icon_id) REFERENCES icons (id)
);

CREATE TABLE events
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(64) NOT NULL,
    description TEXT,
    graphic     VARCHAR(64),
    start_date  DATE        NOT NULL,
    end_date    DATE        NOT NULL,
    user_id     SMALLINT REFERENCES users (id) ON DELETE SET NULL,
    category_id SMALLINT REFERENCES categories (id) ON DELETE RESTRICT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories (id)
);
