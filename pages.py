from playwright.sync_api import Page, expect


class MainPage:
    URL = "https://regoffice.senla.eu/"

    def __init__(self, page: Page):
        self.page = page

        # Заголовки
        self.title = page.locator("h2", has_text="Вас приветствует ЗАГС!")
        self.subtitle = page.locator("p", has_text="Выберите режим входа:")

        # Кнопки
        self.user_button = page.get_by_role("button", name="Войти как пользователь", exact=True)
        self.admin_button = page.get_by_role("button", name="Войти как администратор", exact=True)
        self.certificate_button = page.get_by_role("button", name="Заказать справку", exact=True)

    def open(self):
        self.page.goto(self.URL)
        return self

    def should_be_opened(self):
        expect(self.title).to_be_visible()
        expect(self.subtitle).to_be_visible()
        expect(self.user_button).to_be_visible()
        expect(self.admin_button).to_be_visible()
        expect(self.certificate_button).to_be_visible()

    def click_user(self):
        self.user_button.click()
        return UserForm(self.page)

    # def click_admin(self):
    #     self.admin_button.click()
    #     return AdminForm(self.page)
    #
    # def click_certificate(self):
    #     self.certificate_button.click()
    #     return CertificateForm(self.page)


class UserForm:

    def __init__(self, page: Page):
        self.page = page

        # Поля формы
        self.surname = page.get_by_placeholder("Введите фамилию (минимум 2 символа)")
        self.name = page.get_by_placeholder("Введите имя (минимум 2 символа)")
        self.middle_name = page.get_by_placeholder("Введите отчество (минимум 5 символов)")
        self.phone_number = page.get_by_placeholder("Введите номер телефона (не более 11 символов)")
        self.passport = page.get_by_placeholder("Введите номер паспорта (не более 8 символов)")
        self.address = page.get_by_placeholder("Введите адрес прописки")

        # Кнопки

        self.close_button = page.get_by_role("button", name="Закрыть", exact=True)
        self.accept_button = page.get_by_role("button", name="Далее", exact=True)

        # Успех заполнения формы
        self.success_mark = page.get_by_test_id("CheckCircleIcon")

    def fill_user_form(self, surname: str, name: str, middle_name: str, phone_number: str, passport: str, address: str):
        self.surname.fill(surname)
        self.name.fill(name)
        self.middle_name.fill(middle_name)
        self.phone_number.fill(phone_number)
        self.passport.fill(passport)
        self.address.fill(address)
        return self

    def to_accept_form(self):
        self.accept_button.click()
        return UserChoicePage(self.page)

    def to_close_button(self):
        self.close_button.click()
        return self

class UserChoicePage:
    def __init__(self, page: Page):

        self.page = page

        self.choose_marriage_button = page.get_by_role("button", name="Регистрация брака", exact=True)
        self.choose_birth_button = page.get_by_role("button", name="Регистрация рождения", exact=True)
        self.choose_death_button = page.get_by_role("button", name="Регистрация смерти", exact=True)

        self.return_button = page.get_by_role("button", name="Назад", exact=True)
        self.close_button =  page.get_by_role("button", name="Закрыть", exact=True)

    def user_choice_page_should_be_opened(self):
        expect(self.choose_marriage_button).to_be_visible()
        expect(self.choose_birth_button).to_be_visible()
        expect(self.choose_death_button).to_be_visible()

    def chose_marriage(self):
        self.choose_marriage_button.click()
        return CitizenForm(self.page)
    def choose_birth(self):
        self.choose_birth_button.click()
        return self

    def choose_death(self):
        self.choose_death_button.click()
        return self

    def to_return_to_user(self):
        self.return_button.click()
        return UserForm(self.page)


class CitizenForm:

    def __init__(self, page: Page):
        self.page = page

        self.citizen_surname = page.get_by_label("Фамилия *", exact=True)
        self.citizen_name = page.get_by_label("Имя *", exact=True)
        self.citizen_middle_name = page.get_by_label("Отчество *", exact=True)
        self.citizen_birth_date = page.get_by_label("Дата рождения *", exact=True)
        self.citizen_passport = page.get_by_label("Номер паспорта", exact=True)
        self.citizen_sex = page.get_by_label("Пол *", exact=True)
        self.citizen_address = page.get_by_label("Адрес прописки *", exact=True)

        self.subtitle = page.locator("span").get_by_text("Вы выбрали услугу: Регистрация брака", exact=True)
        self.return_button = page.get_by_role("button", name="Назад", exact=True)
        self.close_button = page.get_by_role("button", name="Закрыть", exact=True)
        self.accept_button = page.get_by_role("button", name="Далее", exact=True)


    def fill_citizen_form(self, citizen_surname: str, citizen_name: str, citizen_middle_name: str, citizen_birth_date: str, citizen_passport: str, citizen_sex: str, citizen_address: str):
        self.citizen_surname.fill(citizen_surname)
        self.citizen_name.fill(citizen_name)
        self.citizen_middle_name.fill(citizen_middle_name)
        self.citizen_birth_date.press_sequentially(citizen_birth_date, delay=20)
        self.citizen_passport.fill(citizen_passport)
        self.citizen_sex.fill(citizen_sex)
        self.citizen_address.fill(citizen_address)
        return self

    def return_button(self):
        self.close_button.click()
        return self

    def to_accept_form(self):
        self.accept_button.click()
        return ServiceMarriageFormPage(self.page)

    def to_return_to_user_choice_page(self):
        self.return_button.click()
        return UserChoicePage(self.page)

class ServiceMarriageFormPage:
    def __init__(self, page: Page):
        self.page = page

        self.marriage_date_of_reg = page.get_by_label("Дата регистрации *", exact=True)
        self.marriage_new_surname = page.get_by_label("Новая фамилия", exact=True)
        self.marriage_spouse_surname = page.get_by_label("Фамилия супруга/и *", exact=True)
        self.marriage_spouse_name = page.get_by_label("Имя супруга/и *", exact=True)
        self.marriage_spouse_middle_name = page.get_by_label("Отчество супруга/и *", exact=True)
        self.marriage_spouse_birthday = page.get_by_label("Дата рождения супруга/и", exact=True)
        self.marriage_spouse_passport = page.get_by_label("Номер паспорта супруга/и *", exact=True)

        self.marriage_form_close_btn = page.get_by_role("button", name="Закрыть", exact=True)
        self.marriage_form_return_btn = page.get_by_role("button", name="Назад", exact=True)
        self.marriage_form_end_btn = page.get_by_role("button", name="Завершить", exact=True)


    def marriage_spouse_form_fill(self, marriage_date_of_reg: str, marriage_new_surname: str, marriage_spouse_surname: str, marriage_spouse_name: str, marriage_spouse_middle_name: str, marriage_spouse_birthday: str, marriage_spouse_passport: str):

        self.marriage_date_of_reg.press_sequentially(marriage_date_of_reg, delay=20)
        self.marriage_new_surname.fill(marriage_new_surname)
        self.marriage_spouse_surname.fill(marriage_spouse_surname)
        self.marriage_spouse_name.fill(marriage_spouse_name)
        self.marriage_spouse_middle_name.fill(marriage_spouse_middle_name)
        self.marriage_spouse_birthday.press_sequentially(marriage_spouse_birthday, delay=20)
        self.marriage_spouse_passport.fill(marriage_spouse_passport)
        return self

    def to_close_marriage_page(self):
        self.marriage_form_close_btn.click()
        return self

    def to_return_to_user_choice_page(self):
        self.marriage_form_return_btn.click()
        return UserChoicePage(self.page)

    def to_accept_marriage_form(self):
        self.marriage_form_end_btn.click()
        return self

class FinalMarriagePage:
    def __init__(self, page: Page):
        self.page = page

        self.success_header_marriage = page.locator("span").get_by_text("Спасибо за обращение")
        self.status_of_marriage_request = page.locator("span").get_by_text("Статус заявки: На рассмотрении.")

        self.update_button_marriage = page.get_by_role("button", name="Обновить")
        self.new_request_button_marriage = page.get_by_role("button", name="Создать новую заявку")
        self.close_button_marriage = page.get_by_role("button", name="Закрыть")

    def to_create_new_request(self):
        self.new_request_button_marriage.click()
        return UserForm(self.page)

    def to_close_marriage_form(self):
        self.close_button_marriage.click()
        return MainPage(self.page)









