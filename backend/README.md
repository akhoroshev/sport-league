Environment setup:

    python3 -m venv venv
     
    . venv/bin/activate
    pip install Flask
    pip install requests
    pip install pylint
    pip install mysqlpy
    

REST API description here

1. common result format:

    result: {
                status: 0
                data: ...
            }

or

    result: {
              status: 1
              error: "error description"
            }

2. data format:


        /register:
            params: {   
                        username: ...
                        password: ...
                    }
            data:   {
                    }

        /event/create:
            params: {
                        username: ...
                        password: ...
                        sport_id: ...
                        timestamp: ...
                        location: ...
                        description: ...
                        size: ...
                    }
            data:   {   
                        event_id: ...
                    }

        /event/close:
            params: {
                        username: ...
                        password: ...
                        event_id: ...
                        event_status: ... ("CANCEL", "COMPLETE")
                        results: {
                            username1: result1,
                            username2: result2
                        }
                    }
            data:   {
                    }

        /event/get:
            params: {
                        event_id: ...
                    }
            data:   {
                        event_info: {
                            sport_id: ...
                            timestamp: ...
                            location: ...
                            description: ...
                            size: ...
                        }

                        participants: [...]
                    }

        /event/list:
            params: {
                        sport_id: ...
                    }
            data:   {
                        event_ids: [...]
                    }

        /event/join:
            params: {
                        username: ...
                        password: ...
                        event_id: ...
                    }
            data:   {
                    }

        /event/leave:
            params: {
                        username: ...
                        password: ...
                        event_id: ...
                    }
            data:   {
                    }

        /rating/global:
            params: {
                        sport_id: ...
                    }
            data:   {
                        usernameI: ratingI
                        ...
                    }

        /rating/local:
            params: {
                        sport_id: ...
                        usernames: [...]
                    }
            data:   {
                        usernameI: ratingI
                        ...
                    }

        /sport/list:
            params: None
            data:   {
                        sport_idI:  {
                                        name: ...
                                        description: ...
                                    }
                    }

        /user/list:
            params: {
                        sport_id: ...
                    }
            data:   {
                        usernames: [...]
                    }

        /follow/list:
            params: None
            data:   {
                        event_ids: [...]
                    }

        /follow/add:
            params: {
                        sport_id: ...
                        location: ...
                    }
            data:   {
                    }

        /follow/remove:
            params: {
                        sport_id: ...
                    }
            data:   {
                    }

