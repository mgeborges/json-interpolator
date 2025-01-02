import json
import unittest

from src.json_interpolator.interpolator import JSONInterpolator


class TestTemplateFunctions(unittest.TestCase):
    def test_valid_template(self):
        template = '{"name": "<<name>>", "age": <<age>>}'
        JSONInterpolator.validate_template(template)  # Should not raise any exception

    def test_list(self):
        template = '{"names": <<names>>}'
        params = {"names": ["Alice", "Bob"]}
        expected = json.loads('{"names": ["Alice", "Bob"]}')
        result = json.loads(JSONInterpolator.render_template(params, template))
        self.assertEqual(result, expected)

    def test_duplicate_placeholders(self):
        template = '{"name": "<<name>>", "duplicate": "<<name>>"}'
        with self.assertRaises(ValueError) as context:
            JSONInterpolator.validate_template(template)
        self.assertIn("Duplicate placeholders found", str(context.exception))

    def test_invalid_placeholder_name_underscore(self):
        template = '{"invalid": "<<__>>"}'
        with self.assertRaises(ValueError) as context:
            JSONInterpolator.validate_template(template)
        self.assertIn("must include word characters", str(context.exception))

    def test_invalid_placeholder_name_digit_start(self):
        template = '{"invalid": "<<1name>>"}'
        with self.assertRaises(ValueError) as context:
            JSONInterpolator.validate_template(template)
        self.assertIn("cannot start with a digit", str(context.exception))

    def test_render_template_success(self):
        template = '{"name": "<<name>>", "age": <<age>>}'
        params = {"name": "John Doe", "age": 30}
        expected = '{"name": "John Doe", "age": 30}'
        result = JSONInterpolator.render_template(params, template)
        self.assertEqual(result, expected)

    def test_render_template_missing_param(self):
        template = '{"name": "<<name>>", "age": <<age>>}'
        params = {"name": "John Doe"}
        with self.assertRaises(KeyError):
            JSONInterpolator.render_template(params, template)

    def test_render_template_extra_param(self):
        template = '{"name": "<<name>>"}'
        params = {"name": "John Doe", "age": 30}
        expected = '{"name": "John Doe"}'
        result = JSONInterpolator.render_template(params, template)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
