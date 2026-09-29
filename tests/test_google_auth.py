import os
import unittest
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.auth.exceptions import TransportError

from database.enums import UserRole
from database.models import Base, User, UserAuthIdentity
from services.user import (
    GoogleAuthError,
    userGoogleLogin,
    userLinkGoogleIdentity,
    userModifyPassword,
    verifyGoogleCredential,
)


class GoogleAuthTest(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test-client-id"})
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("GOOGLE_ORG_ALLOW_LIST", None)
        signing = patch.multiple("services.user", ALGORITHM="HS256", SECRET_KEY="test-signing-secret")
        signing.start()
        self.addCleanup(signing.stop)
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    @staticmethod
    def google_payload(subject="google-subject", email="user@example.com"):
        return {
            "iss": "https://accounts.google.com",
            "sub": subject,
            "email": email,
            "email_verified": True,
            "name": "Google User",
        }

    def test_google_login_creates_guest_user_and_reuses_identity(self):
        with patch(
            "services.user.verifyGoogleCredential",
            return_value=self.google_payload(),
        ):
            first = userGoogleLogin(self.session, "credential")
            second = userGoogleLogin(self.session, "credential")

        self.assertEqual(200, first["status"])
        self.assertEqual(200, second["status"])
        self.assertEqual(1, self.session.query(User).count())
        self.assertEqual(1, self.session.query(UserAuthIdentity).count())
        user = self.session.query(User).one()
        self.assertEqual(UserRole.GUEST, user.role)
        self.assertIsNone(user.password)
        self.assertFalse(user.toJson()["has_password"])
        self.assertEqual(["google"], user.toJson()["auth_providers"])

    def test_google_login_requires_link_when_email_exists(self):
        self.session.add(
            User(
                username="local-user",
                password=User.hashPassword("password"),
                nickname="Local User",
                email="user@example.com",
                role=UserRole.GUEST,
            )
        )
        self.session.commit()

        with patch(
            "services.user.verifyGoogleCredential",
            return_value=self.google_payload(),
        ):
            with self.assertRaises(GoogleAuthError) as context:
                userGoogleLogin(self.session, "credential")

        self.assertEqual(409, context.exception.http_status)
        self.assertEqual("ACCOUNT_LINK_REQUIRED", context.exception.code)
        self.assertEqual(0, self.session.query(UserAuthIdentity).count())

    def test_authenticated_user_can_link_matching_google_email(self):
        user = User(
            username="local-user",
            password=User.hashPassword("password"),
            nickname="Local User",
            email="user@example.com",
            role=UserRole.GUEST,
        )
        self.session.add(user)
        self.session.commit()

        with patch(
            "services.user.verifyGoogleCredential",
            return_value=self.google_payload(),
        ):
            response = userLinkGoogleIdentity(
                self.session,
                user.id,
                "credential",
            )

        self.assertEqual(200, response["status"])
        identity = self.session.query(UserAuthIdentity).one()
        self.assertEqual(user.id, identity.user_id)

    def test_google_only_user_can_set_local_password_without_old_password(self):
        user = User(
            username="google-user",
            password=None,
            nickname="Google User",
            email="user@example.com",
            role=UserRole.GUEST,
        )
        self.session.add(user)
        self.session.commit()

        response = userModifyPassword(
            self.session,
            user.id,
            "",
            "new-password",
        )

        self.assertEqual(200, response["status"])
        self.assertEqual("Set password success", response["message"])
        self.session.refresh(user)
        self.assertTrue(user.checkPassword("new-password"))

    def test_google_only_user_cannot_set_password_with_nonempty_old_password(self):
        user = User(
            username="google-user",
            password=None,
            nickname="Google User",
            email="user@example.com",
            role=UserRole.GUEST,
        )
        self.session.add(user)
        self.session.commit()

        response = userModifyPassword(
            self.session,
            user.id,
            "unexpected-old-password",
            "new-password",
        )

        self.assertEqual(-4, response["status"])
        self.session.refresh(user)
        self.assertIsNone(user.password)

    def test_local_password_user_cannot_bypass_old_password_check_with_empty_value(self):
        user = User(
            username="local-user",
            password=User.hashPassword("old-password"),
            nickname="Local User",
            email="user@example.com",
            role=UserRole.GUEST,
        )
        self.session.add(user)
        self.session.commit()

        response = userModifyPassword(
            self.session,
            user.id,
            "",
            "new-password",
        )

        self.assertEqual(-2, response["status"])
        self.session.refresh(user)
        self.assertTrue(user.checkPassword("old-password"))
        self.assertFalse(user.checkPassword("new-password"))

    def test_google_credential_verification_checks_issuer_and_domain(self):
        payload = self.google_payload()
        with (
            patch.dict(
                os.environ,
                {
                    "GOOGLE_CLIENT_ID": "test-client-id",
                    "GOOGLE_ORG_ALLOW_LIST": '["example.com"]',
                },
                clear=False,
            ),
            patch(
                "services.user.google_id_token.verify_oauth2_token",
                return_value={**payload, "hd": "example.com"},
            ) as verifier,
        ):
            response = verifyGoogleCredential("credential")

        self.assertEqual(payload["sub"], response["sub"])
        self.assertEqual("test-client-id", verifier.call_args.args[2])

    def test_allow_list_accepts_multiple_domains(self):
        with (
            patch.dict(os.environ, {
                "GOOGLE_ORG_ALLOW_LIST": '[" example.com ", "EXAMPLE.ORG"]',
            }),
            patch("services.user.google_id_token.verify_oauth2_token") as verifier,
        ):
            for domain in ("example.com", "example.org"):
                with self.subTest(domain=domain):
                    verifier.return_value = {
                        **self.google_payload(email=f"user@{domain.upper()}"),
                        "hd": domain,
                    }
                    self.assertEqual(domain, verifyGoogleCredential("credential")["hd"])

    def test_allow_list_rejects_missing_hd_external_email_and_suffix_matches(self):
        with (
            patch.dict(os.environ, {"GOOGLE_ORG_ALLOW_LIST": '["example.com"]'}),
            patch("services.user.google_id_token.verify_oauth2_token") as verifier,
        ):
            for hd, email in (
                (None, "user@example.com"),
                ("other.example", "user@example.com"),
                ("example.com", "user@other.example"),
                ("example.com.evil.test", "user@example.com.evil.test"),
                ("sub.example.com", "user@sub.example.com"),
            ):
                with self.subTest(hd=hd, email=email):
                    verifier.return_value = {**self.google_payload(email=email), "hd": hd}
                    with self.assertRaises(GoogleAuthError) as context:
                        verifyGoogleCredential("credential")
                    self.assertEqual(403, context.exception.http_status)
                    self.assertEqual("GOOGLE_DOMAIN_NOT_ALLOWED", context.exception.code)

    def test_invalid_allow_list_fails_closed_before_verification(self):
        for raw in ('', 'example.com', 'null', '{}', '"example.com"', '[1]', '[""]', '[" "]'):
            with (
                self.subTest(raw=raw),
                patch.dict(os.environ, {"GOOGLE_ORG_ALLOW_LIST": raw}),
                patch("services.user.google_id_token.verify_oauth2_token") as verifier,
            ):
                with self.assertRaises(GoogleAuthError) as context:
                    verifyGoogleCredential("credential")
                self.assertEqual(503, context.exception.http_status)
                self.assertEqual("GOOGLE_AUTH_NOT_CONFIGURED", context.exception.code)
                verifier.assert_not_called()

    def test_empty_allow_list_rejects_all_accounts(self):
        with (
            patch.dict(os.environ, {"GOOGLE_ORG_ALLOW_LIST": '[]'}),
            patch("services.user.google_id_token.verify_oauth2_token",
                  return_value={**self.google_payload(), "hd": "example.com"}),
        ):
            with self.assertRaises(GoogleAuthError) as context:
                verifyGoogleCredential("credential")
            self.assertEqual(403, context.exception.http_status)

    def test_unset_domain_configuration_preserves_unrestricted_login(self):
        with patch("services.user.google_id_token.verify_oauth2_token",
                   return_value=self.google_payload()):
            self.assertEqual("user@example.com", verifyGoogleCredential("credential")["email"])

    def test_restricted_login_and_link_do_not_write_or_issue_tokens(self):
        with (
            patch.dict(os.environ, {"GOOGLE_ORG_ALLOW_LIST": '["allowed.example"]'}),
            patch("services.user.google_id_token.verify_oauth2_token",
                  return_value={**self.google_payload(), "hd": "example.com"}),
            patch("services.user.createAccessToken") as issue_token,
        ):
            for action in (
                lambda: userGoogleLogin(self.session, "credential"),
                lambda: userLinkGoogleIdentity(self.session, 1, "credential"),
            ):
                with self.assertRaises(GoogleAuthError) as context:
                    action()
                self.assertEqual(403, context.exception.http_status)
            issue_token.assert_not_called()
            self.assertEqual(0, self.session.query(User).count())
            self.assertEqual(0, self.session.query(UserAuthIdentity).count())

    def test_google_credential_rejects_unverified_email(self):
        with (
            patch.dict(
                os.environ,
                {"GOOGLE_CLIENT_ID": "test-client-id"},
                clear=False,
            ),
            patch(
                "services.user.google_id_token.verify_oauth2_token",
                return_value={
                    **self.google_payload(),
                    "email_verified": False,
                },
            ),
        ):
            with self.assertRaises(GoogleAuthError) as context:
                verifyGoogleCredential("credential")

        self.assertEqual(401, context.exception.http_status)
        self.assertEqual("UNVERIFIED_GOOGLE_ACCOUNT", context.exception.code)

    def test_google_credential_maps_transport_failure_to_service_unavailable(self):
        with (
            patch.dict(
                os.environ,
                {"GOOGLE_CLIENT_ID": "test-client-id"},
                clear=False,
            ),
            patch(
                "services.user.google_id_token.verify_oauth2_token",
                side_effect=TransportError("network unavailable"),
            ),
        ):
            with self.assertRaises(GoogleAuthError) as context:
                verifyGoogleCredential("credential")

        self.assertEqual(503, context.exception.http_status)
        self.assertEqual("GOOGLE_AUTH_UNAVAILABLE", context.exception.code)


if __name__ == "__main__":
    unittest.main()
