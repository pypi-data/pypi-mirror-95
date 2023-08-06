import base64
import datetime
import errno
import hashlib
import json
import os
import sys
import webbrowser
import requests
import six
from six.moves.urllib import parse

try:
    import IPython
except ImportError:
    IPython = None


CLIENT_ID = "815921581707-svsvga8nc62df47jks1iplp0ah7v0412.apps.googleusercontent.com"
CLIENT_SECRET = "5amhcZhFPrpbH5FejXZe8fqw"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

SCOPES = ["email", "openid", "profile"]

TOKEN_URI = "https://accounts.google.com/o/oauth2/token"


class AuthManager:
    def __init__(self, credentials_path=None):
        if credentials_path is not None:
            self._credentials_path = credentials_path
        else:
            self._credentials_path = os.path.expanduser(
                "~/.config/geodesic/credentials"
            )

        self._refresh_token = None
        self._id_token = None
        self._id_token_expire = datetime.datetime.utcnow()

    def print_auth_message(self):
        return self.authenticate()

    def get_authorization_url(self, code_challenge):
        """Returns a URL to generate an auth code.
        Args:
            code_challenge: The OAuth2 code challenge
        """

        return "https://accounts.google.com/o/oauth2/auth?" + parse.urlencode(
            {
                "client_id": CLIENT_ID,
                "scope": " ".join(SCOPES),
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
        )

    def _request_token(self, auth_code, code_verifier):
        """Uses authorization code to request tokens."""

        request_args = {
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
        }

        try:
            response = requests.post(TOKEN_URI, request_args)
            response.raise_for_status()

            # json
            self._refresh_token = response.json()["refresh_token"]
            self._write_token()
            return self._refresh_token
        except requests.exceptions.HTTPError as e:
            raise Exception("Problem requesting token. Please try again {0}".format(e))
        except ValueError as e:
            raise Exception("Problem decoding token response {0}".format(e))
        except KeyError as e:
            raise Exception("Refresh token not in response {0}".format(e))

    @property
    def refresh_token(self):
        if self._refresh_token is not None:
            return self._refresh_token

        pth = self._credentials_path

        if not os.path.exists(pth):
            self.print_auth_message()
            raise OSError("credentials don't exist")

        try:
            with open(pth, "r") as fp:
                rt = json.load(fp)
            rt = rt["refresh_token"]
        except Exception:
            raise ValueError(
                "Unabled to get refresh token, delete file '{0}' and rerun authentication".format(
                    pth
                )
            )

        self._refresh_token = rt
        return rt

    @property
    def id_token(self):
        """Requests/returns the access token. If the current token hasn't expired, returns token"""
        if (
            self._id_token is not None
            and self._id_token_expire
            > datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        ):  # noqa
            return self._id_token

        request_args = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        try:
            response = requests.post(TOKEN_URI, request_args)
            response.raise_for_status()

            res = response.json()

            self._id_token = res["id_token"]
            self._id_token_expire = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=res["expires_in"]
            )

        except requests.exceptions.HTTPError as e:
            raise Exception("Problem requesting token. Please try again {0}".format(e))
        except ValueError as e:
            raise Exception("Problem decoding token response {0}".format(e))
        except KeyError as e:
            raise Exception("id_token not in response {0}".format(e))
        return self._id_token

    def _write_token(self):
        """Attempts to write the passed token to the given user directory."""

        credentials_path = self._credentials_path
        dirname = os.path.dirname(credentials_path)

        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise Exception("Error creating directory %s: %s" % (dirname, e))

        file_content = json.dumps({"refresh_token": self._refresh_token})
        if os.path.exists(credentials_path):
            # Remove file because os.open will not change permissions of existing files
            os.remove(credentials_path)
        with os.fdopen(
            os.open(credentials_path, os.O_WRONLY | os.O_CREAT, 0o600), "w"
        ) as f:
            f.write(file_content)

    def _in_colab_shell(self):
        """Tests if the code is being executed within Google Colab."""
        try:
            import google.colab  # pylint: disable=unused-variable  # noqa

            return True
        except ImportError:
            return False

    def _in_jupyter_shell(self):
        """Tests if the code is being executed within Jupyter."""
        try:
            import ipykernel.zmqshell

            return isinstance(
                IPython.get_ipython(), ipykernel.zmqshell.ZMQInteractiveShell
            )
        except ImportError:
            return False
        except NameError:
            return False

    def _obtain_and_write_token(self, auth_code=None, code_verifier=None):
        """Obtains and writes credentials token based on a authorization code."""
        if not auth_code:
            auth_code = input("Enter verification code: ")
        assert isinstance(auth_code, six.string_types)
        self._request_token(auth_code.strip(), code_verifier)
        print("\nSuccessfully saved authorization token.")

    def _display_auth_instructions_with_html(self, auth_url):
        """Displays instructions for authenticating using HTML code."""
        try:
            IPython.display.display(
                IPython.display.HTML(
                    """<p>To authorize access needed by Geodesic, open the following
                URL in a web browser and follow the instructions:</p>
                <p><a href={0}>{0}</a></p>
                <p>The authorization workflow will generate a code, which you
                should paste in the box below</p>
                """.format(
                        auth_url
                    )
                )
            )
        except NameError:
            print("The IPython module must be installed to use HTML.")
            raise

    def _display_auth_instructions_for_noninteractive(self, auth_url, code_verifier):
        """Displays instructions for authenticating without blocking for user input."""
        print(
            "Paste the following address into a web browser:\n"
            "\n"
            "    {0}\n"
            "\n"
            "On the web page, please authorize access to your "
            "Geodesic using your Google account and copy the authentication code. "
            "Next authenticate with the following command:\n"
            "\n"
            "    geodesic authenticate --code-verifier={1} "
            "--authorization-code=PLACE_AUTH_CODE_HERE\n".format(
                auth_url, six.ensure_str(code_verifier)
            )
        )

    def _display_auth_instructions_with_print(self, auth_url):
        """Displays instructions for authenticating using a print statement."""
        print(
            "To authorize access needed by Geodesic, open the following "
            "URL in a web browser and follow the instructions. If the web "
            "browser does not start automatically, please manually browse the "
            "URL below.\n"
            "\n"
            "    {0}\n"
            "\n"
            "The authorization workflow will generate a code, which you "
            "should paste in the box below. ".format(auth_url)
        )

    def authenticate(
        self, cli_authorization_code=None, quiet=False, cli_code_verifier=None
    ):
        """Prompts the user to authorize access to Geodesic via OAuth2.

        Args:
            cli_authorization_code: An optional authorization code.  Supports CLI mode,
                where the code is passed as an argument to `geodesic authenticate`.
            quiet: If true, do not require interactive prompts.
            cli_code_verifier: PKCE verifier to prevent auth code stealing.  Must be
                provided if cli_authorization_code is given.

        """

        if cli_authorization_code:
            self._obtain_and_write_token(cli_authorization_code, cli_code_verifier)
            return

        # PKCE.  Generates a challenge that the server will use to ensure that the
        # auth_code only works with Google verifier.  https://tools.ietf.org/html/rfc7636
        code_verifier = _base64param(os.urandom(32))
        code_challenge = _base64param(hashlib.sha256(code_verifier).digest())
        auth_url = self.get_authorization_url(code_challenge)

        if quiet:
            self._display_auth_instructions_for_noninteractive(auth_url, code_verifier)
            webbrowser.open_new(auth_url)
            return

        if self._in_colab_shell():
            if sys.version_info[0] == 2:  # Python 2
                self._display_auth_instructions_for_noninteractive(
                    auth_url, code_verifier
                )
                return
            else:  # Python 3
                self._display_auth_instructions_with_print(auth_url)
        elif self._in_jupyter_shell():
            self._display_auth_instructions_with_html(auth_url)
        else:
            self._display_auth_instructions_with_print(auth_url)

        webbrowser.open_new(auth_url)

        self._obtain_and_write_token(None, code_verifier)  # Will prompt for auth_code.


def _base64param(byte_string):
    """Encodes bytes for use as a URL parameter."""
    return base64.urlsafe_b64encode(byte_string).rstrip(b"=")
