from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
import time
import os
from common import adb_shell

Adb_shell = adb_shell.AdbShell()


class GameIn(object):
    class UnityPoco():
        def __init__(self):
            self.poco = UnityPoco()

        def login_unity(self, game_server):
            """
            到点击登录按钮的login
            """

            self.poco.click([0.05, 0.163])
            time.sleep(1)
            self.poco.click([0.1, 0.13])
            os.system(r'adb shell input text ' + game_server)
            self.poco.click([0.934, 0.867])
            self.poco.click([0.03, 0.13])
            self.poco("ObjLoginBtns").child("1").child('Image').click()
            try:
                self.poco("horizontalBtns").wait_for_appearance(timeout=5)
                self.poco("BtnOk").click()
            except Exception:
                print('已通过权限检测')

        def login_touch(self):
            self.poco("ObjLoginBtns").child("1").child('Image').click()

        def skip_anime(self):
            try:
                self.poco("UIPopupPlayVideo").wait_for_appearance(timeout=8)
                print('已进入到播放动画界面')
                try:
                    self.poco("txtSkip").click()
                    self.poco("BtnOk").click()
                except Exception:
                    self.poco("UIPopupPlayVideo").click()
                    self.poco("txtSkip").click()
                    self.poco("BtnOk").click()
            except Exception:
                print('本次客户端没有播放动画')

        def board(self):
            try:
                self.poco("UIPopupLoginNotice").wait_for_appearance(timeout=5)
                for _ in range(3):
                    try:
                        fp = self.poco.freeze()
                        try:
                            fp("CloseBtn").click()
                        except:
                            fp("ObjBtns").child("BtnOk").click()
                    except:
                        break
            except Exception:
                print('无游戏公告')

        def get_ready(self):
            """
            到大厅准备好，可以直接调用aico的run的方法，这个写完，前面的连起来就可以用了！！
            """
            def _sign():
                """
                日常签到的关闭
                """
                if self.poco("BtnSignIn").exists():
                    self.poco("BtnSignIn").click()
                    self.poco("btns").child("btnOk").click()
                    self.poco("topBG").child("Back").click()

            def _bfi_close():
                """
                最烦人的拍脸图关闭
                """
                for _ in range(30):
                    if self.poco("btnClose").exists():
                        self.poco("btnClose").click()
                    elif self.poco("UIHallSeasonStart").offspring("BtnOk").exists():
                        self.poco("UIHallSeasonStart").offspring("BtnOk").click()
                    elif self.poco("Close").exists() != False:
                        self.poco("Close").click()
                    elif self.poco("nextText").exists():
                        self.poco("nextText").click()
                    elif self.poco("Close").exists():
                        self.poco("Close").click()
                    elif self.poco("CloseBtn").exists():
                        self.poco("CloseBtn").click()
                    elif self.poco("point").offspring("BtnClose").exists():
                        self.poco("point").offspring("BtnClose").click()
                    elif self.poco("X").exists() != False:
                        self.poco("X").click()
                    elif self.poco("EnContent").child("Back").exists():
                        self.poco("EnContent").child("Back").click()
                    elif self.poco("empty").exists():
                        try:
                            self.poco("empty").click()
                        except Exception:
                            pass
                    else:
                        break
                    time.sleep(0.5)

            # 如果是新角色 需要创建角色
            if self.poco("btnCreatPlayer").exists():
                self.poco("btnCreatPlayer").click()
                self.poco("inputName").set_text("萝卜头")
                self.poco("BtnConfirm").click()
                self.poco("Button_Leave").click()
            else:
                print('不是新用户 直接进入到主界面')
            # 如果存在向导
            if self.poco("Panel").child("Guider").exists():
                self.poco.click([0.057, 0.96])

            else:
                print('直接进入到了游戏 又不是新角色 也过了引导')
            # 这里就可以选择模式了
            _bfi_close()
            try:
                _sign()
            except Exception:
                pass
            now_mode = self.poco("txtModeName").child("txt_main").get_text()
            if '单人' not in now_mode:
                self.poco("CityMode").click()
                time.sleep(1)
                self.poco.swipe([0.1, 0.5], [0.55, 0.5])
                for i in range(7):
                    mode_name = \
                    self.poco("UIHallSelectMode").offspring("Mask").child("Content").child("UIModeItem(Clone)")[
                        i].offspring(
                        "PnlCountent1").children()[2].get_text()
                    if '单人休闲模式' in mode_name:
                        self.poco("UIHallSelectMode").offspring("Mask").child("Content").child("UIModeItem(Clone)")[
                            0].offspring("PnlCountent1").click()
                        break
                _bfi_close()
                _sign()

        def battle_remind(self):
            """
            处理破势的方法
            """

            def battle_start():
                time.sleep(1)
                self.poco(texture="ui_zy_msxz_ks").click()
                self.poco("Panel").child("BtnOk").wait_for_appearance()
                self.poco("Panel").child("BtnOk").click()

            battle_start()
            self.poco("0").wait_for_appearance()
            time.sleep(4)
            # 卖棋子
            self.poco("0").click()
            Adb_shell.tap([0.26, 0.89])
            time.sleep(0.5)
            Adb_shell.swipe([0.26, 0.89], [0.055, 0.7])
            time.sleep(1)
            try:
                self.poco("Checkmark").click()
                self.poco("Button_Ok").click()
            except Exception:
                pass
            # 刷棋盘
            self.poco("DebugCanvas").child("Button").click()
            Adb_shell.swipe([0.74, 0.4], [0.74, 0.33])
            time.sleep(2)
            self.poco("加满金币").child("Button").click()
            self.poco(text="关闭").click()
            try:
                self.poco("Button_Fresh").click()
            except Exception:
                self.poco("Button_Store").click()
                try:
                    self.poco("Button_Fresh").click()
                except Exception:
                    self.poco("Button_Store").click()
                    self.poco("Button_Fresh").click()

            try:
                self.poco("Checkmark").click()
                self.poco("Button_Ok").click()
            except Exception:
                pass
            # 升人口
            self.poco("Button_ReadChessBook").click()
            if self.poco("Checkmark").exists() == False:
                self.poco("Button_ReadChessBook").click()
            try:
                self.poco("Checkmark").click()
                self.poco("Button_Ok").click()
            except Exception:
                pass

        def battle_finish(self):
            self.poco("DebugCanvas").child("Button").click()
            self.poco("结束战斗").child("Button").click()
            self.poco("Close").child("Text").click()
            time.sleep(2)
            self.poco("Button_Leave").click()
            try:
                self.poco("btns").child("btnOk").click()
            except Exception:
                pass
            time.sleep(2)
            try:
                self.poco("btnContinue").click()
            except Exception:
                pass
            try:
                self.poco("Panle").child("textCloseDes").click()
            except Exception:
                pass
            try:
                self.poco("BtnClose").click()
                self.poco.click([0.02, 0.025])
            except Exception:
                self.poco.click([0.02, 0.025])
                try:
                    self.poco("btnContinue").click()
                    if self.poco("BtnClose").exists():
                        self.poco.click([0.02, 0.025])
                except Exception:
                    pass
            try:
                self.poco.click([0.02, 0.025])
                self.poco("btns").child("btnOk").click()
            except Exception:
                pass

    class AndroidPoco():
        def __init__(self):
            self.poco = AndroidUiautomationPoco()

        def login_android(self):
            """
            使用sdk进行自动化操作的部分，对龙渊的安卓登录sdk做自动化登录使用
            """
            try:
                print('外部sdk登录流程')
                self.poco("com.dragonest.autochess.google:id/ilong_username_edittext").set_text('testlongyuan506')
                self.poco("com.dragonest.autochess.google:id/ilong_password_edittext").set_text('1qaz2wsx')
                self.poco.click([0.52, 0.6])
            except Exception:
                print('已有账号登录')


class GameOut(object):
    def __init__(self):
        self.poco = AndroidUiautomationPoco()

    def install_pag(self, pag_path):
        os.system(r'adb uninstall com.ilongyuan.autochess.ly_pre')
        os.system(r'adb uninstall com.dragonest.autochess.google')
        print('进入装包流程')
        os.system(r'adb install -r ' + pag_path)

    def run_game(self):
        try:
            os.system(r'adb shell am start -W -n '
                  'com.dragonest.autochess.google/com.ilongyuan.autochess.impl.CommonMainActivity')
        except Exception:
            self.poco("Auto Chess").click()
            print('游戏已启动 等待权限检测')
            time.sleep(15)
            print('已通过权限检测')
            time.sleep(3)


def run(pag_path, game_server):
    go = GameOut()
    gi_a = GameIn.AndroidPoco()
    go.install_pag(pag_path)
    time.sleep(5)
    go.run_game()
    time.sleep(15)
    # 等待游戏启动
    gi_u = GameIn.UnityPoco()
    gi_u.login_unity(game_server)
    gi_u.board()
    gi_u.skip_anime()
    time.sleep(10)
    gi_a.login_android()
    time.sleep(10)


def restart():
    go = GameOut()
    go.run_game()
    # 等待游戏启动
    gi_u = GameIn.UnityPoco()
    gi_u.login_touch()
    gi_u.board()
    time.sleep(10)
    gi_u.get_ready()


if __name__ == '__main__':
    gu = GameIn.UnityPoco()
    gu.login_unity('47.103.148.75:3063')

