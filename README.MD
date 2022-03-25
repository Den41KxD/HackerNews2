Get:
http://127.0.0.1:8000/api/user/ 
http://127.0.0.1:8000/api/post/
http://127.0.0.1:8000/api/comment/


POST:
http://127.0.0.1:8000/api/user/
{
        "username": "username",
        "password": "password"
    }


http://127.0.0.1:8000/api-token-auth/
{
        "username": "username",
        "password": "password"
    }

http://127.0.0.1:8000/api/post/
{
        "title": "title",
        "link": "link"
    }

http://127.0.0.1:8000/api/comment/
{
        "text": "text",
        "Post_id": Post_id
    }

http://127.0.0.1:8000/api/post/number_of_post/upvote/