from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
import time

sim_type = input("Enter SIM type Physical(p) & eSIM(e), (p/e): ").strip().lower()
selected_carrier_name = ""  #  To be set after carrier selection

options = Options()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
driver.maximize_window()

driver.get("https://demo-linkupmobile.telgoo5.com/index.php")

# Step 1: Login
driver.find_element(By.NAME, "login_user_id").send_keys("qtglinkupmobile11")
driver.find_element(By.NAME, "passwd").send_keys("aap!)cP15&X12")
driver.find_element(By.ID, "submit_button").click()


time.sleep(4)
if sim_type == "p":
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Inventory')]"))).click()

    try:
        # Try to find "Manage Inventory" directly
        manage_inventory_link = driver.find_element(By.XPATH, "//a[contains(., 'Manage Inventory')]")
    except:
        # If not found, expand menu first
        try:
            expand_icon = driver.find_element(By.XPATH, "//i[contains(@class, 'fa-circle-o')]")
            expand_icon.click()
            time.sleep(1)
        except:
            print(" Expand icon not found or already expanded.")

    # Now wait for the link and click it
    try:
        manage_inventory_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Manage Inventory')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", manage_inventory_link)
        driver.execute_script("arguments[0].click();", manage_inventory_link)
        print("✅ Clicked 'Manage Inventory'")
    except:
        print("❌ Failed to click 'Manage Inventory'")

    #addsingleunit
    switch_buttons = driver.find_elements(By.XPATH, "//span[contains(@class, 'swithOldNew')]")
    if switch_buttons and switch_buttons[0].is_displayed():
        switch_buttons[0].click()
        print("✅ Switched to New View")
    else:
        print("✅ Already in New View or switch button not visible")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add Single Unit')]"))).click()

    # Carrier selection
    carrier_dropdown = wait.until(EC.presence_of_element_located((By.ID, "carrier")))
    select = Select(carrier_dropdown)
    wait.until(lambda d: len(select.options) > 0)

    carrier_options = select.options
    carrier_names = [option.text.strip() for option in carrier_options]

    if len(carrier_options) == 1:
        selected_carrier_name = carrier_names[0]
        print(f" Only one carrier found: {selected_carrier_name}. Auto-selected.")
    else:
        print("Available carriers:")
        for idx, name in enumerate(carrier_names, start=1):
            print(f"{idx}. {name}")

        while True:
            try:
                choice = int(input("Enter carrier number to select: "))
                if 1 <= choice <= len(carrier_names):
                    select.select_by_visible_text(carrier_options[choice - 1].text)
                    selected_carrier_name = carrier_names[choice - 1]  #  Set carrier name
                    break
                else:
                    print(" Invalid choice. Try again.")
            except ValueError:
                print(" Please enter a valid number.")

    # SIM + IMEI
    sim_number = '8' + ''.join([str(random.randint(0, 9)) for _ in range(19)])
    driver.find_element(By.ID, "esn").send_keys(sim_number)
    imei_number = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    driver.find_element(By.ID, "imei").send_keys(imei_number)

    # Assign Employee
    assign_select = Select(wait.until(EC.presence_of_element_located((By.ID, "assign_user"))))
    assign_select.select_by_visible_text("Employee")

    agent_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "agen_type")))
    agent_select = Select(agent_dropdown_element)

    wait.until(lambda d: len(agent_select.options) > 1)
    agent_options = [opt.text.strip() for opt in agent_select.options if "--Select--" not in opt.text and opt.text.strip() != ""]

    print("Available Employees:")
    for i, name in enumerate(agent_options, start=1):
        print(f"{i}. {name}")

    while True:
        try:
            agent_choice = int(input("Enter the number of the employee to assign SIM to: "))
            if 1 <= agent_choice <= len(agent_options):
                break
            else:
                print("❌ Invalid choice. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

    agent_select.select_by_visible_text(agent_options[agent_choice - 1])

    # Select Product "SIM SIM"
    wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Product Name')]/following::span[contains(@class,'select2-selection--single')][1]"))).click()
    time.sleep(1)
    search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'select2-search__field')]")))
    search_input.send_keys("SIM SIM")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'SIM SIM')]"))).click()

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-save"))).click()
    print(" SIM saved in inventory successfully!")

else:
    sim_number = None  # eSIM: auto populated later

input("\n Verify SIM in UI and press Enter to proceed with Port-in flow...")


# Step 2: Click search and open advance search
wait.until(EC.element_to_be_clickable((By.NAME, "search"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "advance_search"))).click()

# Step 3: Wait for dropdown to be clickable
status_dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "acc_status")))
Select(status_dropdown_element).select_by_visible_text("Active")

# Step 4: Select carrier
time.sleep(2)
carrier_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "carrier_search")))
select = Select(carrier_dropdown)
wait.until(lambda d: len(select.options) > 0)

carrier_options = select.options
carrier_names = [option.text.strip() for option in carrier_options]

if len(carrier_options) == 1:
    selected_carrier_name = carrier_names[0]
    print(f"Only one carrier found: {selected_carrier_name}. Auto-selected.")
else:
    print("Available carriers:")
    for idx, name in enumerate(carrier_names, start=1):
        print(f"{idx}. {name}")
    while True:
        try:
            choice = int(input("Enter carrier number to select: "))
            if 1 <= choice <= len(carrier_names):
                select.select_by_visible_text(carrier_options[choice - 1].text)
                selected_carrier_name = carrier_names[choice - 1]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# Step 5: Click Search
time.sleep(2)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
    "#advsearchform > div.modal-footer > div.col-md-3 > button"))).click()

# Step 6: Wait for customer rows and click a random one
rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.allcustomerrow")))
random_row = random.choice(rows)
driver.execute_script("arguments[0].scrollIntoView(true);", random_row)
random_row.click()

time.sleep(5)
# Wait for the Port-in link to appear directly
# Wait for Quick Links panel to appear

# Step: Scroll the full page slowly to allow lazy-loaded elements to appear
for _ in range(5):
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

# Step: Look for all quick link anchors and match exact visible text
quick_links = driver.find_elements(By.XPATH, "//ul[contains(@class,'quk_links')]//a")

for link in quick_links:
    link_text = link.text.strip().lower()
    if "existing subscriber portin" in link_text:
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", link)
        print("✅ Clicked 'Existing subscriber portin'")
        break
else:
    print("❌ Link with text 'Existing subscriber portin' not found.")
# Locate link using partial href instead of text

time.sleep(5)
esn_field = wait.until(EC.presence_of_element_located((By.ID, "new_esn")))
esn_field.send_keys(sim_number)
esn_field.send_keys(Keys.TAB)

time.sleep(4)

plan_dropdown = wait.until(EC.presence_of_element_located((By.ID, "customr_state_plan")))
plan_select = Select(plan_dropdown)
plans = [opt.text for opt in plan_select.options[1:]]
for i, p in enumerate(plans, start=1):
    print(f"{i}. {p}")
plan_choice = int(input("Select plan number: "))
plan_select.select_by_visible_text(plans[plan_choice - 1])

time.sleep(3)
imei = wait.until(EC.visibility_of_element_located((By.NAME,"imei"))).send_keys("353936443654312")

time.sleep(3)
# Step 1: Get the MDN from top header
mdn_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mdn-grn")))
mdn_text = mdn_element.text  # Example: "MDN 8899669996"

# Step 2: Extract number from text
mdn_number = mdn_text.split("MDN")[1].strip()  # "8899669996"

# Step 3: Fill into 'Number to port' input field
port_field = wait.until(EC.presence_of_element_located((By.ID, "port_number")))
port_field.clear()
port_field.send_keys(mdn_number)

print(f"✅ Auto-filled MDN {mdn_number} into Number to port field")

time.sleep(2)

account_no = wait.until(EC.presence_of_element_located((By.ID,"ACNUMBER"))).send_keys("1234")

account_pass = wait.until(EC.presence_of_element_located((By.ID,"PASSWORDPIN"))).send_keys("4321")

Swap_type = wait.until(EC.presence_of_element_located((By.ID, "portin_swap_type")))

Swap_select = Select(Swap_type)

Swap_select.select_by_visible_text("Complete swap as soon as port-in completes")

time.sleep(3)
wait.until(EC.element_to_be_clickable((By.NAME, "searchfax"))).click()

time.sleep(10)
driver.quit()
