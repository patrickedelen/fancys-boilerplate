# from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime

# Base = declarative_base()

# class TaskResult(Base):
#     __tablename__ = 'task_results'
#     id = Column(String, primary_key=True, index=True)
#     status = Column(String, index=True)
#     result = Column(Text)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_done = Column(DateTime, default=datetime.utcnow)

# # Replace with your actual database URL
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)
