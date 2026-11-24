select match_id, count(*) as row_count
from {{ ref('fct_team_match') }}
group by 1
having count(*) <> 2