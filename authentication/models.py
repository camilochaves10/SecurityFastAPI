class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(1024), index= True, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_colum(String(1024), nullable=False)
    