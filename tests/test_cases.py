
import random
import re
import time
#import asyncio
import pytest
import pytest_playwright
from playwright.sync_api import expect, Page




URL = "https://www.demoblaze.com/"
URL_CART = "https://www.demoblaze.com/cart.html"




def fill_in_login_form(browser: Page, username, password):
    browser.locator("#loginusername").click()
    browser.locator("#loginusername").fill(username)
    browser.locator("#loginpassword").click()
    browser.locator("#loginpassword").fill(password)
    


def fill_in_signup_form(browser: Page, username, password):
    browser.get_by_label("Username:").click()
    browser.get_by_label("Username:").fill(username)
    browser.get_by_label("Password:").click()
    browser.get_by_label("Password:").fill(password) 


def user_login(browser: Page, username, password):
    browser.get_by_role("link", name="Log in").click()
    fill_in_login_form(browser, username, password)
    browser.get_by_role("button", name="Log in").click()
    browser.get_by_text("Log out").wait_for()


def test_user_signup(browser: Page, before, password, generate_username):
    """verify sign up for new user"""

    browser.get_by_role("link", name="Sign up").click()
    fill_in_signup_form(browser, generate_username, password)
    with browser.expect_event("dialog") as event_info:
        dialog_messages = []
    
        def handle_dialog(dialog):
            dialog_messages.append(dialog.message)

            #time.sleep(2)
            dialog.accept()
        browser.on("dialog", handle_dialog)
    
        browser.get_by_role("button", name="Sign up").click()
    q=str(event_info.value)
    pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
    attributes = re.findall(pattern, q)

    # Creating a dictionary of attribute-value pairs
    parsed_data = {attr[0]: attr[1] or attr[2] for attr in attributes}

    expected_message = "Sign up successful."
    assert expected_message in dialog_messages
    


def test_signup_user_exist(browser: Page, username, password, before):
    """verify that impossible to sign up for existing user"""
    
    browser.get_by_role("link", name="Sign up").click()
    fill_in_signup_form(browser, username, password)
    with browser.expect_event("dialog") as event_info:
        dialog_messages = []
    
        def handle_dialog(dialog):
            dialog_messages.append(dialog.message)
            time.sleep(2)
            dialog.accept()
        browser.on("dialog", handle_dialog)
        browser.get_by_role("button", name="Sign up").click()
    q=str(event_info.value)
    pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
    attributes = re.findall(pattern, q)

    # Creating a dictionary of attribute-value pairs
    parsed_data = {attr[0]: attr[1] or attr[2] for attr in attributes}
    expected_message = "This user already exist."
    assert  expected_message in dialog_messages   
    


def test_user_login(browser: Page, username, password,before, after):
    """"verify log in """

    browser.get_by_role("link", name="Log in").click()
    fill_in_login_form(browser, username, password)
    browser.get_by_role("button", name="Log in").click()
    
    expected_btn = "Log out"
    expected_text = f"Welcome {username}"
    expect(browser.get_by_role("link").nth(5)).to_have_text(expected_btn)
    expect(browser.get_by_role("link").nth(6)).to_have_text(expected_text)



@pytest.mark.parametrize(
    "cos, username, password",
    [
        #empty
        ("empty","test", ""),
        #spesial symbols
        ("spec","@#$%^^&*()", "test"),
        #incorrect password
        ("incorect","test", "password"),
    ],
)
def test_user_login_with_icorrect_credentials(browser: Page, username, password, cos, before):
    """verify unsuccessful login and related messages"""
    
    browser.get_by_role("link", name="Log in").click()
    fill_in_login_form(browser, username, password)
    with browser.expect_event("dialog") as event_info:
        dialog_messages = []
    
        def handle_dialog(dialog):
            dialog_messages.append(dialog.message)
            time.sleep(2)
            dialog.accept()
        browser.on("dialog", handle_dialog)
        browser.get_by_role("button", name="Log in").click()
    q=str(event_info.value)
    pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
    attributes = re.findall(pattern, q)

    # Creating a dictionary of attribute-value pairs
    parsed_data = {attr[0]: attr[1] or attr[2] for attr in attributes}
    
    time.sleep(2)
    if cos == "incorect":
        assert "Wrong password." in dialog_messages
    elif cos == "empty":  
        assert "Please fill out Username and Password." in dialog_messages
    else:
        assert "User does not exist." in dialog_messages  
        
    expect(browser.get_by_role("link").nth(6)).to_have_text("Sign up")
    

def add_item_to_cart(browser, id=None):
        xpath_product=f"//a[@class='hrefch' and @href='prod.html?idp_={id}']"
        with browser.expect_navigation(url=re.compile(URL + re.escape(f"prod.html?idp_={id}"))): 
            browser.locator("#tbodyid").locator(xpath_product).click()
        browser.on("dialog", lambda dialog: dialog.accept())
        browser.get_by_role("link", name="Add to cart").click()
        time.sleep(1)        
        browser.goto(URL)
        time.sleep(1)    
        
        

def get_product_name(browser, id=None):
    xpath_product=f"//a[@class='hrefch' and @href='prod.html?idp_={id}']"
    return browser.locator("#tbodyid").locator(xpath_product).inner_text()


def check_count_of_items_cart(browser):
    table_rows = browser.get_by_role("table").locator('//tr[@class="success"]')
    time.sleep(1)
    return(table_rows.count())


def check_total_sum(browser):
    table_rows = browser.get_by_role("table").locator('//tr[@class="success"]')
    
    total_price = 0
    for row in table_rows.all():
        cells1=row.locator('td').nth(2)
        for cell in cells1.all():
            price=int(cell.text_content())
            total_price += price
    return(total_price)


def delete_first_item_from_cart(browser):
    table_rows = browser.get_by_role("table").locator('//tr[@class="success"]')
    if check_count_of_items_cart(browser) > 0:
        for row in table_rows.all():
            row.locator('td').nth(3).get_by_role("link", name="Delete").click()
            break       
    else:
        print("No items")        



def delete_all_items_from_cart(browser):
    table_rows = browser.get_by_role("table").locator('//tr[@class="success"]')
    if check_count_of_items_cart(browser) > 0:
        for row in table_rows.all():
            row.locator('td').nth(3).get_by_role("link", name="Delete").click()
            time.sleep(1)     
    else:
        print("No items")


@pytest.mark.parametrize("n_item", [1, 5])
def test_add_items_into_cart(browser: Page, username, password, n_item, before):
    """ verify adding one and five items"""

    user_login(browser, username, password)
    # check how meny items in the cart
    browser.goto(url=URL_CART, wait_until='domcontentloaded')
    time.sleep(2)
    count_of_item_before = check_count_of_items_cart(browser)
    
    # navigate to the main page
    browser.goto(url=URL, wait_until='domcontentloaded')
    expect(browser).to_have_url(URL)
    # go to categories
    product_list = browser.locator("#tbodyid")
    product_list.wait_for()
    expect(product_list).to_be_visible()
    
    # add few items
    for _ in range(n_item):
        i = random.randint(1, 9)
        add_item_to_cart(browser, i)
        print("Added product: " + str(i))

    with browser.expect_navigation(url=re.compile(".*/cart.html.*")):
        browser.get_by_role("link", name="Cart", exact=True).click()
    expect(browser).to_have_url(URL +"cart.html")
    
    cart_list = browser.get_by_role("table")
    expect(cart_list).to_be_visible()
    # verify that total items in the cart to be increased
    expect(cart_list.locator('//tr[@class="success"]')).to_have_count(count_of_item_before + n_item)
    

def test_price_items_into_cart(browser: Page, username, password, before):
    
    user_login(browser, username, password)
    browser.goto(url=URL_CART, wait_until='domcontentloaded')
    delete_first_item_from_cart(browser)
    time.sleep(1)
    total_price_showed = browser.locator("#totalp")
    total_price_showed = total_price_showed.inner_text()
    if check_count_of_items_cart(browser)>0:
        total_price_calc = check_total_sum(browser)
        # verify that total price correct
        assert total_price_calc == int(total_price_showed)
    else:
        assert not total_price_showed
    


def fill_place_order_form(browser, name, card):
    browser.locator("#name").click()
    browser.locator("#name").fill(name)
    browser.get_by_label("Country:").click()
    browser.get_by_label("Country:").fill("country")
    browser.get_by_label("City:").click()
    browser.get_by_label("City:").fill("city")
    browser.get_by_label("Credit card:").click()
    browser.get_by_label("Credit card:").fill(card)
    browser.get_by_label("Month:").click()
    browser.get_by_label("Month:").fill("mm")
    browser.get_by_label("Year:").click()
    browser.get_by_label("Year:").fill("yyyy")



def test_place_order(browser: Page, username, password, before, name="test order", card="card"):

    user_login(browser, username, password)
    browser.goto(url=URL_CART, wait_until='networkidle')
    btn_place_order = browser.get_by_role("button", name="Place Order")
    expect(btn_place_order).to_be_enabled()

    btn_place_order.click()
    place_order_form =browser.locator("#orderModal")
    expect(place_order_form).to_be_visible()
    #fill in place order form
    fill_place_order_form(browser,name, card)
    btn_on_place_order_form = place_order_form.get_by_role("button", name="Purchase")
    expect(btn_on_place_order_form).to_be_enabled()
    btn_on_place_order_form.click()

    alert = browser.locator("//div[starts-with(@class,'sweet-alert')]")
    expect(alert).to_be_visible()
    message = alert.locator("h2")
    expect(message).to_contain_text("Thank you for your purchase!")
    btn_confirm = alert.get_by_role("button", name="OK")
    with browser.expect_navigation(url=re.compile(URL +"index.html")):
        with browser.expect_navigation(url=re.compile(URL +"index.html")):
            btn_confirm.click()
            expect(alert).not_to_be_visible()
            expect(place_order_form).not_to_be_visible()
    #rediraction to main page    
    expect(browser).to_have_url(URL +"index.html")
    


@pytest.mark.parametrize(
    "name, card",
    [
        #empty card
        ("test order", ""),
        #empty name
        ("", "card"),
    ],
)
def test_fill_place_order_form_incorrect(browser: Page, name, card, username, password, before):
    """verify that a message about non filling fields will be displayed"""

    user_login(browser, username, password)
    browser.goto(url=URL_CART, wait_until='networkidle')
    btn_place_order = browser.get_by_role("button", name="Place Order")
    expect(btn_place_order).to_be_enabled()

    btn_place_order.click()
    place_order_form =browser.locator("#orderModal")
    expect(place_order_form).to_be_visible()
    #fill in place order form
    fill_place_order_form(browser,name, card)
    btn_on_place_order_form = place_order_form.get_by_role("button", name="Purchase")
    expect(btn_on_place_order_form).to_be_enabled()
    dialog_messages = []
    
    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        time.sleep(2)
        dialog.accept()
    browser.on("dialog", handle_dialog)
    btn_on_place_order_form.click()
    assert  "Please fill out Name and Creditcard." in dialog_messages 
   

