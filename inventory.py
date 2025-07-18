from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import random

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.maximize_window()

driver.get("")

# Step 1: Login
driver.find_element(By.NAME, "login_user_id").send_keys("")
driver.find_element(By.NAME, "passwd").send_keys("")
driver.find_element(By.ID, "submit_button").click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sidebar-menu")))

# Step 2: Navigate to New Enrollment
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Inventory')]"))).click()
# time.sleep(2)
link = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//a[contains(text(), 'Manage inventory') or contains(text(), 'Manage Inventory')]"
)))
link.click()

add_unit = driver.find_element(By.XPATH, "//a[contains(@class,'darkgreen-bg') and contains(text(),'Add Single Unit')]")
add_unit.click()

time.sleep(2)

carrier_dropdown = wait.until(EC.presence_of_element_located((By.ID, "carrier")))

# Wrap in Select
select = Select(carrier_dropdown)

# Wait until options are loaded (at least 2 options: default + real)
wait.until(lambda driver: len(select.options) > 1)

# Get all carrier options except the first default option
carrier_options = select.options[1:]

# Prepare carrier names for user display
carrier_names = [option.text.strip() for option in carrier_options]

# Display available carriers to user
print("Available carriers:")
for idx, name in enumerate(carrier_names, start=1):
    print(f"{idx}. {name}")

# Take user input for selection
choice = int(input("Enter carrier number to select: "))

# Get the selected option element
selected_option = carrier_options[choice - 1]

# Select by visible text
select.select_by_visible_text(selected_option.text)

print(f"✅ Carrier selected: {selected_option.text}")

sim_number = '8' + ''.join([str(random.randint(0, 9)) for _ in range(19)])
driver.find_element(By.ID, "esn").send_keys(sim_number)

print("✅ SIM entered:", sim_number)

imei_number = ''.join([str(random.randint(0, 9)) for _ in range(15)])
driver.find_element(By.ID, "imei").send_keys(imei_number)

print("✅ IMEI entered:", imei_number)

assign_dropdown = wait.until(EC.presence_of_element_located((By.ID, "assign_user")))

# Wrap in Select
assign_select = Select(assign_dropdown)

# Select "Employee" by visible text
assign_select.select_by_visible_text("Employee")

print("✅ 'Employee' selected successfully!")

# Wait for the Employee dropdown

# Step 1: Click on the visible dropdown box (Select2)

assign_dropdown = wait.until(EC.presence_of_element_located((By.ID, "agen_type")))
time.sleep(2)  # Let all options load
assign_select = Select(assign_dropdown)

# See what Selenium actually sees
for opt in assign_select.options:
    print(f"🟨 Option found: '{opt.text}'")

# Now filter
options = [opt.text.strip() for opt in assign_select.options if "--Select--" not in opt.text and opt.text.strip() != ""]

print(f"✅ Total valid employee options: {len(options)}")

for i, name in enumerate(options, start=1):
    print(f"{i}. {name}")

choice = int(input("Enter the number of the employee you want to select: "))
selected_option = options[choice - 1]
assign_select.select_by_visible_text(selected_option)
print(f"✅ Selected employee: {selected_option}")

from selenium.webdriver.common.keys import Keys

# Click Product dropdown

time.sleep(3)
# 1. Click on the Product dropdown (combobox)
product_dropdown = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//label[contains(text(),'Product Name')]/following::span[contains(@class,'select2-selection--single')][1]")
))
product_dropdown.click()
time.sleep(1)

# 2. Wait until the search input box is visible
search_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[contains(@class,'select2-search__field')]")
))
search_input.send_keys("SIM SIM")
time.sleep(1)

# 3. Wait and click the actual dropdown item
option_to_click = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//li[contains(text(),'SIM SIM')]")
))
option_to_click.click()

print("✅ Product selected: SIM SIM")


print("✅ Save button clicked!")

time.sleep(5)
print(f"✅ ESN saved successfully: {sim_number}")

# After clicking Save button
save_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-save")))
save_button.click()

print("✅ Save button clicked!")
print(f"✅ ESN saved successfully: {sim_number}")

# ⏸ Pause script until you confirm SIM is added
input("⏸ Please verify SIM manually in the UI. Press Enter to continue...")

driver.quit()

driver.quit()

time.sleep(5)
driver.quit()