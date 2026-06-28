from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from splent_io.splent_feature_slider import slider_bp
from splent_framework.services.service_locator import service_proxy


def _slider_service():
    return service_proxy("SliderService")


def _media_images():
    """Image-only media items for the picker (newest first)."""
    try:
        items = service_proxy("MediaService").list_recent()
    except Exception:
        return []
    return [m for m in items if m.is_image]


def _media_for(slide):
    """Picker images, guaranteeing the slide's CURRENT image is selectable even
    if it dropped out of list_recent() — otherwise editing would silently clear
    the image on save."""
    media = _media_images()
    if slide is not None and slide.media is not None:
        if all(m.id != slide.media.id for m in media):
            media = [slide.media] + media
    return media


def _safe_link(href):
    """Allow only safe link targets — blocks javascript:/data: (stored XSS),
    since the link is rendered into a public <a href> for every visitor."""
    href = (href or "").strip()
    low = href.lower()
    if low.startswith(("http://", "https://", "mailto:")) or href.startswith(("/", "#")):
        return href
    return ""


def _form_to_data(form):
    """Read the slide form into a clean kwargs dict for the service.

    media_id is an int when a real image is picked, otherwise None (the
    "no image" radio submits an empty value). order falls back to 0. link is
    scheme-checked so a malicious javascript: URL can't reach the public page.
    """
    raw_media = (form.get("media_id") or "").strip()
    media_id = int(raw_media) if raw_media.isdigit() else None

    raw_order = (form.get("order") or "").strip()
    try:
        order = int(raw_order)
    except ValueError:
        order = 0

    return {
        "media_id": media_id,
        "title": (form.get("title") or "").strip(),
        "caption": (form.get("caption") or "").strip(),
        "link": _safe_link(form.get("link")),
        "order": order,
        "active": "active" in form,
    }


# =====================================================================
# ADMIN — slides
# =====================================================================
@slider_bp.route("/admin/slider", methods=["GET"])
@login_required
def admin_index():
    slides = _slider_service().all_slides()
    return render_template("slider/admin/list.html", slides=slides)


@slider_bp.route("/admin/slider/new", methods=["GET", "POST"])
@login_required
def admin_new():
    if request.method == "POST":
        data = _form_to_data(request.form)
        _slider_service().create(**data)
        flash("Slide created.", "success")
        return redirect(url_for("slider.admin_index"))
    return render_template(
        "slider/admin/form.html", slide=None, media=_media_for(None)
    )


@slider_bp.route("/admin/slider/<int:slide_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit(slide_id):
    service = _slider_service()
    slide = service.get(slide_id)
    if slide is None:
        abort(404)
    if request.method == "POST":
        data = _form_to_data(request.form)
        service.update(slide, **data)
        flash("Slide updated.", "success")
        return redirect(url_for("slider.admin_index"))
    return render_template(
        "slider/admin/form.html", slide=slide, media=_media_for(slide)
    )


@slider_bp.route("/admin/slider/<int:slide_id>/delete", methods=["POST"])
@login_required
def admin_delete(slide_id):
    service = _slider_service()
    slide = service.get(slide_id)
    if slide is None:
        abort(404)
    service.delete(slide)
    flash("Slide deleted.", "success")
    return redirect(url_for("slider.admin_index"))
