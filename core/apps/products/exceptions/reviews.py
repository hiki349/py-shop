from dataclasses import dataclass


@dataclass(eq=False)
class ReviewInvalidRating(BaseException):
    rating: int

    @property
    def message(self):
        return 'Rating is not valid.'
