import qrcode
import subprocess
import requests
import os

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
        print("Error: qrencode is not installed. Please install it (e.g., 'apt install qrencode' or your system's equivalent).")
        return False # Indicate failure
    except subprocess.CalledProcessError as e:
        print(f"Error executing qrencode: {e}")
        return False # Indicate failure
    return True # Indicate success

def save_qr_as_png(img, filename="revoke_qr.png"):
    try:
        img.save(filename)
        print(f"QR code saved as {filename}")
        return True # Indicate success
    except Exception as e:
        print(f"Error saving QR code as PNG: {e}")
        return False # Indicate failure

def upload_to_site(data, upload_url):
    try:
        files = {'-': ('revoke.asc', data.encode('utf-8'))}
        response = requests.post(upload_url, files=files)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Uploaded successfully. Response: {response.text}")
        return True # Indicate success
    except requests.exceptions.RequestException as e:
        print(f"Upload error: {e}")
        return False # Indicate failure

def main():
    revoke_cert = input("Enter your GPG revoke certificate:\n")
    if not revoke_cert:
        print("Revoke certificate cannot be empty. Exiting.")
        return

    img = generate_qr_code(revoke_cert)

    while True:
        print("\nChoose an action:")
        print("1. Display in terminal")
        print("2. Save as PNG")
        print("3. Upload to site")
        print("4. Exit")
        action = input("Enter your choice: ")

        try:
            if action == '1':
                if not display_qr_in_terminal(revoke_cert):
                    print("Action failed. Please check the error message.")
            elif action == '2':
                save_filename = input("Enter filename for PNG (default: revoke_qr.png): ") or "revoke_qr.png"
                if not save_qr_as_png(img, save_filename):
                    print("Action failed. Please check the error message.")
            elif action == '3':
                upload_url = input("Enter upload URL: ")
                if not upload_to_site(revoke_cert, upload_url):
                    print("Action failed. Please check the error message.")
            elif action == '4':
                break
            else:
                print("Invalid action.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
