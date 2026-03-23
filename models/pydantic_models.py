
from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import datetime
from typing import Optional, List, Dict
from constants.roles import Roles


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью "
                                                                              "совпадать с полем password")
    roles: list[Roles] = lambda: [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100,
                          description="Полное имя пользователя")
    verified: bool
    banned: Optional[bool] = None
    roles: list[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class Genre(BaseModel):
    id: Optional[int] = None
    name: str


class MovieSchema(BaseModel):

    id: int
    name: str = Field(..., min_length=1)
    price: int = Field(..., ge=0)
    description: Optional[str] = None
    imageUrl: Optional[HttpUrl] = None
    location: Optional[str] = None
    published: bool = False
    rating: Optional[float] = 0.0
    genreId: Optional[int] = None
    genre: Optional[Genre] = None
    createdAt: Optional[datetime] = None
    reviews: list[dict] = None

    @field_validator("createdAt", mode="before")
    def parse_created_at(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
