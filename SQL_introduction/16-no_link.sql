-- list rows with name
-- score desc
SELECT score, name
FROM second_table
WHERE name IS NOT NULL
ORDER BY score DESC;
