import qrcode
import subprocess
import requests
import os
from urllib.parse import quote  # Import quote for URL encoding

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
        process = subprocess.run(['qrencode', '-t', 'UTF8', '-o', '-', data], capture_output=True, text=True, check=True)
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

def save_qr_as_png(img, filename="revoke_qr.png"):
    try:
        img.save(filename)
        print(f"QR code saved as {filename}")
        return True
    except Exception as e:
        print(f"Error saving QR code as PNG: {e}")
        return False

def upload_to_site(data, upload_url):
    pad_name = input("Enter a name for the Riseup pad: ")
    if not pad_name:
        print("Pad name cannot be empty.  Aborting upload.")
        return False

    create_pad_url = f"{upload_url}/p/{quote(pad_name)}"

    try:
        params = {'text': data}
        response = requests.post(create_pad_url, data=params)
        response.raise_for_status()
        print(f"Uploaded successfully. Response: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Upload error: {e}")
        return False

def main():
    revoke_cert_path = input("Enter the path to your GPG revoke certificate:\n")
    if not revoke_cert_path:
        print("Revoke certificate path cannot be empty. Exiting.")
        return

    try:
        with open(revoke_cert_path, 'r') as f:
            revoke_cert_content = f.read()
            img = generate_qr_code(revoke_cert_content)

            while True:
                print("\nChoose an action:")
                print("1. Display in terminal")
                print("2. Save as PNG")
                print("3. Upload to site")
                print("4. Exit")
                action = input("Enter your choice: ")

                try:
                    if action == '1':
                        if not display_qr_in_terminal(revoke_cert_content):
                            print("Action failed. Please check the error message.")
                    elif action == '2':
                        save_filename = input("Enter filename for PNG (default: revoke_qr.png): ") or "revoke_qr.png"
                        if not save_qr_as_png(img, save_filename):
                            print("Action failed. Please check the error message.")
                    elif action == '3':
                        upload_url = "https://pad.riseup.net"
                        if not upload_to_site(revoke_cert_content, upload_url):
                            print("Action failed. Please check the error message.")
                    elif action == '4':
                        break
                    else:
                        print("Invalid action.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
    except FileNotFoundError:
        print(f"Error: File not found at path: {revoke_cert_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
