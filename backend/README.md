REST API description here

    register:
        params: {   
                    username: ...
                    password: ...
                }
        result: {
                    status_code: ...
                }

    create event:
        params: {
                    sport_id: ...
                    timestamp: ...
                    location: ...
                    description: ...
                    players: ...
                }
        result: {   
                    event_id: ...
                    status_code: ... 
                }

    close event:
        params: {
                    event_id: ...
                    status_code: ... ("CANCEL", "COMPLETE")
                }
        result: {
                    status_code: ...
                }

    get event:
        params: {
                    event_id: ...
                }
        result: {
                    sport_id: ...
                    timestamp: ...
                    location: ...
                    description: ...
                    players: ...
                    usernames: [...]
                }

    list events:
        params: None
        result: {
                    event_ids: [...]
                }

    join event:
        params: {
                    event_id: ...
                }
        result: {
                    status_code: ...
                }

    leave event:
        params: {
                    event_id: ...
                }
        result: {
                    status_code: ...
                }

    global rating:
        params: {
                    sport_id: ...
                }
        result: {
                    usernameI: ratingI
                    ...
                }

    local rating:
        params: {
                    sport_id: ...
                    usernames: [...]
                }
        result: {
                    usernameI: ratingI
                    ...
                }

    list sports:
        params: None
        result: {
                    sport_idI:  {
                                    name: ...
                                    description: ...
                                }
                }

    list sportsmen:
        params: {
                    sport_id: ...
                }
        result: {
                    usernames: [...]
                }

    list followed events:
        params: None
        result: {
                    event_ids: [...]
                }

    follow event:
        params: {
                    sport_id: ...
                    location: ...
                    radius: ...
                }
        result: {
                    status_code: ...
                }

    unfollow event:
        params: {
                    sport_id: ...
                }
        result: {
                    status_code: ...
                }

