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
            return result.stdout
        except Exception as e:
            return f"Error executing skill {self.name}: {e}"
