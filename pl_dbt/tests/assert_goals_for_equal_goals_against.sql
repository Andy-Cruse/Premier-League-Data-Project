select *
from (
    select sum(goals_for) as gf, sum(goals_against) as ga
    from {{ ref('fct_team_match') }}
)
where gf <> ga