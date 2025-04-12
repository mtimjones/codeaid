# codeaid
Command-line coding assistant using LLMs.

This wrapper utility bundles useful prompts and allows them to be applied
to a source file for operations such as summarize, refactor, etc.

## Usage

$ py codeaid.py
Usage is:

        asst.py --goal <goal> --filename <filename> --target <language>
                Where goal is: [summarize, defects, security, optimize, 
                    refactor, document, complexity, naming, translate, 
                    cleanup, todo, ut ]
                and <filename> is the source file to analyze, 
                <language> is the target language for translate.

## Setup

Add your openai key to the env OPENAI_KEY.


