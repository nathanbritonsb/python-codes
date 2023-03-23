import requests
import warnings
warnings.filterwarnings("ignore")
import bs4 as bs
import lxml

class AuthSamlSso:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def get_session_data_key(self, login_url) -> str:
        """ The session data key is a value in URL of the login page. This is unique and identify the session."""
        r = requests.get(login_url, verify=False, allow_redirects=True)
        url = r.url
        parts = url.split("&")
        session_data_key = None
        for part in parts:
            if "sessionDataKey=" in part:
                session_data_key = part.split("sessionDataKey=")[1]
                break
        return session_data_key

    def get_saml_response(self, login_url, session_data_key) -> str:
        """With sessionDataKey, go to login_url, try authenticate, get SAMLResponse"""
        self.login_url = login_url
        self.session_data_key = session_data_key

        response = self.session.post(self.login_url, verify=False, allow_redirects=True, 
                                data={
                                        "username": self.username, 
                                        "password": self.password, 
                                        "sessionDataKey": self.session_data_key, 
                                        "tocommonauth": 'true'
                                      })

        if response.status_code != 200:
            raise Exception("Authentication failed: problem when try get SAMLResponse.")

        # Get SAMLResponse from xml response of request
        soup = bs.BeautifulSoup(response.text, "lxml")
        saml_response = soup.find("input", {"name": "SAMLResponse"}).get("value")
        return saml_response

    def send_saml_response(self, sso_url, saml_response) -> bool:
        """Send saml response to authenticator."""
        self.sso_url = sso_url
        self.saml_response = saml_response

        response = self.session.post(self.sso_url, verify=False, allow_redirects=True, data={"SAMLResponse": self.saml_response})
        if response.status_code != 200:
            raise Exception("Authentication Failed: problem with send SAMLResponse.")
        else:
            return True

    def get_authenticated_data(self, url) -> str:
        """After the complete process of authentication, try get data from pages."""
        self.url = url
        response = self.session.get(self.url, verify=False, allow_redirects=True)
        return response.content