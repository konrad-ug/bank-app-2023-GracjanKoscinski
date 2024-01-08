from behave import *
from selenium.webdriver.common.keys import Keys
import requests
from unittest_assertions import AssertEqual


assert_equal = AssertEqual()
URL = "http://localhost:5000"


@when('I create an account using imie: {name}, nazwisko: {last_name}, pesel: {pesel}')
def utworz_konto(context, name, last_name, pesel):
    json_body = { "imie": f"{name}",
    "nazwisko": f"{last_name}",
    "pesel": f"{pesel}"
    }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert_equal(create_resp.status_code, 201)

@step('Number of accounts in registry equals: "{count}"')
def sprawdz_liczbe_kont_w_rejestrze(context, count):
    ile_kont = requests.get(URL + f"/api/accounts/count")
    assert_equal(ile_kont.json()["count"], int(count))


@step('Account with pesel "{pesel}" exists in registry')
def sprawdz_czy_konto_z_pesel_istnieje(context, pesel):
    czy_istnieje = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(czy_istnieje.status_code, 200)
    #TODO assert czy konto z peselem istnieje


@step('Account with pesel "{pesel}" does not exists in registry')
def sprawdz_czy_konto_z_pesel_nie_istnieje(context, pesel):
    #TODO assert czy konto z peselem nie istnieje
    czy_istnieje = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(czy_istnieje.status_code, 404)

@when('I delete account with pesel: "{pesel}"')
def usun_konto(context, pesel):
    delete_resp = requests.delete(URL + f"/api/accounts/{pesel}")
    assert_equal(delete_resp.status_code, 200)


@when('I save the account registry')
def zapisz_konta(context):
    resp = requests.patch(URL  + f"/api/accounts/save")
    assert_equal(resp.status_code, 200)


@when('I load the account registry')
def load_rejestr(context):
    #TODO
    pass


@when('I update last name in account with pesel "{pesel}" to "{last_name}"')
def update_nazwiska(context, pesel, last_name):
    #TODO       
    pass


@then('Last name in account with pesel "{pesel}" is "{last_name}"')
def sprawdzenie_nazwiska(context, pesel, last_name):
    #TODO
    pass


