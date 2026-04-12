from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import RunContext
from dataclasses import dataclass
from typing import Optional
import tools
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

model = OpenAIChatModel(
    "deepseek-chat",
    provider=OpenAIProvider(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url="https://api.deepseek.com"
    )
)

agent = Agent(
    model,
    system_prompt='你是Windows平台脚本大师，可以灵活搭配cmd和python脚本指令去实现用户需求。'
                  '你拥有文件操作、目录管理和命令执行能力。请用中文回复用户。',
    tools=[
        tools.create_text_file,
        tools.create_python_file,
        tools.get_directory_structure,
        tools.rename_file,
        tools.execute_windows_command,
        tools.read_file,
        tools.delete_file
    ]
)

async def main():
    result = await agent.run('''请帮我创建一个名为test.txt的文件，内容是'Hello from PydanticAI!'，
    然后读取它的内容给我看''')
    print(f"AI回复: {result.output}")
    print()

if __name__ == "__main__":
    asyncio.run(main())
