from agno.team import Team
from agno.models.openai import OpenAILike
from agents.factory import AgentFactory
from agents.config import AgentConfig


def create_research_team(config: AgentConfig = None) -> Team:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    search_agent = factory.create_agent("search")
    baidu_agent = factory.create_agent("baidu")
    analyst_agent = factory.create_agent("analyst")
    general_agent = factory.create_agent("general")

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Team(
        id="research-team",
        name="研究团队",
        members=[search_agent, baidu_agent, analyst_agent, general_agent],
        model=model,
        instructions=[
            "你是研究团队的协调者",
            "DuckDuckGo搜索专家负责国际信息收集",
            "百度搜索专家负责中文信息收集",
            "数据分析师负责分析数据",
            "通用助手负责整理和总结",
            "根据任务语言和类型选择合适的搜索专家"
        ],
        description="专业研究团队，提供多语言信息搜索、数据分析和报告生成服务"
    )


def create_dev_team(config: AgentConfig = None) -> Team:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    coder_agent = factory.create_agent("coder")
    analyst_agent = factory.create_agent("analyst")
    general_agent = factory.create_agent("general")

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Team(
        id="dev-team",
        name="开发团队",
        members=[coder_agent, analyst_agent, general_agent],
        model=model,
        instructions=[
            "你是开发团队的协调者",
            "代码助手负责编写和调试代码",
            "数据分析师负责性能分析和测试",
            "通用助手负责文档和总结",
            "确保代码质量和项目进度"
        ],
        description="专业开发团队，提供代码开发、性能优化和技术文档服务"
    )


def create_content_team(config: AgentConfig = None) -> Team:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    search_agent = factory.create_agent("search")
    baidu_agent = factory.create_agent("baidu")
    searxng_agent = factory.create_agent("searxng")
    general_agent = factory.create_agent("general")

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Team(
        id="content-team",
        name="内容创作团队",
        members=[search_agent, baidu_agent, searxng_agent, general_agent],
        model=model,
        instructions=[
            "你是内容创作团队的协调者",
            "DuckDuckGo搜索专家负责国际素材收集",
            "百度搜索专家负责中文素材收集",
            "Searxng搜索专家提供多源信息聚合",
            "通用助手负责内容创作和编辑",
            "创作高质量、多语言、有价值的内容"
        ],
        description="专业内容团队，提供多语言内容策划、创作和编辑服务"
    )


def create_full_service_team(config: AgentConfig = None) -> Team:
    if config is None:
        config = AgentConfig()
    config.validate()

    factory = AgentFactory(config)
    all_agents = factory.create_all_agents()

    model = OpenAILike(
        id=config.model,
        api_key=config.get_api_key(),
        base_url=config.base_url,
        default_headers=config.get_headers()
    )

    return Team(
        id="full-service-team",
        name="全功能服务团队",
        members=all_agents,
        model=model,
        instructions=[
            "你是全功能服务团队的协调者",
            "团队包含通用助手、搜索专家、数据分析师和代码助手",
            "根据任务复杂度和类型，灵活调度团队成员",
            "确保高效协作，提供最优质的服务"
        ],
        description="全功能服务团队，提供全方位的AI助手服务"
    )
