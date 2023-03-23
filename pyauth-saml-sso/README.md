 <p align="center">
 <img width="100px" src="https://nathanbrito.com.br/logo.png" align="center" alt="nathanbritonsb" />
</p>
<h2 align="center"> PyAuth: SAML SSO </h2>

<p align="center">Python solution to automate the authentication process on SAML SSO authentication systems to get data of protected pages.</p>

<div align="center">

<a href="">![python](https://img.shields.io/badge/language-python-blue)</a>
<a href="">![beta](https://img.shields.io/badge/status-stable-green)</a>
<a href="">![zabbix](https://img.shields.io/badge/version-1.0-9cf)</a>

</div>


## 1 - Process of authentication

1 - The user access the login page. Then, the user is redirected to real login page with parameters on URL. One of these parameters is the sessionDataKey.

2 - When user try sign in, the form is posted with Username, Password and sessionDataKey to authenticator.

3 - If the authentication get success, the authenticator will answer with a data called SAMLResponse.
    With this SAMLResponse, we can connect to service provider.

4 - After connected to service provider, we only need maintain the session cookies.

5 - The last process is make a request to protected page.

## 2 - Usage Example

```python
from auth import AuthSamlSso

# Initiate the instance with username/password
new = AuthSamlSso(nathan, mypassword)

# Getting the sessionDataKey
session_dk = new.get_session_data_key('http://portal.servicos.nathanbrito.com.br/portal')

# Get samlResponse
saml = new.get_saml_response('https://is.producao.nathanbrito.com.br/samlsso', session_dk)

# Send samlResponse to service provider
if new.send_saml_response('http://portal.servicos.nathanbrito.com.br/portal/consumer', saml):
    # Getting protected page data
    data = new.get_authenticated_data('http://portal.servicos.nathanbrito.com.br/cadastro.html')
    print(data)
else:
    raise Exception("cant send saml to service provider")
```


## 3 - ToDo:

Will be incredible if the script can follow redirects and self identify the urls of authenticators and service providers.
If we can do this, we only will need one public method.

