-- Ijazah Database and Student Records Schema
-- Version: 8.0.0
-- Domain: RELIGION::QEP

-- Students Table
CREATE TABLE qep_students (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    current_level INT DEFAULT 1,
    hifz_progress_juz INT DEFAULT 0,
    tajweed_score DECIMAL(5,2) DEFAULT 0.00,
    status VARCHAR(50) DEFAULT 'ACTIVE'
);

-- Teachers Table
CREATE TABLE qep_teachers (
    teacher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    certification_tier INT DEFAULT 1,
    years_of_experience INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    scholar_board_verified BOOLEAN DEFAULT FALSE
);

-- Ijazah Chains Table
CREATE TABLE qep_ijazah_chains (
    ijazah_id SERIAL PRIMARY KEY,
    teacher_id INT REFERENCES qep_teachers(teacher_id),
    sanad_chain TEXT NOT NULL,
    verified_by_scholar_board BOOLEAN DEFAULT FALSE,
    issue_date DATE,
    verification_date DATE
);

-- Student Achievements Table
CREATE TABLE qep_student_achievements (
    achievement_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES qep_students(student_id),
    tier INT,
    badge_name VARCHAR(100),
    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    certification_link TEXT
);

-- Lesson Attendance and Scores Table
CREATE TABLE qep_lesson_records (
    record_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES qep_students(student_id),
    level INT,
    lesson_number INT,
    score DECIMAL(5,2),
    attendance BOOLEAN DEFAULT TRUE,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexing for performance
CREATE INDEX idx_student_email ON qep_students(email);
CREATE INDEX idx_teacher_email ON qep_teachers(email);
CREATE INDEX idx_ijazah_teacher ON qep_ijazah_chains(teacher_id);
