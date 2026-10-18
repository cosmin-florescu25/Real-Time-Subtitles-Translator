import language_tool_python
import re

tool = language_tool_python.LanguageTool('en-US')

# to resolve misspellings
def post_process_with_tool(text):
    if not text:
        return text

    matches = tool.check(text)

    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text