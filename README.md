# Cyber Security Base 2023 Project 1

This is a [Cyber Security Base 2023 course project 1](https://cybersecuritybase.mooc.fi/module-3.1). The application has many critical security flaws, and should not be used anywhere except on this course.

## The application

A simple movie discussion site, where users can talk about their favourite movies. chatGPT and DALL-e 2 were used only to create content to the site. In this application you can:
1. Create an account
2. Log in/out
3. talk about movies (send and read comments)

## Installation

This project requires python version ^3.10

I have not tried this on Mac, but Linux instructions should work.

1. Clone this repository or download the latest release
2. Navigate to the root directory (containing this README.md) in CLI
3. Create virtual environment with command `python3 -m venv venv`. If it does not work on Windows, try `python -m venv venv`
4. Activate virtual environment
    - Linux/Mac: `source ./venv/bin/activate`
    - Windows Command Prompt: `.\venv\Scripts\activate.bat`
    - Windows PowerShell`.\venv\Scripts\activate.ps1`
5. Install dependencies: `pip install -r requirements.txt`
6. build database: `invoke build`
7. Run application: `invoke dev`
    - or `flask --app ./src/app.py run --debug`
8. Application can be found at: `http://127.0.0.1:5000`

The app has 2 users
1. username: `alice`, password: `pword`
2. username: `bob`, password: `pword`


OWASP top ten 2021

### FLAW 1: A03:2021 – Injection

[link to source code](link)

SQL injection: Malicious sql code is injected and executed in the database. In the worst case scenario, an attacker could run any commands in the database, possibly stealing, modifying and deleting critical data.

This application has an SQL injection vulnerability in the comment text area. The attacker can not run multiple SQL commands, but can modify the command that is used to save comments to the database. Comments that the users send are not sanitized, so a malicious use can, for example, impersonate another user. This can be done writing `<COMMENT>', <USER ID>, <MOOVIE ID>); --` to the comment field.
1. Log in as `alice`
2. Go to `http://127.0.0.1:5000/moovie/1`
3. write into the comment field: `I am bob', 2, 1); --`
4. Now the comment is saved to the database with bob's id (2).

The correct way to implement this operation is to use parametrized queries that are secure agains SQL injections. The fixed code is here: [comment_repository.py 24-28](link). Other solution would be to use ORM (Object relational mapping tool).

### FLAW 2: A01:2021 – Broken Access Control

[link to source code](link)

Currently any user can delete comments posted by other users. The moovie.html template (frontend) does not show delete button for comments written by other users, and delete form has csrf_token, which is validated in the backend. However, the backend does not check at the moment if the user making the request is the same that posted the comment.

try it out!
1. Log in as bob
2. go to `http://127.0.0.1:5000/moovie/1`
3. Send a comment
4. Inspect the delete button in the browser
5. Change `<form action="/comment/delete/2" method="POST">` to `<form action="/comment/delete/1" method="POST">`
6. Click the delete button! Now the first message posted by alice is deleted.

The fix to this vulnerability is commented in the [comment_service.py lines 21-23](link). First the comment's user id is fetched from the database and then checked if it matches the user who tries to delete it. If there is no match, 401 unauthorized is returned.

### FLAW 3: A02:2021 – Cryptographic Failures

[link to user_service.py](link)
[link to build](link)

Insecure hashing functions can lead to exposure of sensitive data, such as passwords. If an attacker would be able to get to the database, weakly crypted passwords could be cracked easily. My application stores passwords hashed with `MD5` to the database. According to Software Engineering Institute (SEI) MD5 is deprecated and ["should be considered cryptographically broken and unsuitable for further use"](https://www.kb.cert.org/vuls/id/836068)

The fix here is simple, just remove the `method="md5"`. The default hash in generate_password_hash function is `pbkdf2`, which is considered secure at the moment. Additionally, it is essential to address all the old hashes, that were stored using MD5. The old password hashes can be updated the next time the user logs in [lines](bothfiles).

### FLAW 4: Cross-Site Request Forgery (CSRF) 

[link to routes /comments](link)

With cross-site request forgery vulnerability, attacker can submit a request to the application in which the user is currently logged in. User can be, for example, directed to a site, that automatically sends request to change password on the application. This app has csrf vulnerability in comment section. Even though the comment field has csrf_token, it's not checked in the backend.

example:
1. Bob logs in to the moovie site.
2. An attacker directs bob to his site, that sends POST request with a comment to the `/comment/<int:id>` route
3. Site recives the comment with bob's cookie, so the comment is saved to the database.
4. Bob is confused.

To fix this, uncomment the @csrf [here](link). [This wrapper](link) checks that the forms csrf_token matches the session's csrf_token.

### FLAW 5 A07:2021 – Identification and Authentication Failures

Many users tend to use simple words found in dictionaries as passwords. These passwords are easy to guess, so the service should enforce strict guidelines on what is required. My application has only one requirement for users password: 12 characters. This is a step to the right direction, but it is not enough to make sure that the users have strong passwords.

Fix: More requirements could be added to validate_passwords() method in the UserService. Minimum length of 12 is fine, but the validator should also check that different kinds of characters are used: upper- and lowercase, numbers and punctuations. It is also important to make sure, that the password is not among the most used ones.