"""
Agno CookCook - 多功能AI Agent系统
支持多种专业Agent协同工作，以及Team和Workflow模式
"""
from agno.os import AgentOS
from agents.factory import AgentFactory
from agents.config import AgentConfig
from teams import (
    create_research_team,
    create_dev_team,
    create_content_team,
    create_full_service_team
)
from workflows import (
    create_research_workflow,
    create_dev_workflow,
    create_content_workflow,
    create_data_pipeline_workflow
)
from utils.logger import setup_logger, get_logger


def create_agent_os():
    """
    创建AgentOS应用，同时支持Agents、Teams和Workflows

    包含的功能：
    - 独立Agents：8个专业Agent可独立使用
    - Teams：4个专业团队提供协同服务
    - Workflows：4个工作流提供流程化服务

    Agents:
    - 通用助手、搜索专家、数据分析师、代码助手、推理专家、Searxng搜索、百度搜索、Exa搜索

    Teams:
    - 研究团队、开发团队、内容团队、全功能团队

    Workflows:
    - 研究工作流、开发工作流、内容工作流、数据流水线
    """
    logger = get_logger()
    
    try:
        logger.info("开始初始化AgentOS...")
        
        config = AgentConfig()
        config.validate()
        logger.info("配置验证成功")

        factory = AgentFactory(config)
        all_agents = factory.create_all_agents()
        logger.info(f"创建了 {len(all_agents)} 个Agents (包含推理增强)")
        
        teams = [
            create_research_team(config),
            create_dev_team(config),
            create_content_team(config),
            create_full_service_team(config)
        ]
        logger.info(f"创建了 {len(teams)} 个Teams")
        
        workflows = [
            create_research_workflow(config),
            create_dev_workflow(config),
            create_content_workflow(config),
            create_data_pipeline_workflow(config)
        ]
        logger.info(f"创建了 {len(workflows)} 个Workflows")
        
        agent_os = AgentOS(
            agents=all_agents,
            teams=teams,
            workflows=workflows
        )
        logger.info("AgentOS初始化成功")
        
        return agent_os
        
    except Exception as e:
        logger.error(f"初始化AgentOS失败: {str(e)}", exc_info=True)
        raise


agent_os = create_agent_os()
app = agent_os.get_app()

from fastapi.middleware.cors import CORSMiddleware
from api.knowledge import router as knowledge_router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6660", "http://127.0.0.1:6660","https://os.agno.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge_router)


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("=" * 50)
    logger.info("Agno CookCook Agent系统启动")
    logger.info("=" * 50)
    
    config = AgentConfig()
    
    print("\n=== Agno CookCook Agent系统 ===")
    
    print(f"\n⚙️  配置信息:")
    print(f"  - API Keys: {len(config.api_keys)} 个 (轮询模式)")
    print(f"  - 模型: {config.model}")
    print(f"  - 服务地址: {config.server_host}:{config.server_port}")
    
    print("\n📦 Agents (8个):")
    for agent_type, description in AgentFactory.list_available_agents().items():
        print(f"  - {agent_type}: {description}")

    print("\n👥 Teams (4个):")
    print("  - research-team: 研究团队")
    print("  - dev-team: 开发团队")
    print("  - content-team: 内容团队")
    print("  - full-service-team: 全功能团队")

    print("\n🔄 Workflows (4个):")
    print("  - research-workflow: 研究工作流")
    print("  - dev-workflow: 开发工作流")
    print("  - content-workflow: 内容工作流")
    print("  - data-pipeline-workflow: 数据流水线")

    print("\n🌐 访问方式:")
    print("  - Agents: POST /agents/{agent_id}/runs")
    print("  - Teams: POST /teams/{team_id}/runs")
    print("  - Workflows: POST /workflows/{workflow_id}/runs")

    print("\n� 日志目录: logs/")
    print("  - 所有日志: logs/YYYY-MM-DD.log")
    print("  - 错误日志: logs/YYYY-MM-DD_error.log")

    print("\n🚀 启动AgentOS服务...")
    print(f"访问 http://{config.server_host}:{config.server_port} 使用Agent系统\n")
    
    logger.info(f"启动AgentOS服务: http://{config.server_host}:{config.server_port}")
    logger.info(f"API Key轮询: {len(config.api_keys)} 个Key")

    try:
        agent_os.serve(
            app="main:app", 
            host=config.server_host, 
            port=config.server_port, 
            reload=True
        )
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}", exc_info=True)
        raise