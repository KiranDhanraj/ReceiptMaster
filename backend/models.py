from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base
from datetime import datetime
Base = declarative_base()
# Defines the User model, which contains user information like email and password
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


# Defines the Reciept model, which contains information about the reciept such as the user who uploaded it, the OCR text, and the date it was created
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ocr_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
# Defines the ReceiptItem model, which contains information about the individual items on the reciept such as the barcode, category, brand, and description
class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True)

    receipt_id = Column(
        Integer,
        ForeignKey("receipts.id")
    )
    
    barcode = Column(String)

    category = Column(String)

    brand = Column(String)

    description = Column(String)

    price = Column(Numeric(10, 2))
    
    name = Column(String)
