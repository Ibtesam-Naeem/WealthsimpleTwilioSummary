from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql://wealthuser:ahmadahmad123@localhost/wealthsimple"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Portfolio(Base):
    """
    Represents the portfolio table in the database and
    stores the total portfolio value and the timestamp of entry.
    """
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total_value = Column(Float, nullable=False)

class Holdings(Base):
    """
    Represents the holdings table in the database.
    stores stock details like stock symbol, total value, shares owned,
    price per share, and all-time return.
    """
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, nullable=False)  
    stock_symbol = Column(String, nullable=False)
    total_value = Column(Float, nullable=False)
    shares_owned = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    all_time_return = Column(Float, nullable=False)

def init_db():
    """
    Initializes the database by creating all defined tables.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Provides a database session and ensures the session is
    properly closed after usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_portfolio(total_value):
    """
    Inserts a new portfolio entry into the database.
    """
    db = SessionLocal()
    new_portfolio = Portfolio(total_value=total_value)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    db.close()
    return new_portfolio.id

def insert_holding(portfolio_id, stock_symbol, total_value, shares_owned, price_per_share, all_time_return):
    """
    Inserts a new stock holding entry into the database.
    """
    db = SessionLocal()
    new_holding = Holdings( 
        portfolio_id=portfolio_id,
        stock_symbol=stock_symbol,
        total_value=total_value,
        shares_owned=shares_owned,
        price_per_share=price_per_share,
        all_time_return=all_time_return
    )
    db.add(new_holding)
    db.commit()
    db.close()