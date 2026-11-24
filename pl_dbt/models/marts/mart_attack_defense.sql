with team as (
    select
        team_id,
        team_name,
        count(*)           as games,
        avg(goals_for)     as goals_for_per_game,
        avg(goals_against) as goals_against_per_game
    from {{ ref('fct_team_match') }}
    group by 1, 2
),

league as (
    select avg(goals_for) as league_avg_goals
    from {{ ref('fct_team_match') }}
)

select
    t.*,
    l.league_avg_goals,
    t.goals_for_per_game - l.league_avg_goals     as attack_vs_league,
    l.league_avg_goals - t.goals_against_per_game as defense_vs_league
from team t
cross join league l