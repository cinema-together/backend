from api.v1 import namespace

register_parser = namespace.parser()
register_parser.add_argument("login", type=str, required=True, help="Login is required", location="form")
register_parser.add_argument("password", type=str, required=True, help="Password is required", location="form")
register_parser.add_argument("email", type=str, required=True, help="Email is required", location="form")

login_parser = namespace.parser()
login_parser.add_argument("login", type=str, required=True, help="Login is required", location="form")
login_parser.add_argument("password", type=str, required=True, help="Password is required", location="form")

change_password_parser = namespace.parser()
change_password_parser.add_argument('current_password', type=str, required=True, help='Wrong Password',
                                    location="form")
change_password_parser.add_argument('new_password', type=str, required=True, help='Wrong Password', location="form")

