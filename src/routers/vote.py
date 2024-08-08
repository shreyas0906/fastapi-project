from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Post id: {vote.post_id} is does not exist")


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"Post id: {vote.post_id} is already voted by user {current_user.id}")
    
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "voting done"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Vote deleted"}