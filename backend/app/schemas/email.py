from pydantic import BaseModel, EmailStr


class EmailData(BaseModel):

    sender: EmailStr

    subject: str

    body: str