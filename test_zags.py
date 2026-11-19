from playwright.sync_api import Page, expect

from conftest import marriage_form_data
from pages import MainPage, UserChoicePage, ServiceMarriageFormPage, CitizenForm, FinalMarriagePage


def test_main_page_open(page: Page):
    main = MainPage(page).open()
    main.should_be_opened()

def test_user_form_fill_for_marriage_registration(page, user_form_data, citizen_form_data, marriage_form_data,
                                                  ):
    main = MainPage(page).open()
    user_form = main.click_user()
    expect(user_form.success_mark).to_have_count(0)
    expect(user_form.accept_button).to_be_disabled()
    user_form.fill_user_form(**user_form_data)
    expect(user_form.accept_button).to_be_enabled()
    user_form.to_accept_form()
    expect(user_form.success_mark).to_have_count(1)

    # Открылась страница выбора типа заявки

    user_choice_page = UserChoicePage(page)
    user_choice_page.user_choice_page_should_be_opened()
    expect(user_choice_page.choose_birth_button).to_be_visible()
    expect(user_choice_page.choose_death_button).to_be_visible()
    expect(user_choice_page.choose_marriage_button).to_be_visible()
    expect(user_choice_page.return_button).to_be_visible()
    expect(user_choice_page.close_button).to_be_visible()
    user_choice_page.chose_marriage()

    # Открылась форма заполнения данных о гражданине

    citizen_data_form = CitizenForm(page)
    expect(user_form.success_mark).to_have_count(2)
    expect(citizen_data_form.subtitle).to_be_visible()
    citizen_data_form.fill_citizen_form(**citizen_form_data)
    expect(citizen_data_form.accept_button).to_be_enabled()
    citizen_data_form.to_accept_form()

    # Открылась страница услуги

    marriage_data_form = ServiceMarriageFormPage(page)
    expect(user_form.success_mark).to_have_count(3)
    marriage_data_form.marriage_spouse_form_fill(**marriage_form_data)
    marriage_data_form.to_accept_marriage_form()
    expect(user_form.success_mark).to_have_count(5)

    # Открылась финальная форма

    final_marriage_page = FinalMarriagePage(page)
    expect(final_marriage_page.success_header_marriage).to_be_enabled()
    expect(final_marriage_page.close_button_marriage).to_be_enabled()
    expect(final_marriage_page.new_request_button_marriage).to_be_enabled()
    final_marriage_page.to_close_marriage_form()
    main.should_be_opened()



















