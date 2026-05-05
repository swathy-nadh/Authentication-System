from sqlalchemy.orm import  Mapped, mapped_column
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique= True, index=True)
    password: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"User(id = {self.id}, email = {self.email})"
