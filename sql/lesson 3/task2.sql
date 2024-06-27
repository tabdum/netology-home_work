SELECT trake_name FROM trake
WHERE duration = (SELECT MAX(duration) FROM trake);
SELECT trake_name FROM trake
WHERE duration >= 210;
SELECT collection_name FROM collection
WHERE 2018 <= year_of_issue AND year_of_issue <= 2020;
SELECT executor_name FROM executor
WHERE executor_name NOT LIKE '% %';
SELECT trake_name FROM trake
WHERE trake_name LIKE '%my' OR trake_name LIKE '%мой';

