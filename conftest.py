from datetime import date

import pytest
from faker import Faker
from playwright.sync_api import sync_playwright



@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            http_credentials={
                "username": "user",
                "password": "senlatest",
            }
        )
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def fake():
    f = Faker("ru_Ru")
    return f


@pytest.fixture
def user_form_data(fake):
    return {
        "surname": fake.last_name(),
        "name": fake.first_name(),
        "middle_name": fake.middle_name(),
        "phone_number": fake.numerify("+7##########"),
        "passport": fake.numerify("######"),
        "address": fake.street_address()
    }

@pytest.fixture
def citizen_form_data(fake):
    return {
        "citizen_surname": fake.last_name(),
        "citizen_name": fake.first_name(),
        "citizen_middle_name": fake.middle_name(),
        "citizen_birth_date": fake.date_of_birth(minimum_age=18, maximum_age=100).strftime("%d/%m/%Y"),
        "citizen_passport": fake.numerify("######"),
        "citizen_sex": fake.random_element(["Муж", "Жен"]),
        "citizen_address": fake.street_address()
    }

@pytest.fixture
def marriage_form_data(fake):
    return {
        "marriage_date_of_reg": date.today().strftime("%d/%m/%Y"),
        "marriage_new_surname": fake.last_name(),
        "marriage_spouse_surname": fake.last_name(),
        "marriage_spouse_name": fake.first_name(),
        "marriage_spouse_middle_name": fake.middle_name(),
        "marriage_spouse_birthday": fake.date_of_birth(minimum_age=18, maximum_age=100).strftime("%d/%m/%Y"),
        "marriage_spouse_passport": fake.numerify("######")
    }