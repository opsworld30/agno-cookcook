from agno.workflow import Workflow
from agents.factory import AgentFactory
from agents.config import AgentConfig


def create_research_workflow(config: AgentConfig = None) -> Workflow:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    
    from agno.agent import Agent
    from agno.db.sqlite import SqliteDb
    from agno.models.openai import OpenAILike
    from agno.tools.baidusearch import BaiduSearchTools
    from utils.datetime_helper import get_datetime_context
    
    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )
    
    search_step = Agent(
        name="搜索步骤",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        tools=[BaiduSearchTools(fixed_max_results=5)],
        add_datetime_to_context=True,
        enable_user_memories=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是工作流的第一步：信息搜索",
            "使用百度搜索收集用户查询的相关信息",
            "注意当前日期时间，搜索时加上年份和'最新'等关键词",
            "搜索结果要全面、准确",
            "将搜索到的信息整理后传递给下一步",
            "重要：baidu_search的query参数必须是字符串，不能是列表",
            "正确示例: baidu_search(query='小红书最新热点 2024')"
        ]
    )
    
    analyst_step = Agent(
        name="分析步骤", 
        model=model,
        db=SqliteDb(db_file=config.db_file),
        add_datetime_to_context=True,
        enable_user_memories=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是工作流的第二步：数据分析",
            "分析上一步搜索到的信息",
            "提取关键要点和趋势",
            "注意时效性，关注最新的数据和趋势",
            "将分析结果传递给下一步"
        ]
    )
    
    summary_step = Agent(
        name="总结步骤",
        model=model,
        db=SqliteDb(db_file=config.db_file),
        add_datetime_to_context=True,
        enable_user_memories=True,
        additional_context=get_datetime_context(),
        instructions=[
            "你是工作流的最后一步：生成报告",
            "基于前面步骤的搜索和分析结果",
            "生成一份完整、清晰的研究报告",
            "报告要包含：主要发现、数据分析、结论建议",
            "在报告中注明当前日期，说明这是基于最新信息的分析"
        ]
    )

    return Workflow(
        id="research-workflow",
        name="研究工作流",
        description="中文信息搜索 -> 数据分析 -> 报告生成",
        steps=[search_step, analyst_step, summary_step]
    )


def create_dev_workflow(config: AgentConfig = None) -> Workflow:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    general_agent = factory.create_agent("general")
    coder_agent = factory.create_agent("coder")
    analyst_agent = factory.create_agent("analyst")

    return Workflow(
        id="dev-workflow",
        name="开发工作流",
        description="需求分析 -> 代码实现 -> 性能测试",
        steps=[
            general_agent,
            coder_agent,
            analyst_agent
        ]
    )


def create_content_workflow(config: AgentConfig = None) -> Workflow:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    searxng_agent = factory.create_agent("searxng")
    baidu_agent = factory.create_agent("baidu")
    general_agent = factory.create_agent("general")

    return Workflow(
        id="content-workflow",
        name="内容创作工作流",
        description="多源素材收集 -> 中文素材补充 -> 内容创作",
        steps=[
            searxng_agent,
            baidu_agent,
            general_agent
        ]
    )


def create_data_pipeline_workflow(config: AgentConfig = None) -> Workflow:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    baidu_agent = factory.create_agent("baidu")
    searxng_agent = factory.create_agent("searxng")
    analyst_agent = factory.create_agent("analyst")
    coder_agent = factory.create_agent("coder")
    general_agent = factory.create_agent("general")

    return Workflow(
        id="data-pipeline-workflow",
        name="数据处理流水线",
        description="中文数据收集 -> 多源数据聚合 -> 数据分析 -> 代码生成 -> 报告输出",
        steps=[
            baidu_agent,
            searxng_agent,
            analyst_agent,
            coder_agent,
            general_agent
        ]
    )
