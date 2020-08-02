# Advanced Web Services
## Flask Backend
```
Date Created: July 07, 2020
Date Modified: - July 21, 2020
Group: 5
```

## How to use it?
To use to do the following steps:

1. Clone my branch using this command `git clone --single-branch --branch sahil https://github.com/SahilFruitwala/rentalvista-backend.git`
2. Go to the folder
3. Open terminal in folder and write the following command `pip install -r requirements.txt`
4. Create .env file in root folder of repo
5. ADD 
    ```
    URI=<mongodb atlas url>
    SECRET_KEY=<secret-key anything>
    SENDGRID_API_KEY=<API key of twilio>
    MAIL_DEFAULT_SENDER=<single sender email from twilio>
    ```
6. Ignore last 2 if you don't want mailing service
7. Run command `python app.py` in windows and for mac/linux `python3 app.py`

