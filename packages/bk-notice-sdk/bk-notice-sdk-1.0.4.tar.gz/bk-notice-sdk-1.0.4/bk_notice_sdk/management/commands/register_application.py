from django.core.management.base import BaseCommand, CommandError

from bk_notice_sdk.views import api_call


class Command(BaseCommand):
    help = "注册平台"

    def handle(self, *args, **options):
        try:
            print("[bk-notice-sdk]call register_application start")
            response = api_call(
                api_method="register_application", success_message="注册平台成功", error_message="注册平台异常", success_code=201
            )
            if response.get("result") is True:
                print("Successfully registered platform")
                self.stdout.write(self.style.SUCCESS("成功注册平台"))
            else:
                print("Registration platform failed:", response["message"])
                raise CommandError("注册平台失败:" + response["message"])
        except Exception as e:
            print("Registration platform exception:", str(e))
            raise CommandError(f"注册平台异常: {e}")
