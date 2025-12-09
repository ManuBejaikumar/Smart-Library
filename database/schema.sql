CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('librarian','member'))
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    category VARCHAR(50),
    copies_available INT DEFAULT 1
);

CREATE TABLE book_authors (
    book_id INT REFERENCES books(book_id),
    author_id INT REFERENCES authors(author_id),
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(book_id),
    member_id INT REFERENCES members(member_id),
    loan_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    return_date DATE NULL
);

CREATE TABLE book_clubs (
    club_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

CREATE TABLE club_members (
    club_id INT REFERENCES book_clubs(club_id),
    member_id INT REFERENCES members(member_id),
    PRIMARY KEY (club_id, member_id)
);