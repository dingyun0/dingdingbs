from autogen import ConversableAgent
from autogen.agentchat import ChatResult

from backend.app.common.index import LLm_Config_List


class AutoGen_service:
    llm_config: dict = {}

    def __init__(self):
        self.llm_config = LLm_Config_List[0]
        pass

    #  获取智能体
    @classmethod
    def get_agent(self, name: str, prompt: str, agent_llm_config: dict = llm_config, human_input_mode: str = "NEVER") -> ConversableAgent:
        return ConversableAgent(
            name,
            system_message=prompt,
            llm_config=agent_llm_config,
            human_input_mode=human_input_mode
        )

    @classmethod
    def angent_chat(agent: ConversableAgent,) -> ChatResult:
        return agent.initiate_chat()
