from fastapi import APIRouter, status, Depends, HTTPException, Response, Body
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_302_FOUND, response_model=List[schemas.Post_Show])
async def posts_get(db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user), 
                    owner_id:int = 0, limit:int = 20, offset:int = 0, search:Optional[str] = ""):
        
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)

    if owner_id != 0:

        if search == "":
            posts = result.filter(models.Post.account_id == owner_id).limit(limit).offset(offset).all()
        else:
            posts = result.filter(models.Post.account_id == owner_id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    else:
        if search == "":
            posts = result.limit(limit).offset(offset).all()
        else:
            posts = result.filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return posts

@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.Post_Show)
async def post_get(id, db:Session = Depends(database.get_db), curr_acct = Depends(oauth2.get_current_user)):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    post = result.filter(models.Post.id == id).first()

    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id:{id}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def post_create(post: schemas.Post_Creation, db:Session = Depends(database.get_db), curr_acct = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump())
    new_post.account_id = curr_acct.id

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def post_update(
    id: int,
    post: schemas.Post_Creation = Body(...),  # Ensure post is an instance
    db: Session = Depends(database.get_db),
    curr_acct = Depends(oauth2.get_current_user)
):
    result = db.query(models.Post).filter(models.Post.id == id)
    post_old = result.first()

    if not post_old:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}"
        )
    
    elif curr_acct.id != post_old.account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
    
    # Update the fields of the existing post
    post_old.title = post.title
    post_old.content = post.content
    post_old.published = post.published  # Use the published field

    db.commit()  # Save changes
    return post_old  # Return the updated post

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def post_delete(id:int, db:Session = Depends(database.get_db), curr_acct = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no post with id:{id}"
            )
    elif curr_acct.id != post_query.first().account_id:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return{ "data":"Has been Deleted"}