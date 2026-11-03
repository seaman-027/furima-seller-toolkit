"""Unit tests for seller_templates.py (run: python -m unittest discover tests)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import seller_templates as st


class TestVariables(unittest.TestCase):
    def test_extract_in_first_use_order(self):
        text = "こんにちは{name}さん、{item}について{name}です"
        self.assertEqual(st.template_variables(text), ["name", "item"])

    def test_no_variables(self):
        self.assertEqual(st.template_variables("変数なし"), [])


class TestRender(unittest.TestCase):
    def test_fills_known_values(self):
        out = st.render("{item}を発送しました", {"item": "スカーフ"})
        self.assertEqual(out, "スカーフを発送しました")

    def test_leaves_unknown_placeholders(self):
        out = st.render("{item} / {method}", {"item": "スカーフ"})
        self.assertEqual(out, "スカーフ / {method}")


class TestTemplates(unittest.TestCase):
    def test_all_templates_load(self):
        names = st.list_templates()
        self.assertIn("out_of_stock", names)
        for name in names:
            self.assertTrue(st.load_template(name).strip())

    def test_out_of_stock_variables(self):
        text = st.load_template("out_of_stock")
        for var in ("item_name", "alt_item", "alt_detail", "alt_price"):
            self.assertIn(var, st.template_variables(text))

    def test_price_accept_variables(self):
        text = st.load_template("price_accept")
        for var in ("item_name", "price"):
            self.assertIn(var, st.template_variables(text))

    def test_return_consultation_variables(self):
        text = st.load_template("return_consultation")
        for var in ("item_name", "response_days"):
            self.assertIn(var, st.template_variables(text))

    def test_bundle_consultation_variables(self):
        text = st.load_template("bundle_consultation")
        for var in ("item_names", "bundle_price", "shipping_note"):
            self.assertIn(var, st.template_variables(text))

    def test_shipping_done_platform_variable(self):
        text = st.load_template("shipping_done")
        self.assertIn("platform", st.template_variables(text))

    def test_return_consultation_platform_variable(self):
        text = st.load_template("return_consultation")
        self.assertIn("platform", st.template_variables(text))

    def test_cancel_request_platform_variable(self):
        text = st.load_template("cancel_request")
        self.assertIn("platform", st.template_variables(text))


class TestPlatform(unittest.TestCase):
    def test_resolve_known_platforms(self):
        self.assertEqual(st.resolve_platform("mercari"), "メルカリ")
        self.assertEqual(st.resolve_platform("rakuma"), "ラクマ")
        self.assertEqual(st.resolve_platform("yahoo"), "Yahoo!フリマ")

    def test_resolve_unknown_platform_fails(self):
        with self.assertRaises(SystemExit):
            st.resolve_platform("unknown-shop")

    def test_render_platform_option_fills_placeholder(self):
        import contextlib
        import io

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = st.main(
                ["render", "shipping_done", "--platform", "yahoo",
                 "--set", "method=おてがる配送"]
            )
        self.assertEqual(code, 0)
        self.assertIn("Yahoo!フリマで受取評価", out.getvalue())
        self.assertNotIn("{platform}", out.getvalue())

    def test_render_cancel_request_platform_option(self):
        import contextlib
        import io

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = st.main(
                ["render", "cancel_request", "--platform", "rakuma"]
            )
        self.assertEqual(code, 0)
        self.assertIn("ラクマのルール", out.getvalue())
        self.assertNotIn("{platform}", out.getvalue())

    def test_explicit_set_platform_wins_over_option(self):
        import contextlib
        import io

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            st.main(
                ["render", "shipping_done", "--platform", "yahoo",
                 "--set", "method=おてがる配送",
                 "--set", "platform=メルカリ"]
            )
        self.assertIn("メルカリで受取評価", out.getvalue())


if __name__ == "__main__":
    unittest.main()
