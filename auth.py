from flask import abort
from setup import db
from flask_jwt_extended import get_jwt_identity
from models.user import User


#function to allow access to admin only
def admin_required():
    admin_id = get_jwt_identity()
    stmt = db.select(User).where(User.id == admin_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        return abort(401)