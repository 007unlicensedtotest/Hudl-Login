Feature: Hudl Login Page Testing
  As a user of Hudl
  I want to be able to login to my account
  So that I can access my sports content and data

  Background:
    Given I am on the Hudl login page

  @smoke @positive 
  Scenario: Successful login with valid email and password
    Given I enter a valid email address
    And I enter a valid password
    Then I should be redirected to the dashboard page
    And I should see my display name

  @smoke @positive 
  Scenario Outline: Successfully redirected to login provider sites
    Given I click the "<provider>" login button
    Then I should get redirected to the <provider_url>

    Examples:
      | provider | provider_url |
      | google   | https://accounts.google.com |
      | facebook | https://www.facebook.com |
      | apple    | https://appleid.apple.com |


  @negative @validation 
  Scenario: Login with invalid email and valid password
    When I enter an invalid email address
    And I enter a valid password
    Then I should see an email error message
    And I should remain on the login page

  @negative @validation 
  Scenario: Login with valid email and invalid password
    When I enter a valid email address
    And I enter an invalid password
    Then I should see a password error message
    And I should remain on the login page

  @negative @validation 
  Scenario: Login with empty email field
    When I leave the email field empty
    Then I should see a validation message for "email"

  @negative @validation 
  Scenario: Login with empty password field
    When I enter a valid email address
    And I leave the password field empty
    Then I should see a validation message for "password"

  @negative @validation 
  Scenario Outline: Login with invalid email formats
    When I enter an invalid email address "<invalid_email>"
    Then I should see an invalid email error message

    Examples:
      | invalid_email     |
      | invalid.email     |
      | @domain.com       |
      | user@            |
      | user@.com        |
      | user name@domain.com |

  @ui @functionality 
  Scenario: Show/Hide password functionality
    When I enter a valid email address
    And I enter a masked password
    And I click the show/hide password button
    Then the password should be visible as plain text
    When I click the show/hide password button
    Then the password should be masked again

  @functionality 
  Scenario: Forgot password link functionality
    When I enter a valid email address
    And I click the "Forgot password?" link
    Then I should be redirected to the password reset page
    And the page should have password reset functionality

  @functionality 
  Scenario: Sign up link functionality
    When I click the "Sign up" link
    Then I should be redirected to the registration page
    And the page should have account creation functionality

  @logout @cleanup
  Scenario: Successful logout after login
    Given I am logged in with valid credentials
    When I click the logout button
    Then I should be logged out successfully
    And I should be redirected to the base website page
    And my session should be cleared
