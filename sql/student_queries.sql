SELECT AVG(Math) AvgMath
FROM students;

SELECT AVG(Science) AvgScience
FROM students;

SELECT AVG(English) AvgEnglish
FROM students;

SELECT Name,
(Math+Science+English)/3 AS AverageMarks
FROM students
ORDER BY AverageMarks DESC;

SELECT MAX(Math) TopMathScore
FROM students;

SELECT MAX(Science) TopScienceScore
FROM students;

SELECT MAX(English) TopEnglishScore
FROM students;