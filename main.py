from functools import partial
from os import walk, path, remove
from random import shuffle
from time import sleep
from shutil import move
from plyer import filechooser
import datetime

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.toast import toast
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.behaviors.magic_behavior import MagicBehavior
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from functools import partial

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


# Custom Widget
class MagicButton1(MagicBehavior, Button):
    pass


class MagicButton(MagicBehavior, MDRaisedButton):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class SearchTestPage(Screen):
    pass


class AboutUsPage(Screen):
    pass


class ResultPage(Screen):
    pass


class MakeTestPage(Screen):
    pass


class ChangeAvatarPage(Screen):
    pass


class DashboardPage(Screen):
    pass


class WelcomePage(Screen):
    pass


class ProfileEdit(Screen):
    pass


class MainApp(MDApp):
    defaultName = "Default Name"

    def build(self):
        return Builder.load_file('main.kv')

    def on_start(self):
        for root_dir, folders, files in walk("avatars"):
            for av in files:
                self.root.ids['chng_avatar'].ids['avatar_grid'].add_widget(
                    ImageButton(
                        source="avatars/"+av,
                        on_release=partial(self.change_avatar, av)
                    )
                )

        for root_dir, folders, files in walk("avatars"):
            for av in files:
                self.root.ids['profileEdit'].ids['avatar_grid'].add_widget(
                    ImageButton(
                        source="avatars/"+av,
                        on_release=partial(self.change_avatar, av)
                    )
                )

        # anim1 = Animation(pos_hint={'center_y': .8}, size_hint=(.8, .8))
        # anim1.start(self.root.ids['welcome'].ids['img'])

        # bx = Animation(pos_hint={'center_y': .5}, duration=1)
        # bx.start(self.root.ids['welcome'].ids['log_in_field'])

        # Animation(pos_hint={'top': .1}, duration=1.5).start(
        #     self.root.ids['welcome'].ids['scrn_btn'])

        # # grid test
        # for root_dir, folders, files in walk("test"):
        #     if files != []:
        #         for file in files:
        #             if file.endswith('.mock'):
        #                 self.fileName = path.splitext(file)[0]
        #                 date, name, id = self.fileName.split(' ')
        #                 self.root.ids['make_test'].ids['LIST'].add_widget(
        #                     ThreeLineListItem(
        #                         text=name,
        #                         secondary_text="ID:- "+id,
        #                         tertiary_text="Date:- "+date,
        #                         on_release=partial(self.openCreatedFile, date)
        #                     )
        #                 )

    def avatarGrid(self):
        # Grid avatars
        for root_dir, folders, files in walk("avatars"):
            for av in files:
                self.root.ids['chng_avatar'].ids['avatar_grid'].add_widget(
                    ImageButton(
                        source="avatars/"+av,
                        on_release=partial(self.change_avatar, av)
                    )
                )

    def welcomeAnim(self):
        anim1 = Animation(pos_hint={'center_y': .8}, size_hint=(.8, .8))
        anim1.start(self.root.ids['welcome'].ids['img'])

        bx = Animation(pos_hint={'center_y': .5}, duration=1)
        bx.start(self.root.ids['welcome'].ids['log_in_field'])

        Animation(pos_hint={'top': .1}, duration=1.5).start(
            self.root.ids['welcome'].ids['scrn_btn'])

    def profileEdit(self, userName):
        self.root.ids['dashboard'].ids['userName'].text = userName
        print(self.root.ids['dashboard'].ids['userName'].text)

    def change_avatar(self, avatarImage, btn_id):
        self.avatar = "avatars/" + avatarImage
        # self.root.ids['chng_avatar'].ids['av_btn'].source = "avatars/" + avatarImage
        self.root.ids['profileEdit'].ids['av_btn'].source = "avatars/" + avatarImage
        self.root.ids['dashboard'].ids['av_btn'].source = "avatars/" + avatarImage

    def openCreatedFile(self, *args):
        Mdate = datetime.datetime.strptime(args[0], "%Y-%m-%d").date()
        Tdate = datetime.date.today()
        print(Tdate, Mdate)

        # if args[0] == datetime.datetime.now().date():
        if Mdate == Tdate:
            with open("test/"+self.fileName+".mock", 'r') as open_current_test:
                line = open_current_test.readline()
                self.root.ids['make_test'].ids['mkt_sm'].current = 'preview'
                testName, testID, testDate, NumOfQues, TestDuration = line.split(
                    ',')
                self.root.ids['make_test'].ids['test_name'].text = testName
                self.root.ids['make_test'].ids['test_id'].text = testID
                self.root.ids['make_test'].ids['set_date'].text = testDate
                self.root.ids['make_test'].ids['num_of_ques'].text = NumOfQues
                self.root.ids['make_test'].ids['dur'].text = TestDuration
        elif Mdate < Tdate:
            for i in self.root.ids['make_test'].ids['LIST'].children:
                self.root.ids['make_test'].ids['LIST'].remove_widget(i)
            remove("test/" + self.fileName + ".mock")
            self.showToast("This test is outdated and it was deleted.")
        else:
            self.showToast("You Give this test on DATE:- " + args[0])

    def changeScreen(self, direction, scrn_name):
        sm = self.root.ids['sm']
        sm.current = scrn_name
        sm = SlideTransition(direction=direction)

    def navBar(self, navState):
        self.root.ids['nav'].set_state(navState)

    def makeNewTest(self):
        sm = self.root.ids['make_test'].ids['mkt_sm']
        sm.current = 'start'

    def setDate(self):
        import datetime
        dob = MDDatePicker(callback=self.get_date,
                           min_date=datetime.datetime.now().date())
        dob.open()

    def get_date(self, the_date):
        self.root.ids['make_test'].ids['set_date'].text = str(the_date)

    def confirmCard(self, opt):

        obj1 = self.root.ids['make_test'].ids['num_of_ques'].text
        obj2 = self.root.ids['make_test'].ids['dur'].text

        if obj1.isnumeric() and obj2.isnumeric():
            if opt == 'open':
                Animation(pos_hint={'center_y': .5}).start(
                    self.root.ids['make_test'].ids['confirm_card'])

            else:
                Animation(
                    pos_hint={'center_y': -1}).start(self.root.ids['make_test'].ids['confirm_card'])

        else:
            self.showToast(
                'number of question and test duration must be Integer')

    def showToast(self, instance):
        toast(instance)

    def pre_make_test(self):
        Animation(pos_hint={'top': .88}).start(
            self.root.ids['make_test'].ids['test_card'])
        self.second = 00
        self.dur = self.root.ids['make_test'].ids['dur'].text
        self.duration = divmod(int(self.dur), 60)
        self.minutes = self.duration[1]
        self.hours = self.duration[0]
        # Clock.schedule_interval(self.update_duration, 1)

        self.btnPress = 0
        self.num_of_ques = self.root.ids['make_test'].ids['num_of_ques'].text
        self.quesNumber = 1
        self.root.ids['make_test'].ids['quesNum'].text = f'Question No. {self.quesNumber}'

        self.quesOption = []
        try:
            with open("test/"+self.root.ids['make_test'].ids['set_date'].text + " " + self.root.ids['make_test'].ids['test_name'].text + " " + self.root.ids['make_test'].ids['test_id'].text + ".mock", 'r') as check_test:
                if check_test.readlines() != f"{self.root.ids['make_test'].ids['test_name'].text},{self.root.ids['make_test'].ids['test_id'].text},{self.root.ids['make_test'].ids['set_date'].text},{self.root.ids['make_test'].ids['num_of_ques'].text},{self.root.ids['make_test'].ids['dur'].text}\n":
                    pass
        except:
            with open("test/"+self.root.ids['make_test'].ids['set_date'].text + " " + self.root.ids['make_test'].ids['test_name'].text + " " + self.root.ids['make_test'].ids['test_id'].text + ".mock", 'a') as create_test:
                create_test.write(
                    f"{self.root.ids['make_test'].ids['test_name'].text},{self.root.ids['make_test'].ids['test_id'].text},{self.root.ids['make_test'].ids['set_date'].text},{self.root.ids['make_test'].ids['num_of_ques'].text},{self.root.ids['make_test'].ids['dur'].text}\n")

    def nextQues(self):
        if self.quesNumber != int(self.num_of_ques):
            if self.quesOption != []:
                self.btnPress = 1
                if self.btnPress == 1:
                    self.root.ids['make_test'].ids['submitbtn'].disabled = False
                    anim = Animation(pos_hint={'top': -1}) + \
                        Animation(pos_hint={'top': .88}, duration=1)
                    anim.start(self.root.ids['make_test'].ids['test_card'])
                    self.quesNumber += 1
                    try:
                        ques, a, b, c, d = self.quesOption[self.quesNumber - 1].split(
                            ',')
                        self.root.ids['make_test'].ids[
                            'quesNum'].text = f'Question No. {self.quesNumber}'
                        self.root.ids['make_test'].ids['ques'].text = ques
                        self.root.ids['make_test'].ids['a'].text = a
                        self.root.ids['make_test'].ids['b'].text = b
                        self.root.ids['make_test'].ids['c'].text = c
                        self.root.ids['make_test'].ids['d'].text = d
                    except:
                        self.btnPress = 0
                        self.root.ids['make_test'].ids[
                            'quesNum'].text = f'Question No. {self.quesNumber}'
                        self.root.ids['make_test'].ids['ques'].text = ''
                        self.root.ids['make_test'].ids['a'].text = ''
                        self.root.ids['make_test'].ids['b'].text = ''
                        self.root.ids['make_test'].ids['c'].text = ''
                        self.root.ids['make_test'].ids['d'].text = ''
                else:
                    self.showToast('Submit The Question first')
        else:
            self.showToast('Already on Last question')

    def previousQues(self):
        if self.quesNumber != 1:
            self.root.ids['make_test'].ids['submitbtn'].disabled = True
            self.quesNumber -= 1
            ques, a, b, c, d = self.quesOption[self.quesNumber - 1].split(',')
            self.root.ids['make_test'].ids['quesNum'].text = f'Question No. {self.quesNumber}'
            self.root.ids['make_test'].ids['ques'].text = ques
            self.root.ids['make_test'].ids['a'].text = a
            self.root.ids['make_test'].ids['b'].text = b
            self.root.ids['make_test'].ids['c'].text = c
            self.root.ids['make_test'].ids['d'].text = d
            anim = Animation(pos_hint={'top': -1}) + \
                Animation(pos_hint={'top': .88}, duration=1)
            anim.start(self.root.ids['make_test'].ids['test_card'])
        else:
            self.showToast('Already on first question')

    def quesSubmit(self):
        ques = self.root.ids['make_test'].ids['ques'].text
        a = self.root.ids['make_test'].ids['a'].text
        b = self.root.ids['make_test'].ids['b'].text
        c = self.root.ids['make_test'].ids['c'].text
        d = self.root.ids['make_test'].ids['d'].text
        if self.btnPress == 0:
            try:
                t1, t2, t3, t4, t5 = f"{ques},{a},{b},{c},{d}".split(',')
                self.quesOption.append(f"{ques},{a},{b},{c},{d}\n")
                self.btnPress = 1
                self.showToast("Question Submited")
                self.root.ids['make_test'].ids['submitbtn'].disabled = True
            except:
                self.showToast("You can't put (,) in Question and Options too")
        else:
            self.root.ids['make_test'].ids['submitbtn'].disabled = True

        if self.root.ids['make_test'].ids['submitbtn'].text == 'Final Submit':
            btnPressFinal = 1
            if btnPressFinal == 1:
                btnPressFinal = 1

                def dialog_callback(txt, obj):
                    if txt == 'Yes':
                        with open("test/"+self.root.ids['make_test'].ids['set_date'].text + " " + self.root.ids['make_test'].ids['test_name'].text + " " + self.root.ids['make_test'].ids['test_id'].text + ".mock", 'a') as create_test:
                            create_test.writelines(self.quesOption)
                        self.changeScreen('right', 'dashboard')
                        remove("test/"+self.root.ids['make_test'].ids['set_date'].text + " " + self.root.ids['make_test']
                               .ids['test_name'].text + " " + self.root.ids['make_test'].ids['test_id'].text + ".mock")
                dialog = MDDialog(
                    title='Final Submit', size_hint=(.8, .3), text_button_ok='Yes',
                    text="[b]If u want to Recheck the question then press Cancel rather than press ok[/b]",
                    text_button_cancel='Cancel',
                    events_callback=dialog_callback
                )
                dialog.open()

        if self.quesNumber == int(self.num_of_ques):
            btnPressFinal = 0
            self.root.ids['make_test'].ids['submitbtn'].disabled = False
            self.root.ids['make_test'].ids['submitbtn'].text = 'Final Submit'

    def searchResults(self):
        def chng(*args):
            if args[0] == datetime.datetime.now().date():
                self.root.ids['search_test'].ids['giveTest_sm'].current = 'Test'
            else:
                self.showToast("You only give this test on DATE:- " + args[0])

        try:
            for root_dir, folders, files in walk("exam"):
                if files != []:
                    for file in files:
                        if file.endswith('.mock'):
                            self.test_fileName = path.splitext(file)[0]
                            test_date, test_name, test_id = self.test_fileName.split(
                                ' ')
                            self.root.ids['search_test'].ids['search_options'].add_widget(
                                ThreeLineListItem(
                                    text=test_name,
                                    secondary_text="ID:- "+test_id,
                                    tertiary_text="Date:- "+test_date,
                                    on_release=partial(chng, test_date)
                                )
                            )

        except Exception as e:
            self.showToast(e)

    def pre_give_test(self):
        Animation(pos_hint={'top': .88}).start(
            self.root.ids['search_test'].ids['test_card'])
        self.second = 00
        with open("exam/"+self.test_fileName+".mock", 'r') as testFile:
            self.test_name, self.test_id, self.test_date, self.noOfQues, self.dur = testFile.readline().split(',')
            self.testQuestion = testFile.readlines()
        self.duration = divmod(int(self.dur), 60)
        self.minutes = self.duration[1]
        self.hours = self.duration[0]

        self.giveBtnPress = 0
        self.giveQuesNumber = 1
        self.userAnswer = ['' for i in range(int(self.noOfQues))]
        self.root.ids['search_test'].ids[
            'quesNum'].text = f'Question No. {self.giveQuesNumber}'
        self.event = Clock.schedule_interval(self.update_duration, 1)
        self.getQuestionOption('0')
        self.root.ids['search_test'].ids['submitbtn'].disabled = True

    def testNextQues(self):

        if self.giveQuesNumber != int(self.noOfQues):
            if self.userAnswer == ['' for i in range(int(self.noOfQues))]:
                self.showToast('Submit The Question first')
            else:
                if self.userAnswer[self.giveQuesNumber - 1] == '':
                    self.showToast("Submit the question first")

                else:
                    self.giveBtnPress = 1
                    if self.giveBtnPress == 1:
                        self.root.ids['search_test'].ids[self.opt].background_color = [
                            .98, .89, .78, .67]
                        anim = Animation(pos_hint={'top': -1}) + \
                            Animation(pos_hint={'top': .88}, duration=1)
                        anim.start(
                            self.root.ids['search_test'].ids['test_card'])
                        self.giveQuesNumber += 1
                        self.getQuestionOption(self.giveQuesNumber - 1)
                        self.root.ids['search_test'].ids[
                            'quesNum'].text = f'Question No. {self.giveQuesNumber}'
                        self.giveBtnPress = 0
        else:
            self.showToast('Already on Last question')

        try:
            for i in ['a', 'b', 'c', 'd']:
                if self.root.ids['search_test'].ids[str(i)].text != self.userAnswer[self.giveQuesNumber - 1]:
                    self.root.ids['search_test'].ids[str(
                        i)].background_color = [.98, .89, .78, .67]
                else:
                    self.root.ids['search_test'].ids[str(i)].background_color = [
                        0, 1, 1, 1]
        except:
            pass

    def testPreviousQues(self):

        for i in ['a', 'b', 'c', 'd']:
            if self.root.ids['search_test'].ids[i].text == self.userAnswer[self.giveQuesNumber - 1]:
                self.root.ids['search_test'].ids[i].background_color = [.98, .89, .78, .67]

        if self.giveQuesNumber != 1:
            self.root.ids['make_test'].ids['submitbtn'].disabled = False
            self.giveQuesNumber -= 1
            self.root.ids['search_test'].ids[
                'quesNum'].text = f'Question No. {self.giveQuesNumber}'
            self.getQuestionOption(self.giveQuesNumber - 1)
            anim = Animation(pos_hint={'top': -1}) + \
                Animation(pos_hint={'top': .88}, duration=1)
            anim.start(self.root.ids['search_test'].ids['test_card'])
        else:
            self.showToast('Already on first question')

        for i in list(('a', 'b', 'c', 'd')):
            if self.root.ids['search_test'].ids[i].text == self.userAnswer[self.giveQuesNumber - 1]:
                self.root.ids['search_test'].ids[i].background_color = [
                    0, 1, 1, 1]

    def giveQuesSubmit(self):
        ans = self.answer
        if self.giveBtnPress == 0:
            self.userAnswer[self.giveQuesNumber - 1] = ans + \
                ',' if self.noOfQues != self.giveQuesNumber else ans
            self.giveBtnPress = 1
            self.showToast("Question Submitted")
            self.root.ids['search_test'].ids['submitbtn'].disabled = True

        if self.giveQuesNumber == int(self.noOfQues):
            btnPressFinal = 0
            self.root.ids['search_test'].ids['submitbtn'].disabled = False
            self.root.ids['search_test'].ids['finalsubmitbtn'].disabled = False

    def giveFinalSubmit(self):
        def dialog_callback(txt, obj):
            if txt == 'Yes':
                move("exam/"+self.test_fileName+".mock", "results")
                with open('results/' + self.test_id + '.ans', 'w') as f:
                    f.writelines(self.userAnswer)

                self.root.ids['sm'].current = 'result'
        dialog = MDDialog(
            title='Final Submit', size_hint=(.8, .3), text_button_ok='Yes',
            text="[b]If u want to Recheck the question then press Cancel rather than press ok[/b]",
            text_button_cancel='Cancel',
            events_callback=dialog_callback
        )
        dialog.open()

    def answerCheck(self):
        score = 0
        for i in range(int(self.noOfQues)):
            test = self.testQuestion[i].split(',')
            self.root.ids['search_test'].ids['review_test'].add_widget(
                ThreeLineListItem(
                    text=test[0],
                    secondary_text="Your Answer:-       "+self.userAnswer[i],
                    tertiary_text="Correct Answer:-     "+test[1],
                )
            )
            if self.userAnswer[i] == test[1]:
                score = score + 1
        dialog = MDDialog(
            title="Result",
            size_hint=(.5, .3),
            text=str(score) + " marks out of " + self.noOfQues,
            auto_dismiss=False
        )
        dialog.open()

    def getQuestionOption(self, num):
        question, O1, O2, O3, O4 = self.testQuestion[int(num)].split(',')
        self.rightAnswer = []
        self.rightAnswer.append(O1)
        lst = [O1, O2, O3, O4[:-1]]
        shuffle(lst)
        self.root.ids['search_test'].ids['ques'].text = question
        self.root.ids['search_test'].ids['a'].text = lst[0]
        self.root.ids['search_test'].ids['b'].text = lst[1]
        self.root.ids['search_test'].ids['c'].text = lst[2]
        self.root.ids['search_test'].ids['d'].text = lst[3]

    def update_duration(self, instance):
        '''To update the timer'''
        if abs(int(self.hours)) == 0 and abs(int(self.minutes)) == 0 and abs(int(self.second)) == 0:
            self.root.ids['search_test'].ids['duration'].text = "TIME'S UP"

            def dialog_callback(*args):
                self.root.ids['search_test'].ids['giveTest_sm'].current = 'answer_check'
            dialog = MDDialog(
                title="Time' Up", size_hint=(.8, .3),
                text="[b]Press ok to submit the question.[/b]",
                auto_dismiss=False,
                events_callback=dialog_callback
            )
            dialog.open()
            Clock.unschedule(self.event)

        elif abs(int(self.hours)) >= 0:
            if abs(int(self.minutes)) >= 0:
                if self.second > 0:
                    self.root.ids['search_test'].ids[
                        'duration'].text = f'{abs(int(self.hours))}:{abs(int(self.minutes))}:{abs(int(self.second))}'
                    self.second -= 1
                elif self.second == 0 and abs(int(self.minutes)) > 0:
                    self.root.ids['search_test'].ids[
                        'duration'].text = f'{abs(int(self.hours))}:{abs(int(self.minutes))}:{abs(int(self.second))}'
                    self.second = 59
                    self.minutes -= 1
                elif self.minutes == 0 and self.hours > 0 and self.second == 0:
                    self.root.ids['search_test'].ids[
                        'duration'].text = f'{abs(int(self.hours))}:{abs(int(self.minutes))}:{abs(int(self.second))}'
                    self.minutes = 60
                    self.hours -= 1

    def optionCheck(self, opt):
        self.opt = opt

        self.answer = self.root.ids['search_test'].ids[self.opt].text

        if self.opt == 'a':
            self.root.ids['search_test'].ids['a'].background_color = [
                0, 1, 1, 1]
            self.root.ids['search_test'].ids['b'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['c'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['d'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['submitbtn'].disabled = False

        elif self.opt == 'b':
            self.root.ids['search_test'].ids['b'].background_color = [
                0, 1, 1, 1]
            self.root.ids['search_test'].ids['a'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['c'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['d'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['submitbtn'].disabled = False

        elif self.opt == 'c':
            self.root.ids['search_test'].ids['c'].background_color = [
                0, 1, 1, 1]
            self.root.ids['search_test'].ids['b'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['a'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['d'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['submitbtn'].disabled = False

        else:
            self.root.ids['search_test'].ids['d'].background_color = [
                0, 1, 1, 1]
            self.root.ids['search_test'].ids['b'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['c'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['a'].background_color = [.98, .89, .78, .67]
            self.root.ids['search_test'].ids['submitbtn'].disabled = False

    def results(self):
        from kivymd.uix.label import MDLabel
        for root_dir, folders, files in walk("results"):
            if files == []:
                self.root.ids['result'].ids['results'].add_widget(
                    MDLabel(
                        text='You not give any mock test yet',
                        halign='center'
                    )
                )
            else:
                for file in files:
                    if file.endswith('.mock'):
                        self.fileName = path.splitext(file)[0]
                        date, name, id = self.fileName.split(' ')
                        self.root.ids['result'].ids['results'].add_widget(
                            ThreeLineListItem(
                                text=name,
                                secondary_text="ID:- "+id,
                                tertiary_text="Date:- "+date,
                                on_release=partial(
                                    self.resultsCarousel, self.fileName)
                            )
                        )

    def resultsCarousel(self, *args):
        with open('results/' + args[0] + '.mock', 'r') as f:
            line = f.readline()
            qo = f.readlines()
            name, id, date, qn, t = line.split(',')
        with open('results/' + id + ".ans", 'r') as a:
            answers = a.readline().split(',')
            cq = 0
            wq = 0
            for i in range(int(qn)):
                ewai = qo[i].split(',')
                if ewai[1] == answers[i]:
                    cq += 1
                else:
                    wq += 1
        sm = self.root.ids['result'].ids['result_view']
        sm.current = 'view'
        self.root.ids['result'].ids['testName'].text = name
        self.root.ids['result'].ids['testID'].text = id
        self.root.ids['result'].ids['date'].text = date
        self.root.ids['result'].ids['AQ'].text = qn
        self.root.ids['result'].ids['CQ'].text = str(cq)
        self.root.ids['result'].ids['WQ'].text = str(wq)

        for i in range(int(qn)):
            ewai = qo[i].split(',')
            fl = MDFloatLayout()
            card = MDCard(
                pos_hint={'center_x': .5, 'center_y': .5},
                size_hint=(.9, .58),
                elevation=11
            )
            lb = MDLabel(
                text=ewai[0],
                halign='center',
                font_style='H6'
            )

            gl = MDGridLayout(
                cols=2
            )

            gl1 = MDGridLayout(
                cols=1,
                md_bg_color=[0, 1, 0, 1] if answers[i] == ewai[1] else [
                    1, 0, 0, 1]
            )

            lb1 = MDLabel(
                text="A:-   " + ewai[1],
                halign='center'
            )

            lb2 = MDLabel(
                text="B:-   " + ewai[2],
                halign='center'
            )

            lb3 = MDLabel(
                text="C:-   " + ewai[3],
                halign='center'
            )

            lb4 = MDLabel(
                text="D:-   " + ewai[4],
                halign='center'
            )

            lb5 = MDLabel(
                text="Your Option:-   " + answers[i],
                halign='center'
            )

            bl = MDBoxLayout(
                orientation='vertical'
            )

            fl.add_widget(card)
            card.add_widget(bl)
            bl.add_widget(lb)
            bl.add_widget(gl)
            gl.add_widget(lb1)
            gl.add_widget(lb2)
            gl.add_widget(lb3)
            gl.add_widget(lb4)
            bl.add_widget(gl1)
            gl1.add_widget(lb5)
            self.root.ids['result'].ids['carousel'].add_widget(fl)


if __name__ == "__main__":
    MainApp().run()
