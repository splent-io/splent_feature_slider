"""Template hooks for splent_feature_slider.

* ``layout.authenticated_sidebar`` — admin sidebar link to the slide manager.
* ``layout.hero`` — renders the public carousel above the page content.

The carousel's CSS and JS are NOT injected here: they are declared through the
asset registry (in __init__.init_feature) so the shell loads them in a
deduplicated, deterministic order — same pattern as the skins. The carousel
markup is config-driven (overlay / autoplay / interval / caption colour) via the
admin-editable settings read by config_store.get_config().
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


def slider_hero():
    """Render the carousel into the full-width hero slot above the content.

    Scope-aware: by default (scope="home") it renders only on the homepage;
    "all" renders it on every public page. Behaviour comes from the framework's
    declarative settings schema (get_config) — no per-feature config module.
    """
    from splent_framework.settings.settings_schema import get_config

    cfg = get_config("slider")
    if cfg.get("scope", "home") == "home" and request.endpoint != "public.index":
        return ""
    try:
        slides = service_proxy("SliderService").active_slides()
    except Exception:
        return ""
    if not slides:
        return ""
    return Markup(
        render_template("slider/carousel.html", slides=slides, cfg=cfg)
    )


register_template_hook("layout.authenticated_sidebar", slider_admin_link)
register_template_hook("layout.hero", slider_hero)
