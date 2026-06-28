from splent_io.splent_feature_slider.models import Slide
from splent_framework.repositories.BaseRepository import BaseRepository


class SliderRepository(BaseRepository):
    def __init__(self):
        super().__init__(Slide)
