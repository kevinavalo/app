# User Stories

## General User
1. As a general user, I would like to update my profile information so that it can always be up-to-date despite possible changes.

*Acceptance Criteria*:

**PASSWORD**
1. When a user inputs an empty string into the new_password field and a user inputs an empty string into the confirm_password field (i.e. the password is not changed) the current user's password is not changed.
2. When a user inputs a string into the new_password field and a different string the confirm_password field, the current user's password is not changed and an error is returned, saying 'passwords must match'
3. When a user inputs a valid string into the new_password field and the same valid string the confirm_password field, the current user's password is changed and the user is redirected to login.

**EMAIL**
1. When a user inputs an empty string into the new_email field (i.e. the email is not changed) the current user's email is not changed.
2. When a user inputs an invalid email into the new_email field, the current user's email is not changed and an error message is returned, saying, 'you must enter a valid email address'
3. When a user inputs a valid email that has already been used by another user into the new_email field, the current user's email is not changed and an error message is returned, saying, 'email address already in use'
4. When a user inputs a valid email address that has not been used by another user, the current user's email is updated.

**FIRST NAME/LAST NAME**
1. When a user inputs an empty string into the new_first_name/new_last_name field (i.e. the user's first name/last name is not changed) the current user's first name/last name is not changed.
2. When a user inputs a valid string into the new_first_name/new_last_name field the current user's first name/last name is changed.

**PHONE NUMBER**
1. When a user inputs an empty string into the new_phone_number field (i.e. the phone number is not changed) the current user's phone number is not changed.
2. When a user inputs an invalid phone_number into the new_phone_number field, the current user's phone_number is not changed and an error message is returned, saying, 'you must enter a valid phone number'
3. When a user inputs a valid phone number that has already been used by another user into the new_phone_number field, the current user's phone number is not changed and an error message is returned, saying, 'phone number already in use'
4. When a user inputs a valid phone number that has not been used by another user, the current user's phone number is updated.

**STATE**

**CITY**

**LOGIN/LOGOUT/AUTH**
2. As a general user, I would like to be able to log into an account and stay logged in.

*Acceptance Criteria*:
1. There is a username field, a password field, and a login button on a login page.
2. When an existing user attempts to login with a correct password, there is a unique authenticator created in the database and an auth cookie is created.
3. When an existing user attempts to login with an incorrect password, they are brought back to the login page with corresponding errors.
4. When a non-existing user attempts to login, they are brought back to the login page with corresponding errors.
5. When the user is brought to a different page while still logged in, he/she remains logged in.
6. When the user is logged in, he/she is prevented from logging in as any other user.
7. When the user is logged in, if he/she navigates away from the web application and later returns (before the expiration of the authenticator), he/she is still logged in.

3. As a general user, I would like to be able to log out of my account
*Acceptance Criteria*:
1. A user can only logout when he/she is currently logged in, meaning the button is only visible to users that are logged in, and logout is restricted to logged in users using a login_required decorator.
2. When a user logs out his/her authenticator is deleted from the database table.
3. When a user logs out his/her authenticator cookie is deleted.
4. When a user logs our he/she is redirected to the login page.


## Buyer
1. As a buyer, I would like to pay for the item with my credit card.

## Seller
1. As a seller, I would like to update my listing information in case the item details change.

## Browser
1. As a browser, I would like to search within a specific category of item as to narrow my search.
2. As a browser, I would like to organize my search by price, either descending or ascending, so that I can scan for items within my desired price range.
3. As a browser, I would like the ability to comment on listings so that I can elicit more information from the seller or express my opinions.
4. As a browser, I would like to delete my comments in case I accidentally posted a comment, or no longer wish for it to be on the post.
