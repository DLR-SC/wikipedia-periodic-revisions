#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
	Parses the edit histories of Wikipedia language versions.
"""
import nltk
import re
import string

from collections import Counter, defaultdict, OrderedDict
from wikipedia_w_time import wikipedia
from wikipedia_w_time import exceptions
from datetime import datetime

class ProcessRevisions:

    def __init__(self, language, event, rev_from: datetime=None, rev_to: datetime=None):

        self.language = language
        self.event = event
        self.revisions = {}
        self.content = ""
        self.links = []
        self.rev_from=rev_from
        self.rev_to=rev_to

    def wikipedia_page(self):
        # Get Wikipedia revision history
        wikipedia.set_lang(self.language)

        try:
            event_pagetitle = '_'.join(self.event.split())
            page = wikipedia.WikipediaPage(event_pagetitle, rev_from=self.rev_from, rev_to=self.rev_to)
            self.page = page
            self.revisions = page.revisions
            return page

        except exceptions.PageError:
            print("An exception was thrown in ProcessRevisions in wikirevparser")
            return None

    def replace_link(self, input_string, link, text):
        # Replace link with text
        if type(input_string) != str:
            return None

        output_string = input_string.replace("[[%s]]" % link, text)
        output_string = output_string.replace("[[%s|%s]]" % (link, text), text)

        return output_string

    def get_caption(self, line):
        # Get captions and links from captions, and replace both by string.
        # Todo: fix bug with "<ref" in caption
        if type(line) != str:
            return None

        if "|alt=" in line:

            elements = line.split("|alt=")[-1].split("|")[1:]
            caption = '|'.join(elements)[:-2]
            self.content = self.content.replace(line, caption)

        else:
            caption = re.search(r"thumb\|(.*)\]\]", line, re.IGNORECASE)
            if not caption: return None
            caption = caption.group(1)
            if "px" in caption or caption.startswith("{{legend"): return None

        # Links
        links, texts = self.get_links(caption)

        for link, text in zip(links, texts):
            caption = self.replace_link(caption, link, text)

            self.content = self.replace_link(self.content, link, text)
            self.links.append(link.lower())

        caption = caption.split("|")[-1].strip()
        caption = self.proper_formatting(caption, punct=True)

        return caption

    def get_category(self, link):
        # Get categories and remove label and language links.
        if type(link) != str:
            return None

        elements = link.split(":")

        if len(elements) == 2:
            label, category = elements

        elif len(elements) == 3:
            label, wiki, category = elements

        else:
            return None
        # Filter out language links
        if len(label) == 2 and label.islower(): return None

        return category

    def get_image_link(self, line):
        # Get image title and return correct link to commons.wikimedia.org
        if type(line) != str:
            return None

        occurrence = re.search(r"(:|=)([^(:|=)].*)(.jpg|.svg|.png)", line, re.IGNORECASE)
        if not occurrence:
            occurrence = re.search(r"(^)([^(:|=)].*)(.jpg|.svg|.png)", line, re.IGNORECASE)
        try:
            image_title, image_extension = occurrence.group(2, 3)
        except AttributeError:
            return None
        if ":" in image_title:
            image_title = image_title.split(":")[-1]

        image_title = '_'.join([x for x in image_title.split()])
        image_link = "https://commons.wikimedia.org/wiki/File:" + image_title + image_extension
        return image_link

    def get_links(self, input_string):
        # Get links from content.

        if type(input_string) != str:
            return None, None

        double_square_bracket, content = self.get_occurrences(r"\[\[(.*?)\]\]", input_string)
        links = []
        texts = []

        for element in double_square_bracket:
            elements = element.split("|")

            link = elements[0]
            if len(elements) == 2:
                text = elements[1]
            else:
                text = link

            links.append(link)
            texts.append(text)

        return links, texts

    def get_occurrences(self, regex, content):
        # Get references/citations.

        if type(content) != str:
            return None

        exp = re.compile(regex, re.IGNORECASE)
        occurrences = exp.findall(content)
        content = re.sub(exp, '', content)

        return occurrences, content

    def get_reference_types(self, input_list):
        # Get the reference type from a reference/citation block if annotated.
        if type(input_list) != list or len(input_list) < 1:
            return None

        elif type(input_list[0]) != str:
            return None

        types = Counter()

        for element in input_list:
            try:
                reference_type = re.search("{{[c|C]ite (.*?)( |\|)", element, re.IGNORECASE).group(1)
                if len(reference_type) <= 1: continue
                types[reference_type] += 1

            except AttributeError:
                types["_nill_"] += 1

        return types

    def get_urls(self, input_list):
        # Get URLs.
        urls = []
        http_regex = "http[s]*:\/\/([^ ]*)"

        for element in input_list:
            url = re.search(http_regex + r"( |}})", element, re.IGNORECASE)
            if url:
                url = url.group(1).split("|")[0]
            else:
                url = re.search(http_regex, element, re.IGNORECASE)
                if not url: continue
                url = url.group(1).split("|")[0]
            if "www" in url:
                url = url[4:]
            urls.append(url)
        return urls

    def parse_images(self):
        # Get and parse images.
        images = []
        captions = []
        extensions = [".jpg", ".svg", ".png", ".JPG", ".SVG", ".PNG"]

        for line in self.content.split("\n"):
            for extension in extensions:

                if not extension in line: continue

                image_link = self.get_image_link(line)
                images.append(image_link)

                self.content = self.content.replace(line, "")

                caption = self.get_caption(line)
                captions.append(caption)

        return images, captions

    def parse_categories(self):
        # Get and parse categories (and links).
        categories = []
        possible_links, texts = self.get_links(self.content)

        for link, text in zip(possible_links, texts):

            if ":" in link:
                category = self.get_category(link)
                if link.startswith("Category:"):
                    categories.append(link.split(":")[1])
                self.content = self.replace_link(self.content, link, "")

            else:
                self.links.append(link.lower())
                self.content = self.replace_link(self.content, link, text)

        return categories

    def parse_references(self):
        # Get and parse references and the top level domains.
        reference_template_types = Counter()  # some references have "type" markup, e.g. "book", "thesis", "news" etc.

        regex_letters = "\dA-Za-zğäåæáéëíıïóøöúü"
        regex_symbols = "\"'(){}[\]&=«»:.,?_~–\-/| "

        references, self.content = self.get_occurrences(r"<ref(.*?)<\/ref>", self.content)
        citations, self.content = self.get_occurrences(r"{{[c|C]ite [" + regex_letters + regex_symbols + ">]+}}",
                                                       self.content)

        urls = self.get_urls(references + citations + [x for x in self.content.split()])

        reference_types = self.get_reference_types(references + citations)
        if reference_types != None:
            reference_template_types += reference_types

        return urls, reference_template_types

    def proper_formatting(self, input_string, punct=True):
        # Add end punct, strip quotation marks, and tokenize.

        if type(input_string) != str:
            return None
        if len(input_string) < 1:
            return None
        if punct:
            if input_string[-1] not in string.punctuation:
                input_string += "."

        input_string = "".join([x for x in input_string if x != "'"])

        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        output_string = ' '.join(nltk.word_tokenize(input_string))

        return output_string

    def parse_sections(self):
        # Get and parse section titles.
        # Todo: improve section organization in output
        sections = []
        header1s, self.content = self.get_occurrences(r"[^=]={2}([^=].*?)={2}", self.content)
        header2s, self.content = self.get_occurrences(r"[^=]={3}([^=].*?)={3}", self.content)
        header3s, self.content = self.get_occurrences(r"[^=]={4}([^=].*?)={4}", self.content)
        sections.append([self.proper_formatting(x.strip(), punct=False) for x in header1s])
        sections.append([self.proper_formatting(x.strip("=").strip(), punct=False) for x in header2s])
        sections.append([self.proper_formatting(x.strip("==").strip(), punct=False) for x in header3s])

        return sections

    def parse_text(self):
        # Get and remove tables and markup from content.
        clean_content = []
        italics_markup, self.content = self.get_occurrences(r"\'{2,}", self.content)

        for line in self.content.split("\n"):

            line = line.strip()
            if len(line) == 0: continue
            if line[0] in string.punctuation or "px" in line: continue

            clean_content.append(self.proper_formatting(line))

        self.content = ' '.join([w for w in clean_content])

    def parse_revisions(self):
        # Input: revisions from Wikipedia page.
        # Output: dictionary with extracted page elements per revision.
        data = OrderedDict([])

        if self.revisions == None: return None

        for n, revision in enumerate(self.revisions):
            self.links = []
            self.content = ""
            parsed_data = defaultdict()
            timestamp = revision["timestamp"]

            if "user" not in revision.keys(): continue
            user = revision["user"]

            if "*" not in revision["slots"]["main"].keys(): continue
            self.content = revision["slots"]["main"]["*"]

            urls, reference_template_types = self.parse_references()
            images, captions = self.parse_images()
            categories = self.parse_categories()
            sections = self.parse_sections()
            self.parse_text()

            # parsed_data["captions"] = captions
            parsed_data["categories"] = categories
            parsed_data["content"] = self.content
            parsed_data["images"] = images
            parsed_data["links"] = self.links
            # parsed_data["reference_template_types"] = reference_template_types
            parsed_data["sections"] = sections
            parsed_data["urls"] = urls
            parsed_data["user"] = user

            data[timestamp] = parsed_data
        return data