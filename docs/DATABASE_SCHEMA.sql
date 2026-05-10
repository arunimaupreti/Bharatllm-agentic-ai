CREATE TABLE scholarships (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    benefits TEXT,
    official_link TEXT,
    min_income INTEGER DEFAULT 0,
    max_income INTEGER DEFAULT 0,
    required_education TEXT DEFAULT 'Any',
    min_marks INTEGER DEFAULT 0,
    eligible_states TEXT[] DEFAULT ARRAY['All India'],
    gender TEXT DEFAULT 'Any',
    categories TEXT[] DEFAULT ARRAY['All'],
    deadline DATE,
    course_type TEXT DEFAULT 'Any',
    institute_type TEXT DEFAULT 'Any',
    nationality TEXT DEFAULT 'Indian',
    min_age INTEGER DEFAULT 0,
    max_age INTEGER DEFAULT 0,
    embedding VECTOR,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_scholarships_required_education ON scholarships(required_education);
CREATE INDEX idx_scholarships_deadline ON scholarships(deadline);
CREATE INDEX idx_scholarships_states ON scholarships USING GIN(eligible_states);
CREATE INDEX idx_scholarships_categories ON scholarships USING GIN(categories);
