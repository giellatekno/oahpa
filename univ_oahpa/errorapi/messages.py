class FeedbackMessageStore(object):
    """ Reads and stores messages in memory.
    """

    # Example of format. This will be rewritten on file load.
    # TODO: parse XML errors
    messages = {
        'sme': {
            'CGErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "CGErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "CGErr",
                },
            ],
            'DiphErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "DiphErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "DiphErr",
                },
            ],
        },
        'nob': {
            'CGErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "CGErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "CGErr",
                },
            ],
            'DiphErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "DiphErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "DiphErr",
                },
            ],
        },
    }

    @property
    def error_tags(self):
        if not hasattr(self, '_error_tags'):
            # Extract tags we care about from XML
            e_tags = []
            for l, msgs in self.messages.iteritems():
                _ks = sum( [list(k) for k in msgs.keys()], [])
                e_tags.extend(_ks)
            self._error_tags = set(e_tags)
        return self._error_tags

    def get_message(self, iso, error_tag, task=False):
        """
            >>> messagestore.get_message("sme", "CGErr")
            "You forgot consonant gradation!"
            >>> messagestore.get_message("sme", "CGErr", task="Sg+Gen")
            "You forgot consonant gradation (genitive sg.)!"
        """
        from sets import ImmutableSet

        def copy_item(m):
            return m.copy()

        error_tag = ImmutableSet(error_tag)

        messages = self.messages.get(iso, {}).get(error_tag, False)

        if messages:
            if task:
                task_messages = [a for a in map(copy_item, messages) if a.get('task', '') == task]
                return task_messages
            else:
                return map(copy_item, messages)

        return False

    def parse(self, file_path):
        """ Reads the XML file and stores all messages """

        # TODO @tag2 attribute on message, how should this work?
        from sets import ImmutableSet

        from xml.dom import minidom as _dom
        from collections import defaultdict

        tree = _dom.parse(file_path)

        root = tree.getElementsByTagName("messages")[0]
        lang = root.getAttribute("xml:lang")
        messages = root.getElementsByTagName("message")

        parsed_messages = defaultdict(list)

        for m in messages:
            tag = [m.getAttribute('tag')]
            tag2 = m.getAttribute('tag2')
            if tag2 is not None:
                if tag2.strip():
                    tag.append(tag2)
            tags = ImmutableSet(tag)
            task = m.getAttribute('task')
            string = m.firstChild.wholeText
            parsed_messages[tags].append({
                "string": string,
                "task": task,
                "tags": tags,
            })

        self.messages[lang] = parsed_messages

    def __init__(self, *xml_paths):

        self.messages = {}
        for x in xml_paths:
            self.parse(x)

if __name__ == "__main__":
    m = FeedbackMessageStore('../sme/meta/morfaerrorfstmessages.xml')
