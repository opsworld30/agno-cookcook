from agents.factory import AgentFactory
from agents.config import AgentConfig


def test_reasoning_agent():
    config = AgentConfig()
    factory = AgentFactory(config)
    
    reasoning_agent = factory.create_agent("reasoning")
    
    print("\n=== 测试1: 逻辑推理问题 ===\n")
    reasoning_agent.print_response(
        "一个人需要带一只狐狸、一只鸡和一袋谷物过河。船只能容纳他和一样东西。"
        "如果无人看管，狐狸会吃鸡，鸡会吃谷物。他如何安全地把所有东西都带过河？",
        stream=True
    )
    
    print("\n\n=== 测试2: 数学推理 ===\n")
    reasoning_agent.print_response(
        "9.11 和 9.9 哪个更大？请详细解释你的推理过程。",
        stream=True
    )
    
    print("\n\n=== 测试3: 伦理推理 ===\n")
    reasoning_agent.print_response(
        "分析电车难题：一辆失控的电车即将撞向5个人，你可以拉动拉杆让电车转向另一条轨道，"
        "但那条轨道上有1个人。你会怎么做？请从多个伦理框架分析这个问题。",
        stream=True
    )


def test_general_agent_with_reasoning():
    config = AgentConfig()
    config.enable_reasoning = True
    config.reasoning_min_steps = 2
    config.reasoning_max_steps = 8
    
    factory = AgentFactory(config)
    general_agent = factory.create_agent("general")
    
    print("\n=== 测试通用助手的推理增强模式 ===\n")
    general_agent.print_response(
        "如果一个房间里有3只猫，每只猫能抓3只老鼠，需要3分钟。"
        "那么100只猫抓100只老鼠需要多少时间？",
        stream=True
    )


if __name__ == "__main__":
    print("=" * 60)
    print("推理增强功能测试")
    print("=" * 60)
    
    test_reasoning_agent()
    
    print("\n" + "=" * 60)
    print("通用助手推理增强测试")
    print("=" * 60)
    
    test_general_agent_with_reasoning()
