from fastapi import APIRouter,Path,HTTPException
from pydantic import BaseModel
from datetime import datetime
from ..models import Blog,Comment,User
from . import comment

from ..utils.dependencies import db_dependency,user_dependency

router = APIRouter()

class BlogRequest(BaseModel):
    title: str
    content: str
    image :str


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    image : str
    author_id : int
    created_date : datetime
    updated_date : datetime
    
router.include_router(comment.router,prefix='/comment',tags=['Comment'])


@router.post('/publish-post',status_code=201)
def publish_post(blog: BlogRequest,db : db_dependency,user: user_dependency) -> BlogResponse:
    new_blog = Blog(**blog.model_dump(),author_id=user.get('id'))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/all')
def get_all_blogs(db:db_dependency,user:user_dependency,skip:int = 0, limit : int =10) -> list[BlogResponse]:
    blogs = db.query(Blog).offset(skip).limit(limit).all()
    return blogs

@router.get('/my')
def get_my_blogs(db:db_dependency,user:user_dependency,skip:int = 0, limit : int =10) -> list[BlogResponse]:
    blogs = db.query(Blog).filter(Blog.author_id == user.get('id')).offset(skip).limit(limit).all()
    return blogs

@router.put('/my/{blog_id}')
def update_my_blog(db:db_dependency,user:user_dependency,blog_request: BlogRequest,blog_id: int = Path(gt=0)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog:
        if blog.author_id == user.get("id"):
            blog.title = blog_request.title
            blog.content = blog_request.content
            blog.image = blog_request.image
            db.commit()
            db.refresh(blog)
            return blog
        else :
            raise HTTPException(detail="You don't have access to update this blog",status_code=400)
    raise HTTPException(detail="Blog not found",status_code=404)
        

@router.delete("/my/{blog_id}",status_code=200)
def delete_my_blog(db:db_dependency,user:user_dependency,blog_id:int = Path(gt=0)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog:
        if blog.author_id == user.get("id"):
            db.delete(blog)
            db.commit()  
            return {"success":"blog deleted"}
        else :
            raise HTTPException(detail="You don't have access to delete this blog",status_code=400)
    raise HTTPException(detail="Blog not found",status_code=404)

    