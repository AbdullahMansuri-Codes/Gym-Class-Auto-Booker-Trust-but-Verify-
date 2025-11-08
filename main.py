from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time

# Account credentials
ACCOUNT_EMAIL = ""
ACCOUNT_PASSWORD = ""
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

wait = WebDriverWait(driver, 5)

# ---------- LOGIN ----------
login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
login_btn.click()

email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
email_input.clear()
email_input.send_keys(ACCOUNT_EMAIL)

password_input = driver.find_element(By.ID, "password-input")
password_input.clear()
password_input.send_keys(ACCOUNT_PASSWORD)

submit_btn = driver.find_element(By.ID, "submit-button")
submit_btn.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# ---------- CLASS SCRAPING ----------
booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

# Find all day titles (e.g., Mon, Tue, Wed, etc.)
day_titles = driver.find_elements(By.CLASS_NAME, "Schedule_dayTitle__YBybs")

# For each day section, find its associated classes
for day_title in day_titles:
    day_text = day_title.text

    if "Tue" in day_text or "Thu" in day_text:
        # Find the parent container (the day block)
        day_container = day_title.find_element(By.XPATH, "./ancestor::div[contains(@class, 'Schedule_dayGroup__')]")

        # Get all class details inside this day block
        class_details = day_container.find_elements(By.CLASS_NAME, "ClassCard_classDetail__Z8Z8f")

        for detail in class_details:
            try:
                # Extract text of class detail
                time_text = detail.text

                if "6:00 PM" in time_text:
                    # Get the full class card (parent element)
                    card = detail.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ClassCard_card__')]")
                    class_name = card.find_element(By.TAG_NAME, "h3").text
                    button = card.find_element(By.TAG_NAME, "button")

                    class_info = f"{class_name} on {day_text}"

                    # Handle booking logic
                    if button.text == "Booked":
                        print(f"✓ Already booked: {class_info}")
                        already_booked_count += 1
                        processed_classes.append(f"[Booked] {class_info}")
                    elif button.text == "Waitlisted":
                        print(f"✓ Already on waitlist: {class_info}")
                        already_booked_count += 1
                        processed_classes.append(f"[Waitlisted] {class_info}")
                    elif button.text == "Book Class":
                        button.click()
                        print(f"✓ Successfully booked: {class_info}")
                        booked_count += 1
                        processed_classes.append(f"[New Booking] {class_info}")
                        time.sleep(0.5)
                    elif button.text == "Join Waitlist":
                        button.click()
                        print(f"✓ Joined waitlist for: {class_info}")
                        waitlist_count += 1
                        processed_classes.append(f"[New Waitlist] {class_info}")
                        time.sleep(0.5)

            except Exception as e:
                print(f"❌ Error processing a class on {day_text}: {e}")

# ---------- SUMMARY ----------
print("\n--- BOOKING SUMMARY ---")
print(f"New bookings: {booked_count}")
print(f"New waitlist entries: {waitlist_count}")
print(f"Already booked/waitlisted: {already_booked_count}")
print(f"Total Tuesday & Thursday 6pm classes: {booked_count + waitlist_count + already_booked_count}")

print("\n--- DETAILED CLASS LIST ---")
for class_detail in processed_classes:
    print(f"  • {class_detail}")

# --- TRUST BUT VERIFY SECTION ---
print("\n🔍 Verifying bookings on 'My Bookings' page...")

try:
    # Step 1: Navigate to "My Bookings" page
    try:
        my_bookings_tab = wait.until(
            ec.element_to_be_clickable((By.XPATH, "//a[contains(., 'My Bookings')] | //button[contains(., 'My Bookings')]"))
        )
        my_bookings_tab.click()
    except Exception:
        print("⚠️ Could not click 'My Bookings' tab (maybe already on the page).")

    # Step 2: Wait for the bookings page to load
    wait.until(ec.presence_of_element_located((By.XPATH, "//*[@id='my-bookings-page']")))

    # Step 3: Get all booking cards
    booking_cards = driver.find_elements(By.CLASS_NAME, "MyBookings_bookingCard__VRdrR")

    verified_classes = []
    verified_count = 0

    for card in booking_cards:
        try:
            # Instead of relying on changing CSS module names, just read all visible text
            card_text = card.text.strip()

            # Only include Tuesday/Thursday 6PM bookings
            if ("Tue" in card_text or "Thu" in card_text) and "6:00 PM" in card_text:
                verified_classes.append(card_text)
                verified_count += 1

        except Exception as e:
            print(f"⚠️ Could not read one of the booking cards: {e}")

    # Step 4: Print verification summary
    print("\n--- VERIFICATION SUMMARY ---")
    print(f"Total intended bookings (Tues/Thurs 6PM): {booked_count + waitlist_count}")
    print(f"Total verified on 'My Bookings' page: {verified_count}")

    if verified_count == (booked_count + waitlist_count + already_booked_count):
        print("✅ All bookings successfully verified on 'My Bookings' page!")
    else:
        print("⚠️ Some bookings could not be verified. Please double-check manually.")

    # Optional: print all verified classes
    print("\n--- VERIFIED CLASSES ---")
    for c in verified_classes:
        print(f"  • {c}")

except Exception as e:
    print(f"❌ Verification failed: {e}")
