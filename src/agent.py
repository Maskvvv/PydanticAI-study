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


@dataclass
class UserInfo:
    name: str
    role: str


dependency_agent = Agent(
    model,
    deps_type=UserInfo,
    system_prompt=lambda ctx: f"你是{ctx.deps.role}的AI助手。用户名是{ctx.deps.name}。请用专业但友好的方式回答问题。",
)


@dataclass
class CodeAnalysis:
    language: str
    purpose: str
    complexity: str
    suggestions: list[str]


structured_agent = Agent(
    model,
    result_type=CodeAnalysis,
    system_prompt='你是一个代码分析专家。分析用户提供的代码，返回结构化的分析结果。'
)


async def demo_basic_chat():
    print("=" * 50)
    print("📝 演示1: 基础对话能力")
    print("=" * 50)
    
    result = await agent.run("你好！请介绍一下你自己有什么能力？")
    print(f"AI回复: {result.output}")
    print()


async def demo_tool_usage():
    print("=" * 50)
    print("🔧 演示2: 工具调用能力")
    print("=" * 50)
    
    result = await agent.run("请帮我查看当前目录的结构")
    print(f"AI回复: {result.output}")
    print()


async def demo_file_operations():
    print("=" * 50)
    print("📁 演示3: 文件操作能力")
    print("=" * 50)
    
    result = await agent.run(
        "请创建一个名为demo.txt的文件，内容是'Hello from PydanticAI!'，然后读取它的内容给我看"
    )
    print(f"AI回复: {result.output}")
    print()


async def demo_dependency_injection():
    print("=" * 50)
    print("💉 演示4: 依赖注入能力")
    print("=" * 50)
    
    user = UserInfo(name="张三", role="Python开发者")
    result = await dependency_agent.run("请给我推荐一些学习资源", deps=user)
    print(f"AI回复: {result.output}")
    print()


async def demo_structured_output():
    print("=" * 50)
    print("📊 演示5: 结构化输出能力")
    print("=" * 50)
    
    code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    result = await structured_agent.run(f"请分析这段代码:\n{code}")
    analysis: CodeAnalysis = result.output
    print(f"语言: {analysis.language}")
    print(f"目的: {analysis.purpose}")
    print(f"复杂度: {analysis.complexity}")
    print(f"建议: {', '.join(analysis.suggestions)}")
    print()


async def demo_streaming():
    print("=" * 50)
    print("🌊 演示6: 流式输出能力")
    print("=" * 50)
    
    print("AI回复: ", end="", flush=True)
    async with agent.run_stream("请用一段话介绍什么是Agent？") as response:
        async for text in response.stream_text():
            print(text, end="", flush=True)
    print("\n")


async def demo_conversation_history():
    print("=" * 50)
    print("💬 演示7: 对话历史能力")
    print("=" * 50)
    
    message_history = []
    
    result1 = await agent.run("我叫李四", message_history=message_history)
    message_history = result1.all_messages()
    print(f"第一轮: {result1.data}")
    
    result2 = await agent.run("你还记得我叫什么名字吗？", message_history=message_history)
    print(f"第二轮: {result2.data}")
    print()


async def main():
    print("\n" + "🚀" * 25)
    print("   PydanticAI Agent 能力演示")
    print("🚀" * 25 + "\n")
    
    demos = [
        ("基础对话", demo_basic_chat),
        ("工具调用", demo_tool_usage),
        ("文件操作", demo_file_operations),
        ("依赖注入", demo_dependency_injection),
        ("结构化输出", demo_structured_output),
        ("流式输出", demo_streaming),
        ("对话历史", demo_conversation_history),
    ]
    
    print("可用的演示项目:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  0. 运行所有演示")
    print(f"  q. 退出")
    print()
    
    while True:
        choice = input("请选择要运行的演示 (0-7/q): ").strip().lower()
        
        if choice == 'q':
            print("\n感谢使用，再见！👋")
            break
        elif choice == '0':
            for name, demo in demos:
                try:
                    await demo()
                except Exception as e:
                    print(f"❌ {name}演示出错: {e}\n")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            name, demo = demos[int(choice) - 1]
            try:
                await demo()
            except Exception as e:
                print(f"❌ {name}演示出错: {e}\n")
        else:
            print("无效选择，请重新输入\n")


if __name__ == "__main__":
    asyncio.run(main())
