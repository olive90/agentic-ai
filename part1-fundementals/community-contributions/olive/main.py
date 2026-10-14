import os
from dotenv import load_dotenv

import utils

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# check if API keys are set
if not GEMINI_API_KEY:
    raise ValueError("Missing Gemini API key")
if not GROQ_API_KEY:
    raise ValueError("Missing Groq API Key")


opt_message = "I want you to generate a customer support ticket for a 3rd party re-seller. "
opt_message += "The ticket should be a single sentence describing a common issue a customer might face with their product or service. "
opt_message += "Please ensure the ticket is varied and covers different types of problems. "
opt_message += "Do not give any subjects, only the body of the ticket."

opt_res = utils.optimizer(GEMINI_API_KEY, opt_message)
print(f"### Generated Ticket:\n{opt_res}")

# messages list
evaluator_message = "I want you to assess the quality and completeness of the following customer support ticket and suggest improvements."
evaluator_message += "The ticket is as follows: " + opt_res + " "
evaluator_message += "Please assess the quality and completeness as either 'Low', 'Medium', or 'High'. "
evaluator_message += "Respond with only the quality and completeness level."
evaluator_message += "Please also suggest necessary improvements."

evaluator_res = utils.evaluator(GROQ_API_KEY, evaluator_message)
print(f"### Evaluation result for Quality and Completeness:\n{evaluator_res}")

quality = evaluator_res.strip().splitlines()[0].strip().lower()

if evaluator_res != "high":
    message = "Revise the ticket as follows: " + opt_res + " "
    message += "based on the feedback as follows: " + evaluator_res + " "
    message += "Respond with clarity and actionable details."

    final_opt_res = utils.optimizer(GEMINI_API_KEY, message)
    print(f"### Final Ticket:\n{final_opt_res}")

else:
    print(evaluator_res)






