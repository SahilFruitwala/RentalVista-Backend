# Advanced Web Services

>Heroku Frontend Link: https://rentalvista.herokuapp.com/
>Heroku Back-end Link: https://rentalvista-api.herokuapp.com/
>Github Frontend Link: https://github.com/SahilFruitwala/Group5_RentalVista_Frontend
>Github Back-end Link: https://github.com/SahilFruitwala/Group5_RentalVista_Backend

> Feature Developed: **User Management System**

#### User Management Feature
I have created user management feature for assignment 4. In this assignment, mainly, I have created backend part and some frontend part. I have developed API to signup, login, edit profile, change password, forgot password and fetch user data. On frontend part, I have developed two new pages, forgot password and change password pages. (Note: All pages for user management feature were developed earlier.)

### Frontend Files created
* Files created apart from existing files:
    1. ./src/components/profile/resetPassword/resetPassword.js
    2. ./src/components/profile/resetPassword/resetPassword.css
    3. ./src/components/login/forgot.js


### Backend Files and Endpoints created
`Note: Base project was setup by me.`
* Created additional python files in **services** directory:
    1. [services/users.py](./services/users.py)
    2. [services/token.py](./services/token.py)
    3. [services/password_generator.py](./services/password_generator.py)
* Endpoints created in `app.py` file:
    1. Signup endpoint: **/users/login**
    2. Login endpoint: **/users/login**
    3. Forgot password endpoint: **/users/forgot**
    4. Change password endpoint: **/users/change**
    5. Fetching user details endpoint: **/users/user**
    6. Edit user details endpoint: **/users/edit**
    7. Logout endpoint: **/users/logout**


## 1. How to run backend on your machine
To use code base follow the steps given below:
1. Clone the repository using https://github.com/SahilFruitwala/rentalvista-backend.git
2. Go to the directory using terminal
3. Install dependencies using `pip install -r requirements.txt`
4. Create .env file into the root directory of project
5. Add following environment variables
    ```
    URI = <mongodb atlas url>
    SECRET_KEY = <secret-key anything>
    SENDGRID_API_KEY = <API key of twilio>
    MAIL_DEFAULT_SENDER = <single sender email from twilio>
    ```
    __Note__: In Mongodb Atlas url remove last part which looks like `&w=majority`. This is because when we set environment variable on heroku it was not allowing to add data with **&** 
6. Run command `python app.py` in windows and for mac/linux `python3 app.py`

## 2. How to run frontend on your machine
To use code base follow the steps given below:
1. Clone the repository using https://github.com/SahilFruitwala/rental-vista.git
2. Go to the directory using terminal
3. Install dependencies using `npm install`
4. Create .env file into the root directory of project
5. Add following environment variables
    `REACT_APP_REGISTER_URL=<API Endpoint>`
    __Note__: For local server add `http:` and make sure API-endpoint/Server supports CORS. For more details regarding CORS go to this [Link](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). After adding environment variable into `.env` file one has to restart development server.
6. Run command `npm run start`

### Backend Files and Endpoints developed
`Note: Base project was setup by me.`
* Created additional python files in **services** directory:
    1. [services/users.py](./services/users.py)
    2. [services/token.py](./services/token.py)
    3. [services/password_generator.py](./services/password_generator.py)
* Endpoints created in `app.py` file:
    1. Signup endpoint: **/users/login**
    2. Login endpoint: **/users/login**
    3. Forgot password endpoint: **/users/forgot**
    4. Change password endpoint: **/users/change**
    5. Fetching user details endpoint: **/users/user**
    6. Edit user details endpoint: **/users/edit**
    7. Logout endpoint: **/users/logout**

