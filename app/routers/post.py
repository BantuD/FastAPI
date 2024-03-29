from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from .. import database,models,schemas
from ..database import get_db
from typing import List,Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get('/',response_model=List[schemas.Post])
@router.get('/',response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db),user = Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0,search: Optional[str]=""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
    print(result)
    return result

@router.get('/{id}',response_model=schemas.PostWithVotes)
def getOnePost(id: int,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)):

    postQuery = db.query(models.Post).filter(models.Post.id == id)
    thepost = postQuery.first() #to fetch the first line only
    #print(thepost)

    if not thepost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} not found')
    
    # votes = db.query(models.Vote).filter(models.Vote.post_id == id).count()
    
    result = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    return result

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db),user = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user.id,**post.dict())  # convert Post class into table format
    # new_post = models.Post(              # alternative method
    #     id = post.id,
    #     title = post.title,
    #     content = post.content,
    #     published = post.published
    #     )
    #print(user.email)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post not found')
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not Authorized to perform this action')
    

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}',response_model=schemas.Post)
def update_post(id: int,new_post: schemas.UpdatePost,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)): #keep post name different than class Post 
    
 
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post not found')
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Unauthorized user')
    

    postQuery.update(new_post.dict(),synchronize_session=False)
    db.commit()
    print(postQuery.first())
    return postQuery.first()