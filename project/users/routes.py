from . import users_blueprint

@users_blueprint.route('/users')
def users_list():
    return "User List"
