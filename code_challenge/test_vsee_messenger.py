from code_challenge.handler.vsee_messenger import SimpleVSeeMessengerTests
from datetime import datetime

if __name__ == '__main__':

    # TODO: Thang Truong - Need a method to detect desired_caps automatically
    caps = dict(platformName="Android",
                deviceName="emulator-5554",
                automationName="UIAutomator2",
                avd='PixelXLAPI30',
                avdReadyTimeout=50000,
                avdLaunchTimeout=900000,
                app="C:\\Users\\Thang Truong\\Downloads\\VSee-vsee-beta.apk")

    executor = 'http://localhost:4734/wd/hub'

    # TODO: Use a registered account (Thang Truong with note)
    user = 'thangluca@gmail.com'
    password = 'Tt#270819'

    # datetime object containing current date and time
    now = datetime.now()
    time_send = now.strftime("%d/%m/%Y %H:%M")
    sContact = 'Test Call'
    sMessage = ('happy to say Hello to you %s now %s' % (sContact, time_send))

    oVSee_Messenger = SimpleVSeeMessengerTests(desired_caps=caps, executor=executor, user=user, credential=password)
    oVSee_Messenger.login()
    sMessageStatus = oVSee_Messenger.sendMessage(sContact=sContact, sMessage=sMessage)
    # Make sure the message is delivered
    assert sMessageStatus == 'Delivered', 'The message should be Delivered instead of %s' % sMessageStatus
