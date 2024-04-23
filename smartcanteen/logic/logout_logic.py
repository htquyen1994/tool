from flask import Response, make_response
from swagger_server.models import UserInfo, LoginResponse
from smartcanteen.util.trader_agent import TraderAgent



class LogoutLogic:
    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def logout_post(cls):
        """
        Do logout
        :rtype: CommResponse
        :return: Logout result
        """
        TraderAgent.get_instance().set_session(None)
        return Util.make_json_response(session_key=''), ResponseMessage.Success.http_code
