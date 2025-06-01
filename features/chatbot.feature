Feature: Login
  As a user, I want to log in to the application with valid and invalid credentials

Scenario: Valid login credentials
  Given the user is on the login page
  When the user enters valid username and password
  Then the user should be logged in successfully

Scenario: Invalid login credentials
  Given the user is on the login page
  When the user enters invalid username or password
  Then an error message should be displayed indicating invalid credentials
**step-definitions/login.steps.js**
import { test } from '@playwright/test';
import { expect } from 'chai';

const LoginPage = require('./login-page');

let loginPage;

test('Valid login credentials', async () => {
  loginPage = new LoginPage();
  await loginPage.visit();

  // Enter valid username and password
  await loginPage.fillUsernameAndPassword('valid-username', 'valid-password');
  await loginPage.submitForm();

  // Verify the user is logged in successfully
  expect(await loginPage.isLoggedIn()).to.be.true;
});

test('Invalid login credentials', async () => {
  loginPage = new LoginPage();
  await loginPage.visit();

  // Enter invalid username or password
  await loginPage.fillUsernameAndPassword('invalid-username', 'wrong-password');
  await loginPage.submitForm();

  // Verify an error message is displayed indicating invalid credentials
  expect(await loginPage.getErrorMessage()).to.contain('Invalid username or password');
});
**login-page.js**
class LoginPage {
  async visit() {
    this.page = await global.playwright.chromium.launch();
    await this.page.goto('https://example.com/login');
  }

  async fillUsernameAndPassword(username, password) {
    await this.page.fill('[name="username"]', username);
    await this.page.fill('[name="password"]', password);
  }

  async submitForm() {
    await this.page.click('[type="submit"]');
  }

  async isLoggedIn() {
    return this.page InnerText('h1') === 'Logged in successfully';
  }

  async getErrorMessage() {
    return this.page InnerText('.error-message');
  }
}
In this example, we have a `feature/login.feature` file that defines two scenarios: one for valid login credentials and another for invalid login credentials. The scenarios use Given-When-Then syntax to describe the expected behavior of the application.

The matching step definition file, `login.steps.js`, contains two tests: one for each scenario. Each test uses Playwright's `test` function to run the test, and Chai's `expect` function to verify that the expected behavior occurs.

The `LoginPage` class is used to interact with the login page in both tests. It provides methods for visiting the page, filling out the username and password fields, submitting the form, verifying if the user is logged in successfully, and getting an error message if the credentials are invalid.

Note that this is just an example, and you will need to modify it to fit your specific use case. Additionally, you may need to add more tests or scenarios depending on the requirements of your application.