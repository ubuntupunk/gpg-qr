import qrcode
import subprocess
import requests
import os
from PIL import Image  # Import Pillow

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
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
    except FileNotFoundError:
        print("Error: qrencode is not installed. Please install it (e.g., 'apt install qrencode').")
    except subprocess.CalledProcessError as e:
        print(f"Error executing qrencode: {e}")

def save_qr_as_png(img, filename="revoke_qr.png"):
    img.save(filename)
    print(f"QR code saved as {filename}")

def upload_to_site(data, upload_url):
    try:
        files = {'-': ('revoke.asc', data.encode('utf-8'))}  # Simulate curl's -F-=\<-
        response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            print(f"Uploaded successfully. Response: {response.text}")
        else:
            print(f"Upload failed. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Upload error: {e}")

def main():
    revoke_cert = input("Enter your GPG revoke certificate:\n")

    img = generate_qr_code(revoke_cert)

    while True:
        action = input("Choose an action:\n1. Display in terminal\n2. Save as PNG\n3. Upload to site\n4. Exit\n")

        if action == '1':
            display_qr_in_terminal(revoke_cert)
        elif action == '2':
            save_filename = input("Enter filename for PNG (default: revoke_qr.png): ") or "revoke_qr.png"
            save_qr_as_png(img, save_filename)
        elif action == '3':
            upload_url = input("Enter upload URL: ")
            upload_to_site(revoke_cert, upload_url)
        elif action == '4':
            break
        else:
            print("Invalid action.")

if __name__ == "__main__":
    main()
