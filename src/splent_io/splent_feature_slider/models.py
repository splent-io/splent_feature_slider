from splent_framework.db import db


class Slide(db.Model):
    """One slide in the homepage carousel.

    The image lives in the media library (``media_id`` -> MediaItem); the slider
    only REFERENCES it, so images are uploaded and managed in /admin/media.
    ON DELETE SET NULL means deleting a media item leaves the slide intact but
    image-less, and the render simply skips slides without an image.
    """

    __tablename__ = "slide"

    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(
        db.Integer,
        db.ForeignKey("media_item.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title = db.Column(db.String(255), default="")
    caption = db.Column(db.Text, default="")
    link = db.Column(db.String(512), default="")
    order = db.Column(db.Integer, default=0, index=True)
    active = db.Column(db.Boolean, default=True, index=True)

    media = db.relationship("MediaItem", lazy="joined")

    @property
    def image_url(self):
        return self.media.url if self.media else ""

    def __repr__(self):
        return f"Slide<{self.id}>"
