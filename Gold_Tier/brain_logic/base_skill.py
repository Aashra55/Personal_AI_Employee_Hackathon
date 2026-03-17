import subprocess
import os

# Base Skill class for Gold Tier AI Employee

class BaseSkill:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, prompt: str) -> str:
        print(f"[*] Activating Skill: {self.name}")
        try:
            result = subprocess.run(
                ["ccr.cmd", "code"],
                input=prompt,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            output = result.stdout
            if "429" in output or "Quota exceeded" in output or "RESOURCE_EXHAUSTED" in output:
                print("\n" + "!"*50)
                print("!!! ALERT: GEMINI API QUOTA EXCEEDED (429) !!!")
                print("The system cannot reason right now. Please wait a few minutes.")
                print("!"*50 + "\n")
                return "API Error: Quota Exceeded"

            return output
        except Exception as e:
            return f"Error executing skill {self.name}: {e}"
