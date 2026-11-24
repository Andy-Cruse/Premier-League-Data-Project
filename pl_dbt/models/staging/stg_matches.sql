with raw_data as (
    select payload, loaded_at
    from {{ source('raw', 'raw_matches') }}
),

flattened as (
    select
        m.value:id::int                      as match_id,
        m.value:utcDate::timestamp_ntz       as kickoff_utc,
        m.value:status::string               as status,
        m.value:matchday::int                as matchday,
        m.value:homeTeam:id::int             as home_team_id,
        m.value:awayTeam:id::int             as away_team_id,
        m.value:score:fullTime:home::int     as home_goals,
        m.value:score:fullTime:away::int     as away_goals,
        r.loaded_at
    from raw_data r,
         lateral flatten(input => r.payload:matches) m
),

latest as (
    select *
    from flattened
    qualify row_number() over (partition by match_id order by loaded_at desc) = 1
)

select
    match_id,
    kickoff_utc,
    matchday,
    home_team_id,
    away_team_id,
    home_goals,
    away_goals,
    case
        when home_goals > away_goals then 'HOME_WIN'
        when home_goals < away_goals then 'AWAY_WIN'
        else 'DRAW'
    end as result
from latest
where status = 'FINISHED'