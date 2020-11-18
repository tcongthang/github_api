from appium import webdriver
import logging
import time
from code_challenge.handler.appium_server import AppiumServer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SimpleVSeeMessengerTests(object):

    def __init__(self, desired_caps, executor, user, credential):
        # set up appium
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filemode='w')
        # Creating an object
        logger = logging.getLogger()
        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.INFO)
        # Start Appium Server
        appium_server = AppiumServer()
        appium_server.start_server()

        self.logger = logging.info
        self.desired_caps = desired_caps
        self.user = user
        self.credential = credential
        self.executor = executor
        # get locator definition
        self.locator = Locators(desired_caps['platformName'])
        self.driver = self.__openVsee()

    def tearDown(self):
        self.driver.quit()

    def __openVsee(self):

        # time.sleep(60)
        # TODO: Thang Truong should have the way to handle appium serve (auto-start, with ip, port ....)
        # todo: Thang Truong - Should we have a better way? example of handle different port & server address
        # appium_service = AppiumService()
        # #set Path: https://www.qafox.com/appium-configuring-node-js-and-npm/
        # appium_service.start()

        driver = webdriver.Remote(command_executor=self.executor, desired_capabilities=self.desired_caps)
        time.sleep(30)
        self.logger('INFO: driver.session_id %s' % driver.session_id)
        # make sure the right package and activity were started
        self.logger('INFO: current_package %s' % driver.current_package)
        self.logger('INFO: driver.current_activity %s' % driver.current_activity)
        # self.logger('INFO:  driver.title %s' % driver.title)

        return driver

    def login(self):
        # self.__waitforelement(type=By.ID, element='com.vsee.vsee.beta:id/loginEmailEdit')
        time.sleep(10)
        self.logger('Enter username/email')
        ele_email_login = self.driver.find_element_by_id('com.vsee.vsee.beta:id/loginEmailEdit')
        ele_email_login.send_keys(self.user)

        self.logger('Enter credential')
        ele_email_paswd = self.driver.find_element_by_id('com.vsee.vsee.beta:id/loginPasswordEdit')
        ele_email_paswd.send_keys(self.credential)

        self.logger('Press SignIn button')
        btn_Sign_in = self.driver.find_element_by_id('com.vsee.vsee.beta:id/loginSignInBut')
        btn_Sign_in.click()
        time.sleep(20)
        # self.__waitforelement(type=By.CLASS_NAME, element=self.locator.csWelcome)

    def switchtoContacts(self):
        self.driver.find_element_by_xpath(self.locator.xpContacts).click()
        time.sleep(2)

    def switchtoChats(self):
        self.driver.find_element_by_xpath(self.locator.xpChats).click()
        time.sleep(2)

    def switchtoCalls(self):
        self.driver.find_element_by_xpath(self.locator.xpCalls).click()
        time.sleep(2)

    # Function relating to Chats view
    def getlistChatPicker(self):
        org = self.driver.find_element_by_xpath(self.locator.xpChats)
        if org.get_attribute("selected") == 'true':
            print('ALREADY ON CHATS VIEW')
        else:
            self.switchtoChats()
        return self.driver.find_elements(By.XPATH, self.locator.xpChatPicker)

    def startNewChat(self):
        self.driver.find_element_by_xpath(self.locator.xpTopChatIcon).click()

    # Function relating to Contacts view
    def findContact(self, sContact):
        for element in self.getlistContact():
            if sContact == element.text:
                return element

        return False

    def getlistContact(self):
        # Switch to Contacts tab first
        self.switchtoContacts()
        return self.driver.find_elements(By.XPATH, self.locator.xpLstContact)

    def sendMessage(self, sContact='Test Call', sMessage=None):
        """
        This is a function to send a message to the Contact who chat together before - showing on Chats view
        :param sContact: People we want to chat
        :param sMessage: text message
        :return: Status of text message or False
        """
        lstPicker = self.getlistChatPicker()
        time.sleep(5)
        for oChat in lstPicker:
            if sContact == oChat.text:
                oChat.click()
                # time.sleep(2)
                self.driver.find_element_by_xpath(self.locator.xpChatEditTextBox).send_keys(sMessage)
                # time.sleep(2)
                # Click send button
                self.driver.find_element_by_xpath(self.locator.xpSendMessagesBtn).click()
                time.sleep(1)
                self.logger('Message: %s should be sent to %s' % (sMessage, sContact))
                sMessageStatus = self.driver.find_element_by_xpath(self.locator.xpMessageStatus).text

                return sMessageStatus

        self.logger('Hey, Look likes the you have never sent message to %s - should use another way' % sContact)

        return False

    def sendFirstMessage(self, sContact='Test Call', sMessage=None):
        """
        This is a function to send a message to the Contact who has a first chat - not shown on Chats view yet
        :param sContact: People we want to chat
        :param sMessage: text message
        :return: Status of text message
        """
        # Switch to Contacts tab first
        self.switchtoContacts()
        lstContact = self.getlistContact()
        oElement = None
        for sContactElement in lstContact:
            if sContact == sContactElement.text:
                oElement = sContactElement
        time.sleep(5)
        oElement.click()

    ######### On-going function ###################
    def __waitforelement(self, type, element):
        # try:
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((type, element)))
        #
        # finally:
        #     self.driver.quit()


    # def test_home_screen(self):
    #     self.logger('Check to make sure new contact/group icon is shown')
    #     add_icon = self.driver.find_element_by_id('com.vsee.vsee.beta:id/action_add')
    #     self.assertEqual(add_icon.tag_name, 'Add Contact/Group')
    #
    #     self.logger('Check to make sure Chats tab icon is shown')
    #
    #     self.driver.find_element_by_accessibility_id(self.locator.idChats)
    #     self.driver.find_element_by_xpath(self.locator.xpChats)
    #     self.logger('Check to make sure the Calls tab icon is shown')
    #
    #     self.driver.find_element_by_accessibility_id(self.locator.idCalls)
    #     self.driver.find_element_by_xpath(self.locator.xpCalls)
    #     self.logger('Check to make sure the Contacts tab icon is shown')
    #
    #     self.driver.find_element_by_accessibility_id(self.locator.idContacts)
    #     self.driver.find_element_by_xpath(self.locator.xpContacts)
    #     self.logger('Check to make sure the More icon is shown')
    #
    #     self.driver.find_element_by_accessibility_id(self.locator.idMore)
    #     self.driver.find_element_by_xpath(self.locator.xpMore)
    #
    #     self.logger('Check to make sure the Search Contacts box is shown')
    #     self.driver.find_element_by_id(self.locator.idSearch)

class Locators(object):
    """
    Class to define the locator of element
    """
    def __init__(self, platform):

        self.platform = platform
        # Maybe this can be handle to check multiple version of app
        base = 'com.vsee.vsee.beta'

        if 'Android' in self.platform:

            # bottom action bar
            self.idChats = 'Chats'
            self.xpChats = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Chats"]'

            self.idCalls = 'Calls'
            self.xpCalls = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Calls"]'

            self.idContacts = 'Contacts'
            self.xpContacts = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Contacts"]'

            self.idMore = 'More'
            self.xpMore = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="More"]'

            # Element on Contacts screen-view
            self.idSearch = 'contact_list_search_view'
            self.idContactLst = 'com.vsee.vsee.beta:id/contactListView'
            self.csContactView = 'android.view.ViewGroup'
            self.csWelcome = 'android.widget.TextView'
            self.xpLstContact = "//*[@resource-id='com.vsee.vsee.beta:id/itemContactListNameView']"

            # Element on Chats screen-view
            self.xpChatPicker = "//*[@resource-id='com.vsee.vsee.beta:id/chat_picker_name']"
            self.xpTopChatIcon = '//android.widget.TextView[@content-desc="Chat"]'

            # Element on a running Chat view
            self.xpChatText = "//*[@resource-id='com.vsee.vsee.beta:id/chat_picker_background_layout']"
            self.xpSendMessagesBtn = "//*[@resource-id='com.vsee.vsee.beta:id/chatSendBut']"
            self.xpLstMessagesDelivered = "//*[@resource-id='com.vsee.vsee.beta:id/message_text']"
            self.xpChatEditTextBox = "//*[@resource-id='com.vsee.vsee.beta:id/chatEditText']"
            self.xpMessageStatus = "//*[@resource-id='com.vsee.vsee.beta:id/message_status']"

        else:
            raise ValueError('ERROR: SHOULD DEFINE EXECUTION PLATFORM HERE Ex: iOS, WinApp ...')

