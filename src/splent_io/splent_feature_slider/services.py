from splent_io.splent_feature_slider.models import Slide
from splent_io.splent_feature_slider.repositories import SliderRepository
from splent_framework.db import db
from splent_framework.services.BaseService import BaseService


class SliderService(BaseService):
    """Homepage carousel slides, each backed by a media-library image."""

    def __init__(self):
        super().__init__(SliderRepository())

    def active_slides(self):
        """Active slides that still have an image, in display order."""
        slides = (
            Slide.query.filter_by(active=True)
            .order_by(Slide.order.asc(), Slide.id.asc())
            .all()
        )
        return [s for s in slides if s.media is not None]

    def all_slides(self):
        return Slide.query.order_by(Slide.order.asc(), Slide.id.asc()).all()

    def get(self, slide_id):
        return Slide.query.get(slide_id)

    def create(self, **data):
        slide = Slide(**data)
        db.session.add(slide)
        db.session.commit()
        return slide

    def update(self, slide, **data):
        for key, value in data.items():
            setattr(slide, key, value)
        db.session.commit()
        return slide

    def delete(self, slide):
        db.session.delete(slide)
        db.session.commit()
