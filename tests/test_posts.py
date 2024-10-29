import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    # def validate_post(post):
    #     return schemas.Post_Show(**post)
    
    # posts_map = map(validate_post, res.json())
    # print(list(posts_map))
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_get_a_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post_Show(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id

def test_create_a_post(authorized_client, test_account):
    post_data = {
        "title": "first title",
        "content": "first content",
        "account_id": test_account['id']
    }

    res = authorized_client.post("/posts/", json=post_data)
    post_test = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post_test.published == True 
    assert post_test.owner.id == test_account['id']

def test_create_a_post_published_false(authorized_client, test_account):
    post_data = {
        "title": "first title",
        "content": "first content",
        "published": False,
    }

    res = authorized_client.post("/posts/", json=post_data)
    post_test = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post_test.published == False 
    assert post_test.owner.id == test_account['id']

def test_delete_a_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 200
    assert res.json() == { "data":"Has been Deleted" }

def test_update_a_post(authorized_client, test_account, test_posts):
    post_data = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    post_test = schemas.Post(**res.json())

    assert res.status_code == 200
    assert post_test.published == False 
    assert post_test.title == post_data['title']
    assert post_test.content == post_data['content']

def test_unauthorized_account_get_all_posts(client):
    res = client.get("/posts/")

    assert res.status_code == 401

def test_get_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/9999")

    assert res.status_code == 404

def test_unauthorized_account_delete_posts(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_post_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/9999")

    assert res.status_code == 404

def test_delete_other_account_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 401
    assert res.json().get("detail") == "UNAUTHORIZED"

def test_unauthorized_account_update_posts(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_update_not_exist_post(authorized_client, test_posts):
    post_data = {
        "title": "first title",
        "content": "first content",
        "published": False,
    }

    res = authorized_client.put(f"/posts/9999", json=post_data)
    
    assert res.status_code == 404

def test_update_other_accounts_post(authorized_client, test_posts, test_account):
    post_data = {
        "title": "first title",
        "content": "first content",
        "published": False,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post_data)
    
    assert res.status_code == 401
    assert res.json().get("detail") == "UNAUTHORIZED"


    

    