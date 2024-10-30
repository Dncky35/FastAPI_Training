import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_account):
    vote = models.Vote(post_id = test_posts[3].id, account_id = test_account['id'] )
    session.add(vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[2].id, "dir":1})
    
    assert res.status_code == 202

def test_vote_on_posts_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir":1})

    assert res.status_code == 409

def test_vote_detele(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir":0})

    assert res.status_code == 202

def test_vote_detele_not_exist(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir":0})

    assert res.status_code == 409

def test_delete_vote_non_exist(authorized_client):
    res = authorized_client.post("/votes/", json = {"post_id": "4568", "dir":0})
    assert res.status_code == 404

def test_vote_unauthorized_client(client, test_posts):
    res = client.post("/votes/", json={"post_id": test_posts[3].id, "dir":"1"})

    assert res.status_code == 401