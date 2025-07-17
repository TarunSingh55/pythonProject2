from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

# Get SIM type
sim_type = input("Enter SIM type Physical(p) & eSIM(e), (p/e): ").strip().lower()
selected_carrier_name = ""  #  To be set after carrier selection

# Setup
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.maximize_window()
print("hello")
print("hello")

# Login
driver.get("https://dev-linkupmobile.telgoo5.com/index.php")
driver.find_element(By.NAME, "login_user_id").send_keys("qtglinkupmobile11")
driver.find_element(By.NAME, "passwd").send_keys("aap!)cP15&X12")
driver.find_element(By.ID, "submit_button").click()
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sidebar-menu")))

# ---------- Inventory Flow (Only for Physical SIM) ----------
if sim_type == "p":
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Inventory')]"))).click()

    # Step: Find and click 'Manage Inventory' with fallback
    try:
        # Step 1: Get all menu links first
        all_links = driver.find_elements(By.TAG_NAME, "a")

        for link in all_links:
            if "Manage Inventory" in link.text:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable(link)).click()
                print(" Clicked 'Manage Inventory'")
                break
        else:
            print("Manage Inventory' link not found in link list")

    except Exception as e:
        print(f"Final fail to click 'Manage Inventory': {e}")

    #switch inventory to new view
    switch_buttons = driver.find_elements(By.XPATH, "//span[contains(@class, 'swithOldNew')]")
    if switch_buttons and switch_buttons[0].is_displayed():
        switch_buttons[0].click()
        print("Switched to New View")
    else:
        print("Already in New View or switch button not visible")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add Single Unit')]"))).click()

    # Carrier selection
    carrier_dropdown = wait.until(EC.presence_of_element_located((By.ID, "carrier")))
    select = Select(carrier_dropdown)
    wait.until(lambda d: len(select.options) > 0)

    #  Filter out options like "--Select Carrier--"
    carrier_options = [
        option for option in select.options
        if option.text.strip() and not option.text.strip().lower().startswith('--select')
    ]

    carrier_names = [option.text.strip() for option in carrier_options]

    if len(carrier_options) == 1:
        selected_carrier_name = carrier_names[0]
        select.select_by_visible_text(selected_carrier_name)
        print(f"Only one carrier found: {selected_carrier_name}. Auto-selected.")
    else:
        print("Available carriers:")
        for idx, name in enumerate(carrier_names, start=1):
            print(f"{idx}. {name}")

        while True:
            try:
                choice = int(input("Enter carrier number to select: "))
                if 1 <= choice <= len(carrier_names):
                    selected_option = carrier_options[choice - 1]
                    select.select_by_visible_text(selected_option.text)
                    selected_carrier_name = selected_option.text.strip()
                    print(f"Selected carrier: {selected_carrier_name}")
                    break
                else:
                    print(" Invalid choice. Try again.")
            except ValueError:
                print(" Please enter a valid number.")

    # SIM + IMEI
    sim_number = '8' + ''.join([str(random.randint(0, 9)) for _ in range(19)])
    driver.find_element(By.ID, "esn").send_keys(sim_number)
    imei_number = ''.join([str(random.randint(3, 9)) for _ in range(15)])
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
                print(" Invalid choice. Try again.")
        except ValueError:
            print(" Please enter a valid number.")

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

# ---------- Port-in Flow ----------
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Prepaid/postpaid orders')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'enrollment_nll_step1')]"))).click()

wait.until(EC.presence_of_element_located((By.NAME, "zip_code"))).send_keys("98104")
wait.until(EC.presence_of_element_located((By.ID, "fname"))).send_keys("TEST")
wait.until(EC.presence_of_element_located((By.ID, "lastname"))).send_keys("TEST")
wait.until(EC.presence_of_element_located((By.NAME, "trad_address_main"))).send_keys("123 MAIN STRRN")
wait.until(EC.presence_of_element_located((By.NAME, "un_d_address_main"))).send_keys("123 MAIN STRRN")
email = f"test{random.randint(1000,9999)}@gmail.com"
wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)

#--------------plan selection for portin--------------------
plan_dropdown = wait.until(EC.presence_of_element_located((By.ID, "plan")))
plan_select = Select(plan_dropdown)
plans = [opt.text for opt in plan_select.options[1:]]
for i, p in enumerate(plans, start=1):
    print(f"{i}. {p}")
plan_choice = int(input("Select plan number: "))
plan_select.select_by_visible_text(plans[plan_choice - 1])

wait.until(EC.element_to_be_clickable((By.ID, "submit1"))).click()

#-----------Port in option selection------------
try:
    print(" Trying dev-style dropdown...")
    shipment_select = Select(wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'shipment_method')]"))
    ))
    shipment_select.select_by_visible_text("Port in- customer has a sim and can give its information. (PC251)")
    print(" Selected enrollment on DEV server")
except (TimeoutException, NoSuchElementException):
    try:
        # If not found, try DEMO server dropdown
        print("Trying demo-style dropdown...")
        enrollment_type = wait.until(
            EC.presence_of_element_located((By.NAME, "shipment_method_new[]"))
        )
        enrollment_select = Select(enrollment_type)
        enrollment_select.select_by_visible_text("Port In- Customer has a SIM and can give its information. (PC251)")
        print(" Selected enrollment on DEMO server")
    except Exception as e:
        print(" Failed to select enrollment method on both servers:", str(e))

wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'porting_number')]"))).send_keys("1502925616")

#------ flow for esim checkbox-----------
if sim_type == "e":
    esim_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@id, 'is_ESIM')]")))
    esim_checkbox.click()
    print(" eSIM checkbox clicked.")
else:
    esn_field = wait.until(EC.presence_of_element_located((By.NAME, "esn_new[]")))
    esn_field.send_keys(sim_number)
    time.sleep(2)
    esn_field.send_keys(Keys.TAB)

time.sleep(2)

#----------- esim portin flow------------
if sim_type == "e":
    time.sleep(5)
    carrier_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "carrier[]")))
    select = Select(carrier_dropdown)
    wait.until(lambda d: len(select.options) > 0)

    carrier_options = [option for option in select.options if option.text.strip() != "Select Carrier"]
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
                    selected_carrier_name = carrier_names[choice - 1]  #  Set name
                    break
                else:
                    print(" Invalid choice. Try again.")
            except ValueError:
                print(" Please enter a valid number.")

# ------------ esim device------------------------
time.sleep(3)
if sim_type == "e":
    device_id = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control.device_cls")))
    device_id.send_keys("351553464102717")

# Mandatory street type check for BLUECONNECTSATT
if selected_carrier_name.strip().upper() in ("BLUECONNECTSATT", "FIERCE", "LINKUP"):
    time.sleep(7)
    wait.until(EC.presence_of_element_located((By.NAME, "porting_st_type[]"))).send_keys("Ave")

wait.until(EC.presence_of_element_located((By.NAME, "porting_ac_number[]"))).send_keys("1234")

wait.until(EC.presence_of_element_located((By.NAME, "account_pass[]"))).send_keys("3456")

wait.until(EC.element_to_be_clickable((By.NAME, "submit"))).click()
time.sleep(5)
wait.until(EC.element_to_be_clickable((By.ID, "pay_method_3"))).click()
time.sleep(5)
wait.until(EC.element_to_be_clickable((By.ID, "sub_cash"))).click()

print("\n✅ Port-in completed successfully!")

time.sleep(5)
driver.quit()
