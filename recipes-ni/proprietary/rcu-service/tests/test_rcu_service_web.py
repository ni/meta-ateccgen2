import http.client
import importlib.util
import json
import threading
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "files" / "rcu-service-web.py"
SPEC = importlib.util.spec_from_file_location("rcu_service_web", SCRIPT_PATH)
WEB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WEB)


class FakeEnum:
    def __init__(self, values):
        self.values = values

    def keys(self):
        return self.values.keys()

    def Value(self, name):
        return self.values[name]


class FakeProto:
    RcuRestartType = FakeEnum({"SERVICE_LEVEL_RESTART": 7})
    PowerState = FakeEnum({"POWER_STATE_RUNNING": 9})
    Attribute = FakeEnum({"Attr_UTF8_RcuImageVersion": 400})


class FakeClient:
    STUB = object()

    def __init__(self):
        self.channel_passwords = []
        self.restart_calls = []
        self.power_calls = []
        self.attribute_calls = []

    def initiate_channel(self, address, port=50051, cert_path=None, password=""):
        self.channel_passwords.append(password)
        if password != "ni":
            raise PermissionError("invalid password")

    def get_attribute(self, attribute, index):
        self.attribute_calls.append((attribute, index))
        return "test-version"

    def initiate_restart(self, value):
        self.restart_calls.append(value)

    def request_rack_power_state(self, value):
        self.power_calls.append(value)


class RcuServiceWebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = FakeClient()
        WEB.rcupyclient = cls.client
        WEB.rcu_service_pb2 = FakeProto
        cls.server = WEB.ThreadingHTTPServer(("127.0.0.1", 0), WEB.RcuServiceWebHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.port = cls.server.server_address[1]
        WEB.RCU_SERVICE_ADDR = "127.0.0.1"
        WEB.RCU_SERVICE_PORT = cls.port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        payload = response.read()
        response_headers = dict(response.getheaders())
        connection.close()
        return response.status, response_headers, payload

    def login(self):
        status, headers, _ = self.request(
            "POST",
            "/login",
            body="password=ni",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(status, 303)
        self.assertIn("SameSite=Strict", headers["Set-Cookie"])
        return headers["Set-Cookie"].split(";", 1)[0]

    def test_login_and_protected_dashboard(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b'name="password"', body)

        status, _, body = self.request("GET", "/api/health")
        self.assertEqual(status, 401)
        self.assertEqual(json.loads(body), {"error": "not authorized"})

        status, _, body = self.request(
            "POST",
            "/login",
            body="password=wrong",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(status, 401)
        self.assertIn(b"Login failed: invalid password", body)
        self.assertEqual(self.client.channel_passwords[-1], "wrong")

        status, _, body = self.request(
            "POST",
            "/login",
            body="password=%3Cscript%3Ealert%281%29%3C%2Fscript%3E",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(status, 401)
        self.assertIn(b"Login failed: invalid password", body)

        cookie = self.login()
        self.assertEqual(self.client.channel_passwords[-1], "ni")
        status, _, body = self.request("GET", "/", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertIn(b"RCU Service Dashboard", body)

        status, _, body = self.request("GET", "/api/health", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["version"], "test-version")
        self.assertIn((400, 0), self.client.attribute_calls)

    def test_authenticated_actions_use_named_enum_values_once(self):
        cookie = self.login()
        self.client.restart_calls.clear()
        self.client.power_calls.clear()
        headers = {"Content-Type": "application/json", "Cookie": cookie}

        status, _, _ = self.request("POST", "/api/restart", json.dumps({"type": "service"}), headers)
        self.assertEqual(status, 200)
        self.assertEqual(self.client.restart_calls, [7])

        status, _, _ = self.request("POST", "/api/power", json.dumps({"state": "running"}), headers)
        self.assertEqual(status, 200)
        self.assertEqual(self.client.power_calls, [9])

    def test_logout_expires_session_cookie(self):
        cookie = self.login()
        status, headers, _ = self.request("GET", "/logout", headers={"Cookie": cookie})
        self.assertEqual(status, 303)
        self.assertIn("expires=Thu, 01 Jan 1970 00:00:00 GMT", headers["Set-Cookie"])


if __name__ == "__main__":
    unittest.main()
