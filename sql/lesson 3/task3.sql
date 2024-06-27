SELECT genre_name, COUNT(*)  
FROM genre_executor
JOIN genre ON genre_executor.genre_id = genre.genre_id
GROUP BY genre_name
ORDER BY genre_name ASC;

SELECT COUNT(*)
FROM trake
JOIN albom ON fk_albom_id = albom_id
WHERE year_of_issue BETWEEN 2019 AND 2020;

SELECT albom_name, AVG(duration)
FROM trake
JOIN albom ON fk_albom_id = albom_id
GROUP BY albom_name;

SELECT executor_name FROM executor
	WHERE executor_name NOT IN (
		SELECT DISTINCT executor_name FROM executor e
		LEFT JOIN albom_executor ae ON e.executor_id = ae.executor_id
		LEFT JOIN albom al ON ae.albom_id = al.albom_id
		WHERE al.year_of_issue = 2020
		)
	ORDER BY executor_name

SELECT DISTINCT(collection_name)
FROM collection cn
JOIN collection_trake ct ON cn.collection_id = ct.collection_id
JOIN trake ON ct.trake_id = trake.trake_id
JOIN albom_executor ax ON trake.fk_albom_id = ax.albom_id
JOIN executor ex ON ax.executor_id = ex.executor_id
WHERE executor_name = 'executor 1'
ORDER BY collection_name;
