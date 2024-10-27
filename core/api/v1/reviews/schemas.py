from datetime import datetime

from pydantic import BaseModel

from core.apps.products.entities.reviews import ProductReviewEntity as ReviewEntity


class ReviewInSchema(BaseModel):
    rating: int
    text: str

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            rating=self.rating,
            text=self.text,
        )


class CreateReviewSchema(BaseModel):
    product_id: int
    customer_token: int
    review: ReviewInSchema


class ReviewOutSchema(ReviewInSchema):
    id: int # noqa
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, entity: ReviewEntity) -> "ReviewOutSchema":
        return cls(
            id=entity.id,
            text=entity.text,
            rating=entity.rating,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
