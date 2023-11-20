from bk_notice_sdk import config
from bk_notice_sdk.utils import return_json_response, api_call


@return_json_response
def get_current_information(request):
    """获得当前平台的通知公告信息"""
    return api_call(
        api_method="announcement_get_current_announcements",
        success_message="平台获取通知公告信息成功",
        error_message="获取通知公告异常",
        params={"platform": config.PLATFORM},
    )
