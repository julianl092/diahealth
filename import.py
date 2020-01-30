from csv import DictReader
from app import db
from app.models import Tag, Link, ModifiedQuestion

with open('database.csv') as csv_file:
    csv_reader = DictReader(csv_file, delimiter=",")
    for row in csv_reader:
        c1 = db.session.query(Tag).filter_by(name=row['Category 1']).all()
        if not c1: 
            t1 = Tag(name=row['Category 1'])
            db.session.add(t1)
            db.session.commit()
        c2 = db.session.query(Tag).filter_by(name=row['Category 2']).all()
        if not c2: 
            t2 = Tag(name=row['Category 2'])
            db.session.add(t2)
            db.session.commit()
        q = ModifiedQuestion(question_text=row['Topic/Question'], type='modified', answer=row['Answer'], created_by=1)
        qtags = db.session.query(Tag).filter(Tag.name.in_([row['Category 1'], row['Category 2']])).all()
        q.tags = [qtag for qtag in qtags]  
        db.session.add(q)
        db.session.commit()