WITH films_with_actors AS (
    SELECT
        f.film_id,
        f.title,
        STRING_AGG (a.actor_name, ',') AS film_actors
    FROM {{ref('films') }} f
    LEFT JOIN {{ ref('film_actors') }} fa ON f.film_id = fa.film_id
    LEFT JOIN {{ ref('actors') }} a ON fa.actor_id = a.actor_id
    GROUP BY f.film_id, f.title
)

SELECT
    fwf.*,
    fwa.actors
FROM films_with_ratings fwf
LEFT JOIN films_with_actors ON fwf.film_id = films_with_actors.film_id