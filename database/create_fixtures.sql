CREATE TABLE IF NOT EXISTS hashtags_table (
    id SERIAL PRIMARY KEY , 
    hashtag_text varchar(128), 
    count int
);

CREATE TABLE IF NOT EXISTS unigrams_table (
    id SERIAL PRIMARY KEY , 
    unigram_text varchar(128), 
    count int
);