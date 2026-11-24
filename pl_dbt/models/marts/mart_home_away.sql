select
    team_id,
    team_name,
    is_home,
    count(*)                         as games,
    sum(points)                      as points,
    round(avg(points), 2)            as points_per_game,
    sum(goals_for)                   as goals_for,
    sum(goals_against)               as goals_against,
    sum(goal_diff)                   as goal_diff
from {{ ref('fct_team_match') }}
group by 1, 2, 3