# flask-simple-captcha

### CURRENT VERSION: **v5.5.2**

**v5.0.0+ added an encryption mechanism to the stored text in the jwts. Previous versions are insecure!**

**v5.5.1** changed the noise generation to ensure that the captcha text is easier to read for humans, since the ai tools are pretty good at reading the text regardless of the noise.

**v5.5.2** fixed a bug where the fonts files were not being included in the package when installed via pip. thank you @timeeeee for the PR

`flask-simple-captcha` is a CAPTCHA generator class for generating and validating CAPTCHAs. It allows for easy integration into Flask applications.

See the encryption / decryption breakdown below for more information on the verification mechanism.

## Features

- Generates CAPTCHAs with customizable length and characters
- Easy integration with Flask applications
- Built-in image rendering and line drawing for added complexity
- Base64 image encoding for easy embedding into HTML
- Uses JWTs and Werkzeug password hashing for secure CAPTCHA verification
- Successfully submitted CAPTCHAs are stored in-memory to prevent resubmission
- Backwards compatible with 1.0 versions of this package
- Avoids visually similar characters by default
- Supports custom character set provided by user
- Casing of submitted captcha is ignored by default
- Minor random font variation in regards to size/family/etc
- PNG/JPEG image format support

## Prerequisites

- Python 3.7 or higher
- Werkzeug >=0.16.0, <3
- Pillow >4, <10

## Installation

Import this package directly into your Flask project and make sure to install all dependencies.

## How to Use

### Configuration

```python
DEFAULT_CONFIG = {
    'SECRET_CAPTCHA_KEY': 'LONG_KEY', # Used for JWT encoding/
    'CAPTCHA_LENGTH': 6 # CAPTCHA text length
    'CAPTCHA_DIGITS': False # Include digits in the character pool?
    'EXPIRE_SECONDS': 600 # CAPTCHA expiration time in seconds
    # 'EXPIRE_MINUTES': 10 # Also supported for backwards compatibility
    # 'EXCLUDE_VISUALLY_SIMILAR': True # Optional exclude visually similar characters like 0OIl
    # 'ONLY_UPPERCASE': True # Optional only use uppercase characters
    # 'CHARACTER_POOL': 'AaBbCc123' # Optional specify character pool
}

```

### Initialization

Add this code snippet at the top of your application:

```python
from flask_simple_captcha import CAPTCHA
YOUR_CONFIG = {
    'SECRET_CAPTCHA_KEY': 'LONG_KEY',
    'CAPTCHA_LENGTH': 6,
    'CAPTCHA_DIGITS': False,
    'EXPIRE_SECONDS': 600,
}
SIMPLE_CAPTCHA = CAPTCHA(config=YOUR_CONFIG)
app = SIMPLE_CAPTCHA.init_app(app)
```

### Protecting a Route

To add CAPTCHA protection to a route, you can use the following code:

```python
@app.route('/example', methods=['GET','POST'])
def example():
    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        render_template('example.html', captcha=new_captcha_dict)
    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if SIMPLE_CAPTCHA.verify(c_text, c_hash):
            return 'success'
        else:
            return 'failed captcha'
```

In your HTML template, you need to wrap the CAPTCHA inputs within a form element. The package will only generate the CAPTCHA inputs but not the surrounding form or the submit button.

```html
<!-- your_template.html -->
<form action="/example" method="post">
  {{ captcha_html(captcha)|safe }}
  <input type="submit" value="Submit" />
</form>
```

## Example Captcha Images

Here is an example of what the generated CAPTCHA images look like, this is a screen shot from the `/images` route of the debug server.

![Example CAPTCHA Image](/captcha-example.PNG)

[link to image url if the above does not load](https://github.com/cc-d/flask-simple-captcha/blob/master/captcha-example.PNG)

## Encryption and Decryption Breakdown

Uses a combination of JWTs and Werkzeug's password hashing to encrypt and decrypt CAPTCHA text.

### Encryption

1. **Salting the Text**: The CAPTCHA text is salted by appending the secret key at the beginning.
   ```python
   salted_text = secret_key + text
   ```
2. **Hashing**: Werkzeug's `generate_password_hash` function is then used to hash the salted CAPTCHA text.
   ```python
   hashed_text = generate_password_hash(salted_text)
   ```
3. **Creating JWT Token**: A JWT token is generated using the hashed CAPTCHA text and an optional expiration time.
   ```python
   payload = {
       'hashed_text': hashed_text,
       'exp': datetime.utcnow() + timedelta(seconds=expire_seconds),
   }
   return jwt.encode(payload, secret_key, algorithm='HS256')
   ```

### Decryption

1. **Decode JWT Token**: The JWT token is decoded using the secret key. If the token is invalid or expired, the decryption process will fail.
   ```python
   decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
   ```
2. **Extract Hashed Text**: The hashed CAPTCHA text is extracted from the decoded JWT payload.
   ```python
   hashed_text = decoded['hashed_text']
   ```
3. **Verifying the Hash**: Werkzeug's `check_password_hash` function is used to verify that the hashed CAPTCHA text matches the original salted CAPTCHA text.
   ```python
   salted_original_text = secret_key + original_text
   if check_password_hash(hashed_text, salted_original_text):
       return original_text
   ```

# Development

### Setting Up Your Development Environment Without VS Code

1. **Create a Virtual Environment:**

   - Navigate to the project directory where you've cloned the repository and create a virtual environment named `venv` within the project directory:

     ```bash
     python -m venv venv/
     ```

2. **Activate the Virtual Environment:**

   - Activate the virtual environment to isolate the project dependencies:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows (using Command Prompt):
       ```cmd
       .\venv\Scripts\activate
       ```
     - On Windows (using PowerShell):
       ```powershell
       .\venv\Scripts\Activate.ps1
       ```

3. **Install Dependencies:**

   Install the required dependencies for development:

   ```bash
   pip install -r requirements_dev.txt
   ```

   Install the local flask-simple-captcha package:

   ```bash
   pip install .
   ```

## Running Tests

#### ENSURE YOU HAVE A VENV NAMED `venv` IN THE PROJECT DIRECTORY AND THAT IT IS ACTIVATED AND BOTH THE DEPENDENCIES AND THE LOCAL FLASK-SIMPLE-CAPTCHA PACKAGE ARE INSTALLED IN THE VENV

As of the time of me writing this README (2023-11-15), pytest reports 97% test coverage of the logic in the `flask_simple_captcha` package. Should be kept as close to 100% as possible. If I hadn't spent the last 7 hours working on this, I'd do it tonight.

### Run Tests Without VS Code

- Run the tests using the following command (make sure your venv is activated and you are in the project directory)
  ```bash
  python -m pytest tests.py -s -vv --cov=flask_simple_captcha/ --cov-report term-missing
  ```
- The command runs pytest with flags for verbose output, standard output capture, coverage report, and displaying missing lines in the coverage.

### Running Tests With VS Code

Simply hit command + shift + p and type "Select And Start Debugging" and select `Python: Run tests`. You will want to make sure your venv is installed and activated.

### Example Test Output

```bash
... previous output omitted for brevity ...

tests.py::TestCaptchaUtils::test_jwtencrypt PASSED
tests.py::TestCaptchaUtils::test_no_hashed_text PASSED

---------- coverage: platform darwin, python 3.8.18-final-0 ----------
Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
flask_simple_captcha/__init__.py                 3      0   100%
flask_simple_captcha/captcha_generation.py      89      5    94%   89-93
flask_simple_captcha/config.py                   7      0   100%
flask_simple_captcha/img.py                     46      1    98%   28
flask_simple_captcha/text.py                    25      0   100%
flask_simple_captcha/utils.py                   51      0   100%
--------------------------------------------------------------------------
TOTAL                                          221      6    97%


================= 38 passed in 4.28s =================
```

## Debug Server

#### **Start the debug server without VS Code**

1. **Set Environment Variables:**
   - Before running the debug Flask server, set the required environment variables:
   - On macOS/Linux:
     ```bash
     export FLASK_APP=debug_flask_server
     export FLASK_DEBUG=1
     ```
   - On Windows (using Command Prompt):
     ```cmd
     set FLASK_APP=debug_flask_server
     set FLASK_DEBUG=1
     ```
   - On Windows (using PowerShell):
     ```powershell
     $env:FLASK_APP="debug_flask_server"
     $env:FLASK_DEBUG="1"
     ```
2. **Start the debug Flask server:**
   - Run the following command to start the debug Flask server:
     ```bash
     flask run --no-debugger
     ```
   - This will start the debug Flask server with the automatic reloader. See the navigation section below on how to access the debug server.

#### **Start the debug server with VS Code**

- Hit command + shift + p and type "Select And Start Debugging" and select `Python: Flask`
- This will start the debug Flask server with debugging features enabled, including the interactive debugger and automatic reloader.

### Accessing the Debug Server

Navigate to `localhost:5000` in your browser to view the debug server. You can also navigate to `localhost:5000/images` to view 50 CAPTCHA images at once.

## Contributing

Feel free to open a PR. The project has undergone a recent overhaul to improve the code quality.

If you make changes in the logic, please follow the steps laid out in this document for testing and debugging. Make sure the coverage % stays >= 100% and that you verify manually at least once that things look okay by submitting a real CAPTCHA in the debug server.

The `pyproject.toml` has the required configuration for `black` and `isort`. There is also a vscode settings file equivalent to the `pyproject.toml` file in `.vscode/settings.json`.

## License

MIT

Contact: ccarterdev@gmail.com
