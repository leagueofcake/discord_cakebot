import re


class HelpEntry:
    def __init__(self, command, description, usage, category, example=None):
        self.command = command
        self.description = description
        self.usage = usage
        self.example = example
        self.category = category
        self.short_description = description.split('\n')[0]

    def get_markdown(self):
        attr = [self.description, self.usage]
        for i in range(len(attr)):
            attr[i] = re.sub(r'(!.+)(\s-\s)', r'`\1`\2', attr[i])  # Make usage command lines as code blocks
            attr[i] = re.sub(r'^(!.+)(\s-\s)?', r'`\1`\2', attr[i])  # Make usage command lines as code blocks

        marked_down = '## {}\n{}  \n\n### Usage\n{}'.format(self.command, *attr)
        if self.example:
            example = re.sub(r'(.*): (!.*)', r'\1: `\2`', self.example)  # Make example command lines as code blocks
            marked_down += '\n\n### Examples\n{}'.format(example)

        marked_down = marked_down.replace('_', '\_')  # Escape underscores
        marked_down = marked_down.replace('\n', '  \n')  # Add two spaces to end of line for Markdown line breaks
        marked_down += '  \n  \n'  # Ending newline
        return marked_down

    def get_entry(self):
        formatted = '\n' \
                    '**Command:** ``' + self.command + '``\n\n' \
                    '**Category:** ' + self.category + '\n' \
                    '**Description:** ' + self.description + '\n\n' \
                    '**Usage**\n```' + self.usage + '```\n'
        if self.example:
            formatted += '\n**Examples**\n```' + self.example + '```'

        docs_link = 'https://discord-cakebot.readthedocs.io/en/latest/command_list.html'
        formatted += '\nDetailed command information can be found at ' + docs_link
        if self.category in ['general', 'music', 'modtools', 'permissions', 'miscellaneous']:
            formatted += '#{}'.format(self.category)
        return formatted
