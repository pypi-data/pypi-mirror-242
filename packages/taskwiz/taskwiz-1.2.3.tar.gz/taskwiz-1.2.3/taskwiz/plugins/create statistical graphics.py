"""
TaskWiz Bot Plugin - dates and times

Retrieve information about dates and times

[FUNCTION_CALL]
"""

from taskwiz import config
from taskwiz.utils.shared_utils import SharedUtil

def create_statistical_graphics(function_args):
    code = function_args.get("code") # required
    SharedUtil.showAndExecutePythonCode(code)
    return "Done!"

functionSignature = {
    "name": "create_statistical_graphics",
    "description": f'''Create statistical graphics''',
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python code that integrates package seaborn to resolve my request",
            },
        },
        "required": ["code"],
    },
}

config.pluginsWithFunctionCall.append("create_statistical_graphics")
config.chatGPTApiFunctionSignatures.append(functionSignature)
config.chatGPTApiAvailableFunctions["create_statistical_graphics"] = create_statistical_graphics