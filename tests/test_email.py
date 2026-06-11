"""Tests for email_service.py — HTML rendering, skip behavior, and error handling."""
import email
import os
import pytest
from unittest.mock import MagicMock, patch


def _decode_mime(msg_str: str) -> str:
    """Parse a raw MIME string and return decoded text content."""
    msg = email.message_from_string(msg_str)
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/html", "text/plain"):
                payload = part.get_payload(decode=True)
                if payload:
                    parts.append(payload.decode("utf-8", errors="replace"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            parts.append(payload.decode("utf-8", errors="replace"))
    # Also include headers (Subject, From, To) in searchable text
    parts.append(str(msg))
    return "\n".join(parts)


SAMPLE_RECIPE = {
    "id": 1,
    "title": "Palak Paneer Test",
    "description": "Creamy spinach curry with paneer.",
    "cuisine_tag": "indian",
    "nutrition_tags": ["protein-rich", "iron-rich"],
    "dietary_tags": ["vegetarian"],
    "spice_level": 3,
    "servings": 4,
    "prep_time_min": 10,
    "cook_time_min": 25,
    "ingredients": [
        {"name": "Spinach", "quantity": "2", "unit": "cups"},
        {"name": "Paneer", "quantity": "200", "unit": "g"},
    ],
    "instructions": ["Blanch spinach.", "Add paneer and simmer."],
    "allergen_notes": "",
    "image_url": "/static/images/palak_paneer.jpg",
    "generated_at": "Apr 27, 2026",
    "source": "on_demand",
}


# ═══════════════════════════════════════════════════════════════════════════════
# SKIP WHEN CREDENTIALS MISSING
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmailSkipBehavior:

    def test_skips_when_no_credentials(self, monkeypatch):
        monkeypatch.delenv("EMAIL_USER", raising=False)
        monkeypatch.delenv("EMAIL_PASSWORD", raising=False)
        from email_service import send_recipe_email
        result = send_recipe_email(SAMPLE_RECIPE, "to@example.com")
        assert result is False

    def test_skips_when_user_empty(self, monkeypatch):
        monkeypatch.setenv("EMAIL_USER", "")
        monkeypatch.setenv("EMAIL_PASSWORD", "somepassword")
        from email_service import send_recipe_email
        result = send_recipe_email(SAMPLE_RECIPE, "to@example.com")
        assert result is False

    def test_skips_when_password_empty(self, monkeypatch):
        monkeypatch.setenv("EMAIL_USER", "from@example.com")
        monkeypatch.setenv("EMAIL_PASSWORD", "")
        from email_service import send_recipe_email
        result = send_recipe_email(SAMPLE_RECIPE, "to@example.com")
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL SENDING (SMTP MOCKED)
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmailSend:

    @pytest.fixture(autouse=True)
    def set_credentials(self, monkeypatch):
        monkeypatch.setenv("EMAIL_USER", "sender@example.com")
        monkeypatch.setenv("EMAIL_PASSWORD", "testpassword")
        monkeypatch.setenv("EMAIL_HOST", "smtp.example.com")
        monkeypatch.setenv("EMAIL_PORT", "587")

    def test_returns_true_on_success(self):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
            from email_service import send_recipe_email
            result = send_recipe_email(SAMPLE_RECIPE, "to@example.com")
            assert result is True

    def test_calls_sendmail_with_correct_recipient(self):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
            from email_service import send_recipe_email
            send_recipe_email(SAMPLE_RECIPE, "recipient@example.com")
            mock_server.sendmail.assert_called_once()
            args = mock_server.sendmail.call_args[0]
            assert args[1] == "recipient@example.com"

    def test_returns_false_on_smtp_failure(self):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = Exception("Connection refused")
            from email_service import send_recipe_email
            result = send_recipe_email(SAMPLE_RECIPE, "to@example.com")
            assert result is False

    def test_does_not_raise_on_smtp_failure(self):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = Exception("SMTP error")
            from email_service import send_recipe_email
            # Should not raise — failure should be handled gracefully
            try:
                send_recipe_email(SAMPLE_RECIPE, "to@example.com")
            except Exception:
                pytest.fail("send_recipe_email raised an exception on SMTP failure")


# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmailContent:

    @pytest.fixture(autouse=True)
    def set_credentials(self, monkeypatch):
        monkeypatch.setenv("EMAIL_USER", "sender@example.com")
        monkeypatch.setenv("EMAIL_PASSWORD", "testpassword")

    def _capture_email_body(self):
        captured = {}
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            def capture_sendmail(from_addr, to_addr, msg_str):
                captured["msg"] = msg_str

            mock_server.sendmail.side_effect = capture_sendmail
            from email_service import send_recipe_email
            send_recipe_email(SAMPLE_RECIPE, "to@example.com", base_url="http://localhost:8080")
        return _decode_mime(captured.get("msg", ""))

    def test_email_contains_recipe_title(self):
        body = self._capture_email_body()
        assert "Palak Paneer Test" in body

    def test_email_contains_ingredient(self):
        body = self._capture_email_body()
        assert "Spinach" in body

    def test_email_contains_instruction(self):
        body = self._capture_email_body()
        assert "Blanch spinach" in body

    def test_email_contains_recipe_link(self):
        body = self._capture_email_body()
        assert "/recipe/1" in body

    def test_email_subject_contains_title(self):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
            captured = {}

            def capture(from_addr, to_addr, msg_str):
                captured["msg"] = msg_str

            mock_server.sendmail.side_effect = capture
            from email_service import send_recipe_email
            send_recipe_email(SAMPLE_RECIPE, "to@example.com")
            assert "Palak Paneer Test" in _decode_mime(captured.get("msg", ""))

    def test_email_handles_empty_allergen_notes(self):
        recipe = dict(SAMPLE_RECIPE, allergen_notes="")
        body = self._capture_email_body()
        # Should render without error even with empty allergen notes
        assert "Palak Paneer Test" in body

    def test_email_includes_allergen_note_when_present(self):
        recipe_with_allergen = dict(SAMPLE_RECIPE, allergen_notes="Cut paneer into small cubes for young children.")
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
            captured = {}

            def capture(from_addr, to_addr, msg_str):
                captured["msg"] = msg_str

            mock_server.sendmail.side_effect = capture
            from email_service import send_recipe_email
            send_recipe_email(recipe_with_allergen, "to@example.com")
            assert "Cut paneer" in _decode_mime(captured.get("msg", ""))
