try:
    # default
    import functools
    from typing import Callable, TYPE_CHECKING

    if TYPE_CHECKING:
        from .Manager import IoTManager

    # external
    import flask
    from flask_restful import Resource, reqparse

    # internal
    from .Endpoint import ValidationResponse, EndpointType


    class EndpointResource(Resource):
        def __init__(self, manager: 'IoTManager', auth_decorator: Callable):
            self.manager = manager

            # decorate post method with the provided decorator
            if auth_decorator:
                self.post = auth_decorator(self.post)

            self.post_parser = reqparse.RequestParser()
            self.post_parser.add_argument("clientId", location=["json", "args"], required=True, type=str,
                                          help="ID of Client.")
            self.post_parser.add_argument("endpointId", location=["json", "args"], required=True, type=str,
                                          help="ID of Endpoint where data should be sent.")
            self.post_parser.add_argument("data", location=["json", "args"], required=True, help="Data to be sent.")

        def post(self):
            args = self.post_parser.parse_args()

            # get validator for the specified client and endpoint
            validator = self.manager.get_validator(args["clientId"], args["endpointId"])

            # check if validator was found
            if isinstance(validator, ValidationResponse):
                return {
                    "success": False,
                    "error": validator.value
                }, 400

            # try and validate the data
            response, data = validator.validate(args["data"])

            # if validation failed
            if response != ValidationResponse.VALID:
                return {
                    "success": False,
                    "error": response.value
                }, 400

            # if validation worked then send the data and return a success
            self.manager.emit(validator.id, data, client_id=args["clientId"])

            return {
                "success": True
            }

except ImportError:
    EndpointResource = None
