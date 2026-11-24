with running as (
    select
        team_id, team_name, game_number, kickoff_utc, points, goals_for, goals_against,
        sum(points) over (
            partition by team_id order by game_number
            rows between unbounded preceding and current row) as cum_points,
        sum(goal_diff) over (
            partition by team_id order by game_number
            rows between unbounded preceding and current row) as cum_gd,
        sum(goals_for) over (
            partition by team_id order by game_number
            rows between unbounded preceding and current row) as cum_gf,
        sum(points) over (
            partition by team_id order by game_number
            rows between 4 preceding and current row) as form_points_last5
    from {{ ref('fct_team_match') }}
)

select
    *,
    rank() over (
        partition by game_number
        order by cum_points desc, cum_gd desc, cum_gf desc
    ) as league_position
from running