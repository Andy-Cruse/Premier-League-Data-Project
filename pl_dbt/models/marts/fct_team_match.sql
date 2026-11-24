with matches as (
    select * from {{ ref('stg_matches') }}
),

home as (
    select
        match_id, kickoff_utc, matchday,
        home_team_id as team_id,
        away_team_id as opponent_id,
        true         as is_home,
        home_goals   as goals_for,
        away_goals   as goals_against
    from matches
),

away as (
    select
        match_id, kickoff_utc, matchday,
        away_team_id as team_id,
        home_team_id as opponent_id,
        false        as is_home,
        away_goals   as goals_for,
        home_goals   as goals_against
    from matches
),

unioned as (
    select * from home
    union all
    select * from away
)

select
    u.match_id,
    u.kickoff_utc,
    u.matchday,
    u.team_id,
    t.team_name,
    u.opponent_id,
    u.is_home,
    u.goals_for,
    u.goals_against,
    u.goals_for - u.goals_against as goal_diff,
    case
        when u.goals_for > u.goals_against then 'W'
        when u.goals_for = u.goals_against then 'D'
        else 'L'
    end as outcome,
    case
        when u.goals_for > u.goals_against then 3
        when u.goals_for = u.goals_against then 1
        else 0
    end as points,
    row_number() over (partition by u.team_id order by u.kickoff_utc) as game_number
from unioned u
join {{ ref('stg_teams') }} t on t.team_id = u.team_id