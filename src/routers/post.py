from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as response_status
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, oauth2
from ..database import get_db
from ..schemas import Post, PostCreate, PostOut, ResponseModel

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[Post]) 
@router.get("/") 
async def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=100,
    skip: int = 0, search: Optional[str] = ""
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id)).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(results)
    # for post in posts:
    # print(post)
    # print(dir(post))
    # print(post.keys())
    # print(post["title"])
    # return {"post": posts}
    return results


@router.post("/")
async def create_post(
    payload: PostCreate,
    status=response_status.HTTP_201_CREATED,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # print(payload.title)
    # print(payload.Content)
    # print(payload.Published)
    # print(f"rating: {payload.rating} type: {type(payload.rating)}")
    # dummy_data.append(payload.model_dump())
    # print(f"len of posts: {len(dummy_data)}")
    """
    For creating the post.
    1. Use the SQL command to insert a post,
    2. %s is used to denote the value in that position. This is used to eliminate SQL injection attacks.
    3. Once the query is executed, fetch the returning value.
    4. To save the changes on the DB use the connection.commit(), without which the changes aren't saved on the DB
    """
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published , rating) VALUES (%s, %s, %s, %s) RETURNING * """,
    #     (payload.title, payload.content, payload.published, payload.rating),
    # )

    # new_post = cursor.fetchone()

    # connection.commit()

    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.published)

    # print(current_user.email_id)

    owner_id = current_user.id

    # print(f"owner id: {owner_id}")

    # payload.update({"owner_id": owner_id})

    new_post = models.Post(
        owner_id=owner_id, **payload.model_dump()
    )  # you're creating the entry to be added to the DB. It's still not added to the DB.

    db.add(new_post)  # Now the entry is added to the DB.
    db.commit()  # Saved the changes to the DB
    db.refresh(new_post)  # Refresh so that the DB reflects the changes

    # return {"post": new_post}

    return new_post


@router.get("/{id}", response_model=Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # response : Response
    # for index, value in enumerate(dummy_data):
    #     print(type(dummy_data["id"]))
    #     if dummy_data["id"] == id:
    #         return {"post": dummy_data[index]}
    #     # response.status_code = status.HTTP_404_NOT_FOUND

    # raise HTTPException(
    #     status_code=response_status.HTTP_404_NOT_FOUND, detail="post not found"
    # )
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))

    # fetched_post = cursor.fetchone()
    """
    First, select the table to find the post --> models.Post
    filter the post we are looking for --> models.Post.id == id
    return the first post we find ---> first()
    If first is not used, sqlalcehmy will keep looking to find any other entry which has the same id and throw error
    """

    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if fetched_post is None:
        raise HTTPException(
            status_code=response_status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    # return {"post": fetched_post}
    return fetched_post


@router.delete("/{id}")
def delete_post_by_id(
    id: int,
    status=response_status.HTTP_204_NO_CONTENT,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # seen_ids = []

    # if len(dummy_data) == 0:
    #     raise HTTPException(
    #         status_code=response_status.HTTP_404_NOT_FOUND, detail="empty list"
    #     )

    # for index, value in enumerate(dummy_data):
    #     seen_ids.append(index)

    #     if value["id"] == id:
    #         del dummy_data[index]
    #         return {"post": f"post with {id} id deleted"}

    # if id not in seen_ids:
    #     raise HTTPException(
    #         status_code=response_status.HTTP_404_NOT_FOUND, detail="post not found"
    #     )
    """
    For deleting a post by id
    1. Execute the SQL command
    2. fetch the deleted row.
    3. Commit it to the DB.
    4. Raise exception is the fetched result is None.
    5. [Optional] To return the deleted post.
    """

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()

    # connection.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(
            status_code=response_status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    elif current_user.id != deleted_post.first().owner_id:
        raise HTTPException(
            status_code=response_status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit()

    return {"data": deleted_post}
    # return deleted_post


@router.put("/{id}", status_code=response_status.HTTP_200_OK)
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # all_ids = []

    # for existing_post in dummy_data:
    #     all_ids.append(existing_post["id"])

    #     if existing_post["id"] == id:
    #         existing_post["title"] = post.title
    #         existing_post["content"] = post.content

    # if id not in all_ids:
    #     raise HTTPException(
    #         status_code=response_status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id {id} not found",
    #     )

    # return {"post": f"post with {id} updated"}
    """
    For updating the post by ID
    1. Execute the SQL command to first find the post by id and update only the required columns
    2. Fetch the updated row.
    3. If the updated row is not None, commit to the DB else raise exception.
    4. [Optional] to return the updated post.
    """

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )

    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_to_update = post_query.first()

    print(f"post to update: {post_to_update.owner_id}")
    print(f"current user: {current_user.id}")

    if post_to_update is None:
        raise HTTPException(
            status_code=response_status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    elif post_to_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=response_status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorized to update post",
        )
    else:
        post_query.update(post.model_dump(), synchronize_session=False)
        # post_to_update.update(post.model_dump(), synchronize_session=False)
        db.commit()
        # return {"data": post_query.first()}
        return post_query.first()
