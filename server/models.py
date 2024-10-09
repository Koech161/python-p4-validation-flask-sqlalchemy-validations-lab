from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
   
        
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author name must not be empty.')
        existing_name = Author.query.filter_by(name=name).first()
        if existing_name:
            raise ValueError('Author already exist')
        return name
   
    @validates('phone_number')
    def validate_number(self,key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be 10 charachters long.')
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

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250 :
            raise ValueError('Content is too short.')
        
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary is too long')
        return summary
    @validates('category')
    def validat_categrory(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category
    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError('Title must contain at least one clickbait keyword: "Won\'t Believe", "Secret", "Top", or "Guess".')
        return title 
    
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
