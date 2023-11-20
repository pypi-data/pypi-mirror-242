import os

from django.conf import settings

stage = os.getenv("BKPAAS_ENVIRONMENT", "prod")
mapping = {"stag": "stage", "prod": "prod"}
# 默认设置
BK_NOTICE = {
    "STAGE": mapping[stage],
    "BK_API_URL_TMPL": os.getenv("BK_API_URL_TMPL"),
    "PLATFORM": os.getenv("APP_CODE", getattr(settings, "APP_CODE", None)),
    "ENTRANCE_URL": "notice/",
}

# 用户配置
USER_SETTING = getattr(settings, "BK_NOTICE", {})

# 合并后配置，以用户配置为主
bk_notice = BK_NOTICE.copy()
bk_notice.update(USER_SETTING)

# 版本
STAGE = bk_notice["STAGE"]

# apigw的模板链接
BK_API_URL_TMPL = bk_notice["BK_API_URL_TMPL"]

# 平台
PLATFORM = bk_notice["PLATFORM"]

# 入口URL
ENTRANCE_URL = bk_notice["ENTRANCE_URL"]

for k, v in bk_notice.items():
    if v is None:
        raise ValueError(f"Missing environment variable: {k}")
