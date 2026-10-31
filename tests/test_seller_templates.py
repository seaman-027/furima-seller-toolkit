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


if __name__ == "__main__":
    unittest.main()
