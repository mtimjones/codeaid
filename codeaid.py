#!/usr/bin/env python3

# Command-line coding assistant using OpenAI
# mtj@mtjones.com
# April 12th, 2025

from openai import OpenAI
import os
import sys
import logging
import argparse
from typing import Optional

class PromptManager:
    """Manages different prompt templates for various code analysis goals."""

    def __init__(self):
        """Initializes the PromptManager with predefined prompts."""
        self.prompts = self._initialize_prompts( )
        self._goals_list = ', '.join( self.prompts.keys( ) )

    def _initialize_prompts( self ) -> dict[str, str]:
        """Sets up predefined prompts for various goals."""
        return {
            "summarize": (
               """Act as a programming assistant. After examining the provided 
               source code, identify the language in which it is written, then 
               give a concise, one-paragraph summary of its functionality. 
               Include any notable or interesting elements a programmer would 
               find useful or appreciate, but keep your explanation streamlined 
               and to the point.
               """
            ),

            "defects": (
                """Act as an expert software debugger. After examining the 
                provided source code, briefly summarize any possible defects 
                you find, focusing strictly on potential errors without including 
                unrelated discussion.
                """
            ),

            "security": (
                """Act as a software security expert. Examine the provided source 
                code, identify any potential vulnerabilities, and offer concise 
                recommendations to improve its security.
                """
            ),

            "optimize": (
                """Act as a software optimization expert. Evaluate the provided 
                source code and recommend performance improvements. Include any 
                best practices, plus language-specific techniques that can 
                significantly enhance efficiency.
                """
            ),

            "refactor": (
                """Act as a software refactoring expert. Analyze the provided 
                source code and propose improvements to maintainability, 
                readability, modularization, naming, and decomposition. Offer 
                reorganizations, style enhancements, and language-specific 
                techniques (e.g., creating classes) that clarify and structure 
                the code more effectively.
                """
            ),

            "document": (
                """Act as a software documentation expert. After examining the 
                provided source code, generate comprehensive documentation, 
                inline comments, or markdown—summarizing the entire file and 
                each module in a clear, concise manner.
                """
            ),

            "complexity": (
                """Act as an expert software engineer dedicated to reducing 
                complexity.  Review the provided source code, evaluate the 
                complexity of its functions and modules, and highlight any 
                excessively tangled or overly complex areas that warrant 
                refactoring. Focus on modularization, maintainability, and 
                readability enhancements.
                """
            ),

            "naming": (
                """Act as an expert software engineer prioritizing readability. 
                Examine the source code’s variable and function naming, 
                highlighting any non-descriptive names and recommending more 
                descriptive alternatives. List only necessary changes, keeping 
                the response concise.
                """
            ),

            "translate": (
                """Act as a software translation expert. Review the provided 
                source code and rewrite it in XXX language, preserving the 
                original functionality and logic.
                """
            ),

            "cleanup": (
                """Your role is a software cleanup specialist.  Your goal is 
                to take the software provided in the context below and convert 
                it into PEP-8 style.  Maintain all functionality, just refine 
                into PEP-8.
                """
            ),

            "todo": (
                """You are an agile story writing expert.  Your goal is to 
                find each TODO in the source code and write an agile story for 
                it.  Please keep the stories focused on the task at hand 
                (using the TODO text and surrounding code as a guide).
                """
            ),

            "ut": (
                """You are a test development expert.  Your goal is to analyze 
                the source code and develop unit-tests using the unittest module 
                to validate the code for quality improvement for future changes.
                """
            )
        }

    def get_prompt_by_goal( self, goal: str ) -> Optional[str]:
        """Retrieves the prompt for the specific goal."""
        return self.prompts.get( goal )

    def goals(self) -> str:
        """Returns a list of available goals as a comma-separated string."""
        return self._goals_list


class OpenAIClient():
    """Client for interaction with OpenAI API."""

    def __init__(self):
        """Initializes the LLMClient with the OpenAI API key."""
        self.openai_key = self._get_openai_key( )

    @staticmethod
    def _get_openai_key( ) -> str:
        """Get the OPENAI Key from the environment variables."""
        openai_key = os.environ.get( 'OPENAI_KEY', None )
        if openai_key is None:
            logging.error( "OPENAI_KEY is not set\n" )
            sys.exit(1)
        return openai_key

    def compose_prompt_message( self, goal:str, context:str, prompt_manager: PromptManager, target:str ) -> Optional[str]:
        """Creates the complete prompt message based on the goal and context."""
        prompt = prompt_manager.get_prompt_by_goal(goal)
        if prompt is None:
            logging.error(f"Goal {goal} is not recognized.\n\n")
            return None

        if target is not None and goal == 'translate':
            prompt = prompt.replace("XXX", target)

        return prompt + context


    def execute_prompt( self, message: str ) -> str:
        """Executes the prompt against the OpenAI API and returns the response."""
        client = OpenAI( api_key = self.openai_key )

        chat_completion = client.chat.completions.create(
            messages = [ { "role": "user", "content": message, } ],
            model="gpt-4o",
        )

        return chat_completion.choices[0].message.content.strip()


def read_source_file( filename: str) -> Optional[str]:
    """Reads the content of the source file and returns to the caller."""
    try:
        with open(filename, "r") as file:
            return file.read( )
    except FileNotFoundError:
        logging.error(f'Source filename ({filename}) not found.')
        return None


def print_usage_instructions( prompt_manager: PromptManager ) -> None:
    """Displays usage instructions for the script."""
    print( "Usage is:\n\n\tasst.py --goal <goal> --filename <filename> --target <language>" )
    print( f"\t\tWhere goal is: [{ prompt_manager.goals( ) } ]" )
    print( "\t\tand <filename> is the source file to analyze, <language> is the target language for translate.\n" )


def parse_arguments() -> argparse.Namespace:
    """Parses the command-line arguments."""
    parser = argparse.ArgumentParser( description='Analyze source files using a given goal.' )
    parser.add_argument( '--goal', default=None,
                         help='Analysis goal (--show-goals to review)' )
    parser.add_argument( '--file', default=None,
                         dest='filename', help='The source filename for analysis' )
    parser.add_argument( '--target', default=None,
                         dest='target', help='The target language for translate.')
    return parser.parse_args( )


def create_prompt_manager( goal, filename, target ) -> PromptManager:
    prompt_manager = PromptManager( )
    if goal is None or filename is None:
        print_usage_instructions( prompt_manager )
        sys.exit( 1 )
    if goal == 'translate' and target is None:
        print_usage_instructions( prompt_manager )
        sys.exit( 1 )

    return prompt_manager


def main( ) -> None:
    """Main function for script execution."""
    args = parse_arguments( )

    prompt_manager = create_prompt_manager( args.goal, args.filename, args.target )

    source = read_source_file( args.filename )

    if source:
        llm_client = OpenAIClient( )
        prompt = llm_client.compose_prompt_message( args.goal, source, prompt_manager, args.target )
        if prompt:
            response = llm_client.execute_prompt( prompt )
            if response:
                print( response  )


if __name__ == "__main__":
    main( )
    sys.exit(0)
