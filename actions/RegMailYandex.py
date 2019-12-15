import time, traceback, os, sys
#local
from Action import Action, ActionResult
parentPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from init_webdriver import BrowserFactory

class RegMailYandexAction(Action):
    def __init__(self, *args, **kwargs):
        super(RegMailYandexAction, self).__init__(*args, **kwargs)

    def execute(self):
        """
        https://mail.yandex.ru/
        """
        self.info('getting https://mail.yandex.ru/')
        self.browser.get('https://mail.yandex.ru/')
        self.browser.set_page_load_timeout(10)
        if (not self.sleepTillLoaded()):
            return self.actionResult(error='https://mail.yandex.ru not loaded')

        res = self.createAccountBtnClick()
        if isinstance(res, ActionResult):
            return res



        # at the very end:
        return self.actionResult()


    def createAccountBtnClick(self):
        """
        https://mail.yandex.ru/
        .HeadBanner-CentralColumn .HeadBanner-ButtonsWrapper
            a.button2 button2_size_mail-big button2_theme_mail-action button2_type_link HeadBanner-Button with-shadow
                span
                    text: Создать аккаунт
        expect:     https://passport.yandex.ru/registration/mail
        """
        self.info('createAccountBtnClick()')
        btns = self.browser.find_elements_by_css_selector('.HeadBanner-CentralColumn .HeadBanner-ButtonsWrapper a.button2')
        reg_btn = None
        for btn in btns:
            spans = btn.find_elements_by_css_selector('span')
            if 0 == len(spans):
                continue
            span = spans[0]
            txt = span.text
            if 'Создать аккаунт' in txt:
                reg_btn = btn
                break
        if not reg_btn:
            return self.actionResult(error="Кнопка Создать аккаунт не обнаружена")
        self.moveToElem(reg_btn)
        previous_url = self.browser.current_url
        reg_btn.click()
        self.sleepTillLoaded(previous_url=previous_url)
        if ("/registration/mail" != self.getCurrentPath().rstrip('/')):
            return self.actionResult(error="Не открылась /registration/mail")
        return True

    def fillRegForm(self):
        """
        .registration__label[for="firstname"]
            click()
        #firstname
            send_keys()

        .registration__label[for="lastname"]
            click()
        #lastname
            send_keys()

        .registration__label[for="login"]
            click()
        #login
            send_keys()
                wait 1 sec
                need check
                if .form__popup-error[data-t="login-error"] isVisible() than repeat

        .registration__label[for="password"]
            click()
        #password
            send_keys()

        .registration__label[for="password_confirm"]
            click()
        #password_confirm
            send_keys()

        #money_eula_accepted    assert checked ??
            создать Яндекс.Кошелек

        #eula_accepted
            assert checked()

        .link_has-no-phone
            У меня нет телефона
            click()



        """


def main():
    """
    easy test
    """
    browser = None
    try:
        browser = BrowserFactory().getInstance()
        a = RegMailYandexAction(browser=browser)
        res = a.run()
        print(res.__dict__)
        time.sleep(7)
    except Exception as e:
        traceback.print_exc()
    finally:
        if 'WebDriver' in type(browser).__name__:
            browser.quit()

if '__main__' == __name__:
    main()