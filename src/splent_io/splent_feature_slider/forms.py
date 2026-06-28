from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureSliderForm(FlaskForm):
    submit = SubmitField("Save splent_feature_slider")
