import json
import unittest

from src.json_interpolator.interpolator import JSONInterpolator


class TestTemplateFunctions(unittest.TestCase):
    #
    # Template validation tests

    def test_valid_template(self):
        template = '{"name": "<<name>>", "age": <<age>>}'
        JSONInterpolator.validate_template(template)  # Should not raise any exception

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

    def test_template_is_not_str(self):
        template = {"name": "<<name>>"}
        with self.assertRaises(TypeError):
            JSONInterpolator.validate_template(template)  # type: ignore

    #
    # Rendering tests

    def test_render_template_success(self):
        template = '{"name": <<name>>, "age": <<age>>}'
        params = {"name": "Alice", "age": 30}
        expected = '{"name": "Alice", "age": 30}'
        result = JSONInterpolator.render_template(params, template)
        self.assertEqual(result, expected)

    def test_render_template_missing_param(self):
        template = '{"name": <<name>>, "age": <<age>>}'
        params = {"name": "Alice"}
        with self.assertRaises(KeyError):
            JSONInterpolator.render_template(params, template)

    def test_render_template_extra_param(self):
        template = '{"name": <<name>>}'
        params = {"name": "Alice", "age": 30}
        expected = '{"name": "Alice"}'
        result = JSONInterpolator.render_template(params, template)
        self.assertEqual(result, expected)

    def test_render_template_duplicate_placeholders(self):
        template = '{"name": <<name>>, "same_name_again": <<name>>}'
        params = {"name": "Alice"}
        expected = '{"name": "Alice", "same_name_again": "Alice"}'
        result = JSONInterpolator.render_template(params, template)
        self.assertEqual(result, expected)

    def test_params_is_not_dict(self):
        template = '{"person": <<person>>}'
        params = '{"person": {"name": "Alice", "age": 30}}'
        with self.assertRaises(TypeError):
            JSONInterpolator.render_template(params, template)  # type: ignore

    def test_template_is_not_valid_json(self):
        template = '{"name": "<<name>>", "age": <<age>>'
        params = {"name": "Alice", "age": 30}
        with self.assertRaises(ValueError):
            JSONInterpolator.render_template(params, template)

    def test_list_is_valid(self):
        template = '{"names": <<names>>}'
        params = {"names": ["Alice", "Bob"]}
        expected = json.loads('{"names": ["Alice", "Bob"]}')
        result = json.loads(JSONInterpolator.render_template(params, template))
        self.assertEqual(result, expected)

    def test_dict_is_valid(self):
        template = '{"person": <<person>>}'
        params = {"person": {"name": "Alice", "age": 30}}
        expected = json.loads('{"person": {"name": "Alice", "age": 30}}')
        result = json.loads(JSONInterpolator.render_template(params, template))
        self.assertEqual(result, expected)

    def test_bool_is_valid(self):
        template = '{"is_valid": <<is_valid>>}'
        params = {"is_valid": True}
        expected = json.loads('{"is_valid": true}')
        result = json.loads(JSONInterpolator.render_template(params, template))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
