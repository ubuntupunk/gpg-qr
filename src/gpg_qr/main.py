import qrcode
import subprocess
import requests
from io import BytesIO
import shutil
import os
from urllib.parse import quote  # Import quote for URL encoding

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=None,  # Let qrcode library choose the best version
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def display_qr_in_terminal(data):
    try:
        process = subprocess.run(['qrencode', '-t', 'UTF8', '-o', '-'], input=data, capture_output=True, text=True, check=True)
        print(process.stdout)

        return True
    except FileNotFoundError:
        print("Error: qrencode is not installed. Please install it (e.g., 'apt install qrencode' or your system's equivalent).")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error executing qrencode: {e}")
        print(f"qrencode stderr: {e.stderr}") #Added to show stderr
        return False
    except Exception as e:
        print(f"An unexpected error occurred during terminal display: {e}")
        return False

def save_qr_as_png(img, filename="qr.png"):
    try:
        img.save(filename) #save the image
        print(f"QR code saved as {filename}")
        return True
    except Exception as e:
        print(f"Error saving QR code as PNG: {e}")
        return False

def upload_to_site(img):
    upload_url = "https://tmpfiles.org/api/v1/upload"

    try:
        # Save the image to a BytesIO object (in memory)
        img_buffer = BytesIO()
        img.save(img_buffer, "png")
        img_buffer.seek(0)  # Reset the buffer's position to the beginning

        files = {'file': ('qr.png', img_buffer, 'image/png')}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        print(f"{COLOR_GREEN}Uploaded successfully. URL: {response.json()['data']['url']}{COLOR_RESET}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Upload error: {e}")
        return False
    except KeyError as e:
        print(f"Unexpected response from tmpfiles.org: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return False


def main():
    revoke_cert_path = input(f"{COLOR_BLUE}Enter name of your ascii GPG key or revoke certificate:{COLOR_RESET}\n")
    if not revoke_cert_path:
        print(f"{COLOR_RED}Key or certificate name cannot be empty. Exiting.{COLOR_RESET}")
        return

    try:
        with open(revoke_cert_path, 'r') as f:
            revoke_cert_content = f.read()
            img = generate_qr_code(revoke_cert_content)

            while True:
                print("\nChoose an action:")
                print(f"{COLOR_YELLOW}1. Display in terminal{COLOR_RESET}")
                print(f"{COLOR_YELLOW}2. Save as PNG{COLOR_RESET}")
                print(f"{COLOR_YELLOW}3. Upload to Temp site{COLOR_RESET}")
                print(f"{COLOR_YELLOW}4. Exit{COLOR_RESET}")
                action = input(f"{COLOR_BLUE}Enter your choice: {COLOR_RESET}")

                try:
                    if action == '1':
                        if not display_qr_in_terminal(revoke_cert_content):
                            print(f"{COLOR_RED}Action failed. Please check the error message.{COLOR_RESET}")
                    elif action == '2':
                        save_filename = input(f"{COLOR_BLUE}Enter filename for PNG (default: qr.png): {COLOR_RESET}") or "qr.png"
                        if not save_qr_as_png(img, save_filename): #save_qr_as_png returns a boolean, not the image
                            print(f"{COLOR_RED}Action failed. Please check the error message.{COLOR_RESET}")
                    elif action == '3':
                        if not upload_to_site(img):
                            print(f"{COLOR_RED}Action failed. Please check the error message.{COLOR_RESET}")
                    elif action == '4':
                        break
                    else:
                        print(f"{COLOR_RED}Invalid action.{COLOR_RESET}")
                except Exception as e:
                    print(f"{COLOR_RED}An unexpected error occurred: {e}{COLOR_RESET}")
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: File not found at path: {revoke_cert_path}{COLOR_RESET}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
