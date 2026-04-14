```markdown
# MAFile Secret Extractor

A lightweight, GUI-based Python utility designed to bulk-extract the `shared_secret` from `.mafile` files. 

This tool is particularly useful if you need to migrate or back up your two-factor authentication (2FA) data. It scans a selected directory for any files with the `.mafile` extension, extracts the secret key, and compiles everything into a single, clean text file.

## Features

* **Simple GUI:** Built with Python's native `tkinter` library, providing an easy-to-use interface with no command-line interaction required.
* **Bulk Processing:** Select an entire folder and the script will process all `.mafiles` inside it simultaneously.
* **Clean Output Formatting:** Outputs the extracted data in a strict `FileName:SharedSecret` format (excluding the `.mafile` extension and without spaces).
* **Resilient Parsing:** Attempts to parse the file natively as JSON, but includes a built-in Regular Expression fallback just in case the `.mafile` is slightly malformed.
* **No External Dependencies:** Uses only standard Python libraries. No `pip install` required.

## Prerequisites

* **Python 3.x** must be installed on your system. 
* *Windows Users:* Ensure "Add Python to PATH" is checked during installation.

## Usage

1. Download or clone this repository.
2. Run the script by double-clicking the `.py` file, or run it via terminal/command prompt:
   ```bash
   python mafile_extractor.py
   ```
3. **Step 1:** Click "Browse..." to select the folder containing your `.mafile` files.
4. **Step 2:** Click "Browse..." to choose where you want to save the output `.txt` file.
5. Click **Extract Secrets**. The script will process the files and show a popup summarizing the results.

## Output Example

The resulting text file will look like this:

```text
AccountOne:XXXXXXXXXXXXXXXXXXXX=
MySecondAccount:YYYYYYYYYYYYYYYYYYYY=
AltAccount3:ZZZZZZZZZZZZZZZZZZZZ=
```

## ⚠️ Security Warning

**Keep your extracted data safe.** The `shared_secret` is the master seed used to generate your time-based one-time passwords (TOTP). Because this script exports those secrets into an unencrypted, plain text file, anyone with access to the output file can generate your 2FA codes. Never share the output file and ensure it is stored in a secure, private location.
