Middleware for the OpenStack Identity API (Keystone)
====================================================

This package contains validatetoken middleware for validating Keystone token
original keystonemiddleware.auth_token is doing, but using the token itself as
authentication information (GET /auth/tokens with
X-Auth-Token=X-Subject-Token). If populates all information like auth_token is
doing and pass it further down the pipeline. If the token is invalid or expired
immedialey NotAuthorized response is returned.
