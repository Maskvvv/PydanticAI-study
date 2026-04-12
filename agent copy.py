from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.mcp import MCPServerStdio
from dataclasses import dataclass
from typing import Optional
import tools
from dotenv import load_dotenv
import os
import asyncio
import sys

load_dotenv()

model = OpenAIChatModel(
    "deepseek-chat",
    provider=OpenAIProvider(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url="https://api.deepseek.com"
    )
)

mcp_server = MCPServerStdio(
    sys.executable,
    args=['mcp_server.py'],
    cwd=r'd:\code\ai\PydanticAI-study',
    env=os.environ,
)

agent = Agent(
    model,
    system_prompt='你是Windows平台脚本大师，可以灵活搭配cmd和python脚本指令去实现用户需求。'
                  '你拥有文件操作、目录管理、命令执行能力，以及获取主机信息的能力。请用中文回复用户。',
    tools=[
        tools.create_text_file,
        tools.create_python_file,
        tools.get_directory_structure,
        tools.rename_file,
        tools.execute_windows_command,
        tools.read_file,
        tools.delete_file
    ],
    mcp_servers=[mcp_server]
)

async def main():
    async with agent.run_mcp_servers():
        print("=" * 50)
        print("MCP 服务已启动，可以调用主机信息工具")
        print("=" * 50)
        print()
        
        result = await agent.run("请获取当前主机的系统信息和网络信息")
        print(f"AI回复: {result.output}")
        print()
        
        result2 = await agent.run("请获取当前主机的磁盘使用情况")
        print(f"AI回复: {result2.output}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
