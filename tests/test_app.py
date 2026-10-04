import hashlib
import hmac
import io
import json
import unittest
from app import add_label, make_app, route, validate_origin

with open("examples/issue.json", encoding="utf-8") as source:
    EVENT = json.load(source)
LABELS = {"bug": 1, "feature": 2, "question": 3}

class ForgejoTests(unittest.TestCase):
    def test_review_first_and_explicit_apply(self):
        writes = []
        preview = route(EVENT, "example/reviews", LABELS, evaluate=lambda _: ("bug", .96),
                        write_label=lambda *args: writes.append(args))
        self.assertEqual(preview["status"], "preview")
        self.assertEqual(writes, [])
        review = route(EVENT, "example/reviews", LABELS, evaluate=lambda _: ("bug", .5),
                       apply=True, write_label=lambda *args: writes.append(args))
        self.assertEqual(review["outcome"], "review")
        self.assertEqual(writes, [])
        applied = route(EVENT, "example/reviews", LABELS, evaluate=lambda _: ("bug", .96),
                        apply=True, write_label=lambda *args: writes.append(args))
        self.assertEqual(applied["status"], "labeled")
        self.assertEqual(writes, [("example", "reviews", 17, 1)])

    def test_signed_webhook_and_invalid_signature(self):
        calls = []
        app = make_app("secret", "example/reviews", LABELS,
                       evaluate=lambda text: calls.append(text) or ("bug", .96))
        body = json.dumps(EVENT).encode()
        valid = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
        def invoke(signature):
            status = []
            env = {"REQUEST_METHOD": "POST", "PATH_INFO": "/webhook", "CONTENT_LENGTH": str(len(body)),
                   "wsgi.input": io.BytesIO(body), "HTTP_X_FORGEJO_SIGNATURE": signature,
                   "HTTP_X_FORGEJO_EVENT": "issues"}
            output = b"".join(app(env, lambda value, headers: status.append(value)))
            return status[0], output
        self.assertEqual(invoke("bad")[0], "401 Unauthorized")
        self.assertEqual(calls, [])
        status, output = invoke(valid)
        self.assertEqual(status, "200 OK")
        self.assertNotIn(b"payment", output)
        self.assertEqual(len(calls), 1)

    def test_url_and_api_request(self):
        with self.assertRaises(ValueError):
            validate_origin("http://remote.example")
        requests = []
        class Response(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *_): self.close()
        def opener(request, timeout):
            requests.append((request, timeout))
            return Response(b'[]')
        add_label("https://forge.example", "token", "example", "reviews", 17, 1, opener=opener)
        self.assertEqual(requests[0][0].full_url,
                         "https://forge.example/api/v1/repos/example/reviews/issues/17/labels")
        self.assertEqual(json.loads(requests[0][0].data), {"labels": [1]})
