from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Author name required")
        if Author.query.filter(db.func.lower(Author.name) == name.lower()).first():
            raise ValueError("Author name already Exist")
        return name
    
    @validates('phone_number')

    def validates_phoneNumber(self,key,phone_number):
        if phone_number and (len(phone_number) != 10 or not phone_number.isdigit()):
            raise ValueError("Phone number not valid")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self,key,title):
        if not title:
            raise ValueError('Title required')
        clickbait_phrases = ["Won't Believe", "Secret", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must be clickbait-y')
        return title
    @validates('posts')
    def validates_post(self,key,posts):
        if posts and len(posts) < 250:
            raise ValueError("post must be 250 characters long")
        return posts
    @validates('summary')
    def validates_summary(self,key,summary):
        if summary and len(summary) > 250:
            raise ValueError ("post must not exceed 250 characters")
        return summary
    @validates(category)
    def validates_category(self,key,category):
        if category not in("Fiction", "Non-Fictional"):
            raise ValueError("post must be in Fictional or Non-Fictional")
        return category
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
