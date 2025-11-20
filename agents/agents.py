from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.searxng import SearxngTools
from agno.tools.baidusearch import BaiduSearchTools
from agno.tools.exa import ExaTools
from agno.tools.file import FileTools
from agno.tools.shell import ShellTools
from agents.config import AgentConfig
from utils.datetime_helper import get_datetime_context


def create_general_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="general-assistant",
        name="通用助手",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        add_history_to_context=True,
        add_datetime_to_context=True,
        enable_user_memories=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个友好的通用AI助手",
            "你可以帮助用户处理各种日常任务和问题",
            "回答时要清晰、准确且有帮助",
            "如果不确定答案，请诚实告知",
            "注意当前的日期时间信息，在需要时间相关的回答时使用",
            "记住用户的偏好和重要信息，提供个性化服务"
        ]
    )


def create_search_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="web-search-expert",
        name="搜索专家",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[DuckDuckGoTools()],
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的信息搜索和研究助手",
            "你可以使用DuckDuckGo搜索实时信息",
            "在回答问题时，优先使用搜索工具获取最新、最准确的信息",
            "对搜索结果进行整理和总结，提供清晰的答案",
            "如果需要多个来源验证，请进行多次搜索",
            "引用信息来源，保持客观和准确",
            "注意当前的日期时间，搜索时可以加上时间相关的关键词(如'最新'、'2024'等)",
            "",
            "工具使用规范：",
            "- duckduckgo_search的query参数必须是字符串类型",
            "- 不要传递列表或数组给query参数",
            "- 正确示例: duckduckgo_search(query='小红书热点话题 2024最新')",
            "- 错误示例: duckduckgo_search(query=['小红书', '热点'])"
        ]
    )


def create_analyst_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="data-analyst",
        name="数据分析师",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[FileTools()],
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的数据分析师",
            "你擅长处理和分析各种数据文件",
            "你可以读取CSV、JSON、Excel等格式的数据",
            "对数据进行统计分析，找出关键洞察",
            "用清晰的语言解释数据趋势和模式",
            "在适当的时候建议数据可视化方案",
            "生成结构化的分析报告",
            "注意当前的日期时间，在分析时间序列数据时使用"
        ]
    )


def create_coder_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="code-assistant",
        name="代码助手",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[FileTools(), ShellTools()],
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的软件开发助手",
            "你精通多种编程语言，包括Python、JavaScript、Java、Go等",
            "你可以帮助编写、审查和优化代码",
            "在编写代码时，要注重代码质量、可读性和最佳实践",
            "提供清晰的代码注释和文档",
            "帮助调试和修复代码问题",
            "可以执行shell命令来运行和测试代码",
            "解释复杂的技术概念时要清晰易懂",
            "注意当前的日期时间，在生成日志、注释等时使用"
        ]
    )


def create_searxng_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="searxng-expert",
        name="Searxng搜索专家",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[SearxngTools(
            host=config.searxng_host,
            fixed_max_results=5
        )],
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的Searxng搜索助手",
            "Searxng是一个隐私友好的元搜索引擎",
            "你可以搜索网页、新闻、科学文献、图片、视频等",
            "对搜索结果进行整理和总结，提供清晰的答案",
            "引用信息来源，保持客观和准确",
            "注意当前的日期时间，搜索时可以加上时间相关的关键词获取最新信息"
        ]
    )


def create_baidu_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Agent(
        id="baidu-search-expert",
        name="百度搜索专家",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[BaiduSearchTools(fixed_max_results=5)],
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的百度搜索助手",
            "你可以使用百度搜索中文和英文信息",
            "特别擅长搜索中文内容和中国本地信息",
            "对搜索结果进行整理和总结，提供清晰的答案",
            "引用信息来源，保持客观和准确",
            "注意当前的日期时间，搜索时加上年份和'最新'等关键词获取最新信息",
            "",
            "工具使用规范：",
            "- baidu_search的query参数必须是字符串类型",
            "- 不要传递列表或数组给query参数",
            "- 正确示例: baidu_search(query='小红书最新热点 2024')",
            "- 错误示例: baidu_search(query=['小红书', '热点'])"
        ]
    )


def create_exa_agent(config: AgentConfig = None) -> Agent:
    if config is None:
        config = AgentConfig()
    config.validate()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )
    
    tools = []
    if config.exa_api_key and config.exa_api_key != "your_exa_api_key_here":
        tools = [ExaTools(api_key=config.exa_api_key)]

    return Agent(
        id="exa-search-expert",
        name="Exa搜索专家",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=tools,
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是一个专业的Exa语义搜索助手",
            "Exa是一个AI驱动的语义搜索引擎",
            "你可以进行深度的语义搜索，理解查询意图",
            "特别擅长搜索新闻、学术内容和专业信息",
            "对搜索结果进行整理和总结，提供清晰的答案",
            "引用信息来源，保持客观和准确",
            "注意当前的日期时间，搜索时可以指定时间范围获取最新信息"
        ] if tools else [
            "Exa搜索需要API Key",
            "请在.env文件中设置EXA_API_KEY",
            "获取API Key: https://exa.ai"
        ]
    )
