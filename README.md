# gpg-qr

A simple tool to generate QR codes from GPG revoke certificates.

## Usage
Place your ascii public.key or revoke.asc in the directory in which you invoke the script, save as PNG, then either view PNG in a CV2 pop-up, or upload PNG to tempfiles.org. The result will be available online for a few hours. 

## Options ##
1. Display in Terminal
2. Save as PNG
3. Upload PNG to TempFiles.org
4. Quit

## Installation ##
```python
pip install gpg-qrcv
```
## Note
This is the cv2 version which uses the cv2 library for processing of the qr code, its a big library and the wheel may take time to build on older machines. A [qrencode](https://fukuchi.org/works/qrencode/) version is available on qrencode branch for those who are able to install it.

## License ##
[GPL3](LICENSE)
