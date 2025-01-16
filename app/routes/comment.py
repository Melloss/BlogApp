from fastapi import APIRouter,Path,HTTPException
from pydantic import BaseModel,Field
from datetime import datetime
from ..models import Comment,Blog
from ..utils.dependencies import user_dependency,db_dependency

router = APIRouter()

class CommentRequest(BaseModel):
    content : str = Field(min_length=1)
    
class CommentResponse(BaseModel):
    id : int
    content :str 
    updated_date: datetime
    author_id: int
    blog_id: int
    
    

@router.post('/{blog_id}',status_code=201)
def post_comment(db:db_dependency,user:user_dependency,comment: CommentRequest,blog_id:int = Path(gt=0)) -> CommentResponse:
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog:
        comment = Comment(
                **comment.model_dump(),
                author_id = user.get('id'),
                blog_id = blog.id,
                user_id = blog.author_id
            )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    raise HTTPException(detail="Blog not found",status_code=404)

        
@router.get('/{blog_id}')
def get_comments(db:db_dependency,user: user_dependency,blog_id: int = Path(gt=0)) -> list[CommentResponse]:
    comments = db.query(Comment).filter(Comment.blog_id == blog_id ).all()
    return comments

@router.delete('/{blog_id}/{comment_id}')
def delete_comment(db: db_dependency,user: user_dependency,blog_id: int = Path(gt=0),comment_id:int = Path(gt=0)):
    comment = db.query(Comment).filter(Comment.blog_id == blog_id and Comment.id == comment_id).first()
    if comment:
        if user.get("id") == comment.author_id:
            db.delete(comment)
            db.commit()
            return {"success": "Comment deleted"}
        raise HTTPException("You don't have access to delte this comment")
    raise HTTPException(detail="Blog not found!",status_code=404)
