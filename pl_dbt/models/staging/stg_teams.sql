with raw_data as (
    select payload, loaded_at
    from {{ source('raw', 'raw_teams') }}
),

flattened as (
    select
        t.value:id::int            as team_id,
        t.value:name::string       as team_name,
        t.value:shortName::string  as short_name,
        t.value:tla::string        as tla,
        t.value:crest::string      as crest_url,
        r.loaded_at
    from raw_data r,
         lateral flatten(input => r.payload:teams) t
)

select team_id, team_name, short_name, tla, crest_url
from flattened
qualify row_number() over (partition by team_id order by loaded_at desc) = 1