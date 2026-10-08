
import os

from openai import OpenAI


class LLMProvider:

    """
    DevMind-X real LLM provider.

    Current provider:
        Groq

    Groq is accessed through its official
    OpenAI-compatible API.

    API key is loaded from:
        GROQ_API_KEY

    No secret is stored in source code.
    """

    def __init__(self):

        self.provider = None
        self.api_key = None
        self.model = None
        self.client = None

        self.initialize()

    # ==============================================================
    # INITIALIZE
    # ==============================================================

    def initialize(self):

        self.api_key = os.environ.get(
            "GROQ_API_KEY"
        )

        if not self.api_key:

            return

        self.provider = "groq"

        self.model = os.environ.get(
            "DEVMIND_LLM_MODEL",
            "openai/gpt-oss-120b"
        )

        self.client = OpenAI(

            api_key=self.api_key,

            base_url=(
                "https://api.groq.com/openai/v1"
            )
        )

    # ==============================================================
    # STATUS
    # ==============================================================

    def is_available(self):

        return (
            self.client is not None
            and self.api_key is not None
        )

    # ==============================================================
    # PROVIDER STATUS
    # ==============================================================

    def status(self):

        return {

            "available":
                self.is_available(),

            "provider":
                self.provider,

            "model":
                self.model
        }

    # ==============================================================
    # CHAT
    # ==============================================================

    def chat(
        self,
        system_prompt,
        user_prompt
    ):

        if not self.is_available():

            return {

                "success": False,

                "error":
                    "GROQ_API_KEY is not configured."
            }

        try:

            response = (
                self.client
                .chat
                .completions
                .create(

                    model=self.model,

                    messages=[

                        {
                            "role": "system",
                            "content": system_prompt
                        },

                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],

                    temperature=0.2,

                    max_tokens=1200
                )
            )

            answer = (
                response
                .choices[0]
                .message
                .content
            )

            if not answer:

                return {

                    "success": False,

                    "error":
                        "Groq returned an empty response."
                }

            return {

                "success": True,

                "provider":
                    self.provider,

                "model":
                    self.model,

                "answer":
                    answer
            }

        except Exception as error:

            return {

                "success": False,

                "error":
                    f"{type(error).__name__}: {error}"
            }
