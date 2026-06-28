from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service, service_proxy

from splent_io.splent_feature_slider.services import SliderService

slider_bp = create_blueprint(__name__)


def init_feature(app):
    register_service(app, "SliderService", SliderService)


def inject_context_vars(app):
    # Expose the active slides so the carousel (rendered via the layout.hero
    # hook) can pick them up. Safe if the service is somehow unavailable.
    def slider_items():
        try:
            return service_proxy("SliderService").active_slides()
        except Exception:
            return []

    return {"slider_items": slider_items}
