CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('librarian', 'member')) NOT NULL
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    join_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    category VARCHAR(50),
    publication_year INT,
    copies_available INT DEFAULT 1 CHECK (copies_available >= 0)
);

CREATE TABLE book_authors (
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    author_id INT REFERENCES authors(author_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE,
    loan_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    CONSTRAINT check_return_after_loan CHECK (return_date IS NULL OR return_date >= loan_date)
);

CREATE TABLE book_clubs (
    club_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_by INT REFERENCES members(member_id),
    created_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE club_members (
    club_id INT REFERENCES book_clubs(club_id) ON DELETE CASCADE,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE,
    join_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (club_id, member_id)
);

CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_loans_member ON loans(member_id);
CREATE INDEX idx_loans_book ON loans(book_id);

INSERT INTO users (username, password_hash, role) VALUES 
('admin', 'admin123', 'librarian'),
('joker', 'manu123', 'member'),
('Z', 'z123', 'member'),
('Lady-in-red', 'obot123', 'member');

INSERT INTO members (user_id, full_name, email, phone) VALUES 
(1, 'Admin Librarian', 'admin@library.com', '079111111'),
(2, 'Manu Bejai-kumar', 'manubejaikumar@gmail.com', '034042455'),
(3, 'Miyubay Zawadi', 'Miyubayz@example.com', '030006208'),
(4, 'Michaella Obot', 'michaellaobot@gmail.com', '078042534');

INSERT INTO authors (name, bio) VALUES 
('J.K. Rowling', 'British author, best known for Harry Potter series'),
('Rick Riordan', 'American author, best known for Percy Jackson series'),
('Dan Brown', 'American author, best known for his thriller series'),
('Stephen King', 'American author, best known for his Horror novels'),
('J.R.R. Tolkien', 'British author,Author of The Lord of the Rings');

INSERT INTO books (title, isbn, category, publication_year, copies_available) VALUES 
('Harry Potter and the Philosopher''s Stone', '9780747532699', 'Fantasy', 1997, 3),
('The Hobbit', '9780261102217', 'Fantasy', 1937, 2),
('IT', '9780261102568', 'Horror', 1986, 1),
('Origin', '9780261092217', 'Thriller', 2017, 6),
('The last Olympian', '9780261102237', 'Fantasy-Adventure', 2009, 3);

INSERT INTO book_authors (book_id, author_id) VALUES (1, 1), (2, 4),(3,3),(4,2);

INSERT INTO book_clubs (name, description, created_by) VALUES 
('Fantasy Readers Club', 'Discussing epic fantasy books', 2),
('Horror Readers Club', 'Discussing Scary Horror books', 3),
('Romance Readers Club', 'Discussing spicy Romance books', 1);

INSERT INTO club_members (club_id, member_id) VALUES (1, 2), (1, 3),(2,2),(2,4),(3,4);

INSERT INTO loans (book_id, member_id, due_date) VALUES 
(1, 2, CURRENT_DATE + INTERVAL '7 days');

select * users;