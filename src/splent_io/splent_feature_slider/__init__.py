from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service, service_proxy

from splent_io.splent_feature_slider.services import SliderService

slider_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.assets.asset_registry import register_asset
    from splent_framework.settings.settings_schema import register_settings

    register_service(app, "SliderService", SliderService)
    register_asset(
        "css", "slider.assets", order=100, subfolder="css", filename="slider.css"
    )
    register_asset(
        "js", "slider.assets", order=100, subfolder="js", filename="slider.js"
    )
    # Admin-configurable behaviour (declared once; the framework renders the
    # panel and persists the values). No ad-hoc config module.
    register_settings(
        "slider",
        "Slider",
        [
            {
                "key": "scope",
                "type": "select",
                "default": "home",
                "label": "Show on",
                "options": [("home", "Home page only"), ("all", "All pages")],
                "help": "Where the carousel appears.",
            },
            {"key": "autoplay", "type": "bool", "default": "1", "label": "Autoplay"},
            {
                "key": "interval",
                "type": "int",
                "default": "6",
                "label": "Interval (seconds)",
            },
            {
                "key": "overlay",
                "type": "bool",
                "default": "1",
                "label": "Shade the bottom half",
                "help": "Darkens the lower half so the white caption stays legible.",
            },
            {
                "key": "caption_color",
                "type": "color",
                "default": "#ffffff",
                "label": "Caption colour",
            },
        ],
        icon="image",
    )


def inject_context_vars(app):
    # Expose the active slides so the carousel (rendered via the layout.hero
    # hook) can pick them up. Safe if the service is somehow unavailable.
    def slider_items():
        try:
            return service_proxy("SliderService").active_slides()
        except Exception:
            return []

    return {"slider_items": slider_items}
