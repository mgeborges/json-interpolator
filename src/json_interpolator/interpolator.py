import re


class JSONInterpolator:
    PLACEHOLDER_REGEX = r"(?P<main><<(?P<tv>(?P<invalid>[0-9]?)[a-zA-Z_][a-zA-Z0-9_]*)>>)"
    pattern = re.compile(PLACEHOLDER_REGEX)

    @classmethod
    def validate_template(cls, template):
        """
        Validates the template to ensure all placeholders are correctly formatted
        and that there are no duplicates.

        Args:
            template (str): The template string to validate.

        Raises:
            ValueError: If duplicate or invalid placeholders are found.
        """
        placeholders = cls.pattern.findall(template)
        if len(set(placeholders)) != len(placeholders):
            raise ValueError("Duplicate placeholders found in the JSON file.")

        for mo in cls.pattern.finditer(template):
            if set(mo["tv"]) == set("_"):
                raise ValueError(f"Placeholder {mo['tv']} must include word characters.")
            elif mo["invalid"]:
                raise ValueError(f"Placeholder {mo['tv']} cannot start with a digit.")

    @classmethod
    def render_template(cls, params, template):
        """
        Renders a template by replacing placeholders with corresponding values.

        Args:
            params (dict): A dictionary containing placeholder-value pairs.
            template (str): The template string with placeholders.

        Returns:
            str: The interpolated template with placeholders replaced by values.
        """
        cls.validate_template(template)

        for mo in cls.pattern.finditer(template):
            template = cls.pattern.sub("%%(%s)s" % mo["tv"], template, 1)

        interpolated_string = (template % params).replace("'", '"')
        return interpolated_string
