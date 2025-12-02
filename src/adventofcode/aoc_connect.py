import os
import pathlib as pl
import datetime as dt
import requests as req


class InvalidDateError(Exception):
    """Error raised when an invalid challenge date is requested.

    Parameters
    ----------
    Exception : InvalidDateError
        An invalid date is requested.
    """
    pass


class InstructionParserError(Exception):
    """Error raised when the instruction parser failed.

    Parameters
    ----------
    Exception : InstructionParserError
        The instruction parser has failed.
    """
    pass


class UnexpectedResponseError(Exception):
    """Error raised when getting an unexpected HTML response.

    Parameters
    ----------
    Exception : UnexpectedResponseError
        Got an unexpected HTML response.
    """
    pass


class TokenError(Exception):
    """Error raised when the AOC session token is missing.

    Parameters
    ----------
    Exception : TokenError
        The AOC session token is missing.
    """
    pass


class WrongLevelError(Exception):
    """Error raised when an unexpected level is obtained.

    Parameters
    ----------
    Exception : WrongLevelError
        The level obtained is invalid.
    """
    pass


class AOCConnector:
    """Connector for the adventofcode challenge.

    This connector handles getting the challenge instructions,
    submitting the answers, and checking if the answer is correct.
    """

    cur_date = dt.date.today()
    min_year = 2015
    max_year = cur_date.year
    min_day = 1
    max_day = 25
    aoc_session_token = os.environ.get("AOC_SESSION_TOKEN", "N/A")
    instruction_parser = None
    root_url = "https://adventofcode.com"

    def __init__(self, year: int, day: int):
        """Initialize the adventofcode connector.

        Parameters
        ----------
        year : int
            Requested year of the challenge.
        day : int
            Requested day of the challenge.
        """

        if self.aoc_session_token == "N/A":
            raise TokenError("AOC session token not found! Please set the AOC_SESSION_TOKEN environment variable.")

        if year < self.min_year:
            raise InvalidDateError(f"There was no aoc challenge before {self.min_year}")

        if year > self.max_year:
            raise InvalidDateError(f"The requested year is in the future! We are still in {self.max_year}")

        if day < self.min_day or day > self.max_day:
            raise InvalidDateError(f"Invalid day: {day}")

        if year == self.max_year and (self.cur_date.month < 12 or day > self.cur_date.day):
            raise InvalidDateError(f"Day {day} has not come yet")

        self._year = year
        self._day = day

    def _get_instruction_page(self):
        """Get the instruction page.
        """

        url = f"{self.root_url}/{self._year}/day/{self._day}"
        response = req.get(url, cookies={"session": self.aoc_session_token})
        self.instruction_parser = HTMLParser(response)

    def _make_instructions(self, root_dir):
        """Retrieve and store the instructions from the instruction page.

        Parameters
        ----------
        root_dir : str | pl.Path
            Directory to store the instructions in.
        """

        if self.instruction_parser is None:
            raise InstructionParserError()
        instructions = self.instruction_parser.parse_instructions()
        with open(pl.Path(root_dir, "instructions.md"), "w") as file:
            file.write(instructions)

    def _make_input(self, root_dir):
        """Retrieve and store the input from the AOC website.

        Parameters
        ----------
        root_dir : str | pl.Path
            Directory to store the input in.
        """

        url = f"{self.root_url}/{self._year}/day/{self._day}/input"
        input_response = req.get(url, cookies={"session": self.aoc_session_token})
        self.input_parser = HTMLParser(input_response)
        input_content = self.input_parser.get_content()

        with open(pl.Path(root_dir, "input.txt"), "w") as file:
            file.write(input_content)

    def _make_python_canevas(self, canevas, root_dir):
        """Create a Python canevas

        Parameters
        ----------
        canevas : str
            Python canevas to use.
        root_dir : str | pl.Path
            Directory to store the Python canevas in.
        """

        with open(pl.Path(root_dir, "solution.py"), "w") as file:
            file.write(canevas)

    def initialize(self, canevas, root=pl.Path(".").resolve(), dir_name="challenges", force=False):
        """Initialize the challenge.

        This creates the challenge directories,retrieves the instructions and input,
        and constructs a Python script canevas to solve the challenge.

        Parameters
        ----------
        canevas : str
            Canevas Python script
        root : str | pl.Path, default=`pl.Path(".").resolve()`
            Root directory, by default pl.Path(".").resolve()
        dir_name : str, default="challenges"
            Directory name to store challenges in, by default "challenges"
        force : bool, default=False
            Force the initialization if a challenge already exists
        """

        root_path = pl.Path(root, dir_name)
        year_path = pl.Path(root_path, str(self._year))
        day_path = pl.Path(root_path, str(self._year), f"day_{self._day}")

        if os.path.exists(day_path) and not force:
            print(f"Directory {day_path.resolve()} already exists! Use the -f flag to overwrite it.")
            return

        if not os.path.exists(root_path):
            os.mkdir(root_path)

        if not os.path.exists(year_path):
            os.mkdir(year_path)

        if not os.path.exists(day_path):
            os.mkdir(day_path)

        self._get_instruction_page()
        self._make_input(day_path)
        self._make_instructions(day_path)
        self._make_python_canevas(canevas, day_path)

    def get_level(self):
        self._get_instruction_page()

        level = 1

        if "--- Part Two ---" in self.instruction_parser.get_content():
            level = 2

        if "Both parts of this puzzle are complete!" in self.instruction_parser.get_content():
            level = 3

        if level < 1:
            raise WrongLevelError()
        if level > 2:
            print("This challenge was already solved!")

        return level

    def submit_answer(self, level, answer):

        if str(level) not in ["1", "2"]:
            raise WrongLevelError()

        url = f"{self.root_url}/{self._year}/day/{self._day}/answer"
        answer_response = req.post(url, data={"level": str(level), "answer": str(answer)},
                                   cookies={"session": self.aoc_session_token})

        answer_content = answer_response.content.decode()

        verdict = "Invalid server response..."
        success = False

        if "That's not the right answer" in answer_content:
            verdict = "That's not the right answer, try again!"

        elif "That's the right answer" in answer_content:
            success = True
            verdict = "That's the right answer!"
            if str(level) == "1":
                verdict += " On to level 2!"

        return verdict, success

    def reload_instructions(self, root_dir):
        """Retrieve and store the instructions from the instruction page.

        Parameters
        ----------
        root_dir : str | pl.Path
            Directory to store the instructions in.
        """

        self._get_instruction_page()

        if self.instruction_parser is None:
            raise InstructionParserError()
        instructions = self.instruction_parser.parse_instructions()
        with open(pl.Path(root_dir, "instructions.md"), "w") as file:
            file.write(instructions)


class HTMLParser:
    """Parser for HTML content of AOC pages.
    """

    def __init__(self, response):
        """Initialize the HTML parser.

        Parameters
        ----------
        response : req.Response
            Response object.
        """

        if response.status_code != 200:
            raise UnexpectedResponseError()

        self._response = response
        self._content = response.content.decode()

    def parse_instructions(self):
        """Parse the instructions from the HTML content."""

        html_main, _ = self._get_inner_tag(self._content, "main")
        all_instructions = ""
        while self._has_tag(html_main, "article"):
            instructions, html_main = self._get_inner_tag(html_main, "article")
            all_instructions += instructions

        return all_instructions

    def get_content(self):
        """Get the raw HTML content."""
        return self._content

    def _has_tag(self, content, tag):
        """Check if the content has a given tag.

        Parameters
        ----------
        content : str
            Content to check.
        tag : str
            Tag to check for.

        Returns
        -------
        bool
            Whether the tag is present in the content.
        """
        return f"<{tag}" in content and f"</{tag}>" in content

    def _get_inner_tag(self, content, tag):
        """Get the inner content of a given tag.
        Parameters
        ----------
        content : str
            Content to parse.
        tag : str
            Tag to get the inner content of.
        Returns
        -------
        str
            Inner content of the tag.
        str
            Remaining content after extracting the tag.
        """

        if f"<{tag}>" in content and f"</{tag}>" in content:
            return content.split(f"<{tag}>")[1].split(f"</{tag}>")[0], f"</{tag}>".join(content.split(f"</{tag}>")[1:])

        elif f"<{tag}" in content and f"</{tag}>" in content:

            inner_content = ">".join(content.split(f"<{tag}")[1].split(">")[1:])
            return inner_content.split(f"</{tag}>")[0], f"</{tag}>".join(content.split(f"</{tag}>")[1:])

        raise ValueError(f"No <{tag}> tag in the content!")
