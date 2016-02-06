GoogleOAuth2
========

A demo and helper class for providing GoogleOAuth2 authentication in java.

Assumptions

- familiarity with OOP, java, maven, and jee
- java application server listening on localhost:8080

Prerequisites

- Google API access credentials (Client ID, Client Secret). Set it up here https://code.google.com/apis/console/
- Set up allowed Redirect URIs at Google API -> API Access. Input: http://localhost:8080/GoogleOAuth2/index.jsp
- a positive outlook on life

Usage

- Add Client ID, and Client Secret parameters to GoogleAuthHelper.java
- Compile the project ($ mvn clean install)
- Deploy war to application server
- Browse to: http://localhost:8080/GoogleOAuth2/
- Click "log in with google" on top of this page

Credits
- Original code form https://github.com/mdanter/OAuth2v1
