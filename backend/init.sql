-- Create tables
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(512),
    github_url VARCHAR(512),
    live_url VARCHAR(512),
    tech_stack JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    proficiency INT CHECK (proficiency BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL
);

-- Insert sample data
INSERT INTO projects (title, description, image_url, github_url, tech_stack) VALUES
('Personal Portfolio', 'A modern portfolio website built with React and Flask', '/images/portfolio.jpg', 'https://github.com/yourusername/portfolio', '["React", "TypeScript", "Flask", "MySQL", "Docker"]'),
('Project 2', 'Description for project 2', '/images/project2.jpg', 'https://github.com/yourusername/project2', '["Node.js", "Express", "MongoDB"]');

INSERT INTO skills (name, category, proficiency) VALUES
('React', 'Frontend', 5),
('TypeScript', 'Frontend', 4),
('Python', 'Backend', 5),
('Docker', 'DevOps', 4),
('MySQL', 'Database', 4);

-- Create default admin user (password: baseball)
INSERT INTO users (username, password_hash) VALUES
('jhyde01', 'scrypt:32768:8:1$7ZVCM9qdUYEDpY9M$8df41c74726379009001e092b8654b4d9c4c42d5a6c82f7e9fe7654a1d9e2c5c9b8e1d3a2f7c4b5e8d1a4f7c0b3e6d9');
