import sqlite3

conn = sqlite3.connect("assessment.db")

cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE student_submissions (
    student_id TEXT,
    question_id TEXT,
    selected_option TEXT,
    is_correct INTEGER
);

CREATE TABLE question_bank (
    question_id TEXT,
    topic TEXT,
    correct_option TEXT
);

INSERT INTO question_bank VALUES
('Q001','Python','A'),
('Q002','SQL','C'),
('Q003','Data Structures','C'),
('Q004','DBMS','B'),
('Q005','Aptitude','D');

INSERT INTO student_submissions VALUES
('S001','Q001','A',1),
('S001','Q002','B',0),
('S001','Q003','C',1),
('S002','Q001','A',1),
('S002','Q002','C',1),
('S002','Q003','D',0),
('S003','Q001','B',0),
('S003','Q002','C',1),
('S003','Q003','C',1),
('S004','Q001','A',1),
('S004','Q002','B',0),
('S004','Q003','C',1);
""")

conn.commit()
conn.close()

print("assessment.db created successfully")
