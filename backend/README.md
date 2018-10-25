**COMMON RESULT FORMAT:**
```
{
    status: 0,
    data: ...
}
```
or
```
{
    status: 1,
    error: "error string"
}
```

**ENDPOINTS:**

**Register new user:**\
`POST /register`

- request parameters:\
`username: string`\
`password: string`

- response data:\
`-`

**Check user is registered:**\
`POST /register/check`

- request parameters:\
`username: string`\
`password: string`

- response data:\
`-`

**Create new event:**\
`POST /event/create`

- request parameters:\
`username: string`\
`password: string`\
`sport_id: int`\
`timestamp: int`\
`location: int`\
`description: string`\
`participants_number_max: int`\
`status_rating: bool`

- response data:\
`event_id: int`\
`usernames: [string] # список пользователей, подписанных на такие события` 

**Close event :**\
`POST /event/close`

- request parameters:\
`username: string`\
`password: string`\
`event_id: int`\
`event_status: 'Canceled'|'Closed'`\
`results: {username1: result1, ...}`

- response data:\
`-`

**Get event info :**\
`POST /event/get`

- request parameters:\
`event_id: int`

- response data:
```
event_info:
{
    sport_id: int
    timestamp: int
    location: int
    description: string
    participants_number_max: int
    status_rating: bool
    state_open: 'Open'|'Closed'|'Canceled'
}
```

**Get events list:**\
`POST /event/list`

- request parameters:\
`sports_id: int`

- response data:\
`event_ids: [int]`

**Join event :**\
`POST /event/join`

- request parameters:\
`username: string`\
`password: string`\
`event_id: int`

- response data:\
`-`

**Leave event:**\
`POST /event/leave`

- request parameters:\
`username: string`\
`password: string`\
`event_id: int`

- response data:\
`-`

**Get sports list:**\
`POST /sport/list`

- request parameters:\
`-`

- response data:
```
sportID:
{
    name: string
    description: string
},
...
```

**Get users list for sport_id:**\
`POST /user/list`

- request parameters:\
`sport_id: int`

- response data:\
`usernames: [string]`

**Get follows list:**\
`POST /follow/list`

- request parameters:\
`username: string`\
`password: string`

- response data:\
`follow_ids: [int]`

**Add follow:**\
`POST /follow/add`

- request parameters:\
`username: string`\
`password: string`\
`sport_id: int`\
`location: int`

- response data:\
`event_id: [int] # подходящие события со статусом 'Opened'`

**Remove follow:**\
`POST /follow/remove`

- request parameters:\
`username: string`\
`password: string`\
`follow_id: int`

- response data:\
`-`

**Get follow info:**\
`POST /follow/get`

- request parameters:\
`username: string`\
`password: string`\
`follow_id: int`

- response data:
```
follow_info:
{
    user_id: int
    sport_id: int
    location: int
}
```

**Get locations list:**\
`POST /location/list`

- request parameters:\
`-`

- response data:
```
locationID:
{
    name: string
    description: string
    longitude: string
    latitude: string
},
...
```

**Get suggested events for user:**\
`POST /event/user`

- request parameters:\
`username: string`

- response data:\
`event_ids: [int]`



**START:**
```
python3 -m venv venv

./venv/bin/activate

pip install Flask requests mysqlpy

python3 backend/backend_app.py
```


