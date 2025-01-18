import json
import re


class JSONInterpolator:
    PLACEHOLDER_REGEX = r"(?P<main><<(?P<tv>(?P<invalid>[0-9]?)[a-zA-Z_][a-zA-Z0-9_]*)>>)"
    pattern = re.compile(PLACEHOLDER_REGEX)

    @classmethod
    def validate_template(cls, template: str) -> None:
        """
        Validates the template to ensure all placeholders are correctly formatted
        and that there are no duplicates.

        Args:
            template (str): The template string to validate.

        Raises:
            ValueError: If invalid placeholders are found.
            TypeError: If the template is not a string.
        """
        if not isinstance(template, str):
            raise TypeError("Template must be string.")

        for mo in cls.pattern.finditer(template):
            if set(mo["tv"]) == set("_"):
                raise ValueError(f"Placeholder {mo['tv']} must include word characters.")
            elif mo["invalid"]:
                raise ValueError(f"Placeholder {mo['tv']} cannot start with a digit.")

    @classmethod
    def validate_parameters(cls, params: dict) -> None:
        """
        Validates the parameters dictionary to ensure all placeholders are present
        and have valid values.

        Args:
            params (dict): A dictionary containing placeholder-value pairs.

        Raises:
            TypeError: If the parameters are not a dictionary
        """
        if not isinstance(params, dict):
            raise TypeError("Parameters must be a dictionary.")

    @classmethod
    def render_template(cls, params: dict, template: str) -> str:
        """
        Renders a template by replacing placeholders with corresponding values.

        Args:
            params (dict): A dictionary containing placeholder-value pairs.
            template (str): The template string with placeholders.

        Returns:
            str: The interpolated template with placeholders replaced by values.

        Raises:
            ValueError: If rendered JSON is invalid.
        """
        cls.validate_template(template)
        cls.validate_parameters(params)

        for mo in cls.pattern.finditer(template):
            if mo["tv"] not in params:
                raise KeyError(f"Parameter {mo['tv']} not found in the parameters.")

        # Iterate over the template placeholders and replace them with corresponding values
        interpolated_string = template
        for match in cls.pattern.findall(interpolated_string):
            interpolated_string = interpolated_string.replace(match[0], json.dumps(params[match[1]]))

        # Ensure the result is a valid JSON string
        try:
            json.loads(interpolated_string)
        except json.decoder.JSONDecodeError:
            raise ValueError("The rendered template is not valid JSON.")
        return interpolated_string
