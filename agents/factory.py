"""Agent工厂 - 统一创建和管理所有Agent"""
from typing import List, Optional
from agno.agent import Agent
from agents.config import AgentConfig
from agents.agents import (
    create_general_agent,
    create_search_agent,
    create_analyst_agent,
    create_coder_agent,
    create_searxng_agent,
    create_baidu_agent,
    create_exa_agent
)


class AgentFactory:
    """Agent工厂类，用于创建和管理不同类型的Agent"""

    AGENT_TYPES = {
        "general": "通用助手",
        "search": "搜索专家(DuckDuckGo)",
        "analyst": "数据分析师",
        "coder": "代码助手",
        "searxng": "Searxng搜索专家",
        "baidu": "百度搜索专家",
        "exa": "Exa搜索专家",
    }

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        初始化Agent工厂

        Args:
            config: 共享的配置对象，如果为None则使用默认配置
        """
        self.config = config or AgentConfig()
        self.config.validate()

    def create_agent(self, agent_type: str) -> Agent:
        """
        根据类型创建单个Agent

        Args:
            agent_type: Agent类型，可选值：general, search, analyst, coder

        Returns:
            创建的Agent实例

        Raises:
            ValueError: 当agent_type不在支持的类型中时
        """
        agent_creators = {
            "general": create_general_agent,
            "search": create_search_agent,
            "analyst": create_analyst_agent,
            "coder": create_coder_agent,
            "searxng": create_searxng_agent,
            "baidu": create_baidu_agent,
            "exa": create_exa_agent,
        }

        if agent_type not in agent_creators:
            raise ValueError(
                f"不支持的Agent类型: {agent_type}. "
                f"支持的类型: {', '.join(self.AGENT_TYPES.keys())}"
            )

        return agent_creators[agent_type](self.config)

    def create_all_agents(self) -> List[Agent]:
        """
        创建所有类型的Agent

        Returns:
            包含所有Agent的列表
        """
        return [
            self.create_agent(agent_type)
            for agent_type in self.AGENT_TYPES.keys()
        ]

    def create_agents(self, agent_types: List[str]) -> List[Agent]:
        """
        根据指定的类型列表创建多个Agent

        Args:
            agent_types: Agent类型列表

        Returns:
            创建的Agent列表
        """
        return [self.create_agent(agent_type) for agent_type in agent_types]

    @classmethod
    def list_available_agents(cls) -> dict:
        """
        列出所有可用的Agent类型

        Returns:
            Agent类型及其描述的字典
        """
        return cls.AGENT_TYPES.copy()
