{% set film_title = 'Dunkirk' %} --  set is what allow us to setup controls i.e. gingas

SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'