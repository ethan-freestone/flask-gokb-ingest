from flask import Blueprint, jsonify
from extensions import db # This is the centralised DB connection
from models.tipp import Title, Identifier

## Learning how to translate spring/MN patterns to Flask
# url_prefix behaves like Micronaut's @Controller("/tipp")
tipp_bp = Blueprint("tipp", __name__, url_prefix="/tipp")

@tipp_bp.route("", methods=["GET"])
def get_all():
    title_page = db.paginate(db.select(Title))

    return jsonify({
        "total": title_page.total,
        "page": title_page.page,
        "per_page": title_page.per_page,
        "pages": title_page.pages,
        "has_next": title_page.has_next,
        "has_prev": title_page.has_prev,
        "items": [item.to_dict() for item in title_page.items]
    }), 200

@tipp_bp.route("/count", methods=["GET"])
def get_count():
    title_count = db.session.scalar(db.select(db.func.count(Title.id)))
    return jsonify({"count": title_count}), 200

# Typing DIRECT in route params
@tipp_bp.route("/<int:title_id>", methods=["GET"])
def get_one(title_id):
    title = db.session.get(Title, title_id)
    if not title:
        return jsonify({"error": "Title not found"}), 404
    return jsonify(title.to_dict()), 200