"""RewriteInline implementation."""

import re
from typing import Optional

import ruamel.yaml as yaml

from spotter.library.rewriting.models import Replacement, RewriteBase, RewriteSuggestion


class RewriteInline(RewriteBase):
    """RewriteInline implementation."""

    def get_regex(self, text_before: str) -> str:  # noqa: D102
        return rf"^(\s*{text_before}\s*:(.*))"

    def get_indent_block(self, content: str, indent_index: int, split_by: str) -> str:
        """
        Get content block with each line indented.

        :param content: content block (usually a whole task)
        :param indent_index: number of empty spaces before first letter
        :param split_by: character to split by
        """
        indent = "\n" + " " * indent_index
        content_split = list(filter(None, content.split(split_by)))
        i_content = [indent + content for content in content_split]
        return "".join(i_content)

    def get_replacement(self, content: str, suggestion: RewriteSuggestion) -> Optional[Replacement]:  # noqa: D102
        suggestion_dict = suggestion.suggestion_spec
        part = self.get_context(content, suggestion)
        indent = self.get_indent_index(content, suggestion.start_mark)
        before = suggestion_dict["data"]["module_name"]
        offset = 2

        args = ""
        variables = ""
        if "args" in suggestion_dict["data"] and suggestion_dict["data"]["args"]:
            args = self.get_indent_block(yaml.round_trip_dump(suggestion_dict["data"]["args"]), offset, "\n")
        if "vars" in suggestion_dict["data"] and suggestion_dict["data"]["vars"]:
            variables = "\n" + yaml.round_trip_dump({"vars": suggestion_dict["data"]["vars"]})
        after = self.get_indent_block("".join([args, variables]), indent, "\n").rstrip("\n")

        regex = self.get_regex(before)
        match = re.search(regex, part, re.MULTILINE)
        if match is None:
            print(
                f"Applying suggestion {suggestion.suggestion_spec} failed at "
                f"{suggestion.file}:{suggestion.line}:{suggestion.column}: could not find string to replace."
            )
            return None
        replacement = Replacement(content, suggestion, match, after)
        return replacement
