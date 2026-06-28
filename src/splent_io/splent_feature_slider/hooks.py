"""Template hooks for splent_feature_slider.

Three slots:

* ``layout.authenticated_sidebar`` — admin sidebar link to the slide manager.
* ``layout.head`` — the carousel stylesheet (served via the blueprint asset
  route, same pattern as the skins).
* ``layout.hero`` — renders the public carousel above the page content. The
  carousel template is self-contained (markup + its own init script).
"""

from flask import render_template, request, url_for
from markupsafe import Markup

from splent_framework.hooks.template_hooks import register_template_hook
from splent_framework.services.service_locator import service_proxy


def slider_admin_link():
    """Sidebar entry for the slide manager (the WP-plugin pattern)."""
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("slider.admin")
        else ""
    )
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("slider.admin_index")}">'
        '<i class="align-middle" data-feather="image"></i> '
        '<span class="align-middle">Slider</span>'
        "</a>"
        "</li>"
    )


def slider_styles():
    """Inject the carousel stylesheet into the public shell's head."""
    return (
        '<link rel="stylesheet" href="'
        + url_for("slider.assets", subfolder="css", filename="slider.css")
        + '">'
    )


def slider_hero():
    """Render the carousel into the full-width hero slot above the content."""
    try:
        slides = service_proxy("SliderService").active_slides()
    except Exception:
        return ""
    if not slides:
        return ""
    return Markup(render_template("slider/carousel.html", slides=slides))


register_template_hook("layout.authenticated_sidebar", slider_admin_link)
register_template_hook("layout.head", slider_styles)
register_template_hook("layout.hero", slider_hero)
