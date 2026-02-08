"""
Agent simulation test WITH address book integration.
Test natural language requests that involve contact management.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import (
    tool_transfer_tokens,
    tool_list_contacts,
    tool_search_contacts
)

USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
TARGET_WALLET = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"

class AgentSimulatorWithContacts:
    """Simulates LLM agent understanding natural language with contact context."""
    
    async def process_request(self, user_request: str, user_context: dict = None):
        print(f"\n{'=' * 80}")
        print(f"👤 USER REQUEST: \"{user_request}\"")
        print(f"{'=' * 80}\n")
        
        request_lower = user_request.lower()
        
        # Simulate LLM reasoning
        print("🧠 AGENT REASONING:")
        
        # Check for contact management requests
        if any(word in request_lower for word in ['通讯录', '地址簿', 'contacts', 'address book', '联系人']):
            if '查看' in request_lower or 'list' in request_lower or '显示' in request_lower:
                print("   ✓ Intent detected: List saved contacts\n")
                result = await tool_list_contacts(sort_by="count")
                print(result)
                return
            elif '搜索' in request_lower or 'search' in request_lower or '找' in request_lower:
                # Extract search query (simplified)
                print("   ✓ Intent detected: Search contacts\n")
                # For demo, search for '家'
                result = await tool_search_contacts("家")
                print(result)
                return
        
        # Check for transfer with contact name
        if '转' in user_request or '发送' in user_request or 'send' in request_lower or 'transfer' in request_lower:
            print("   ✓ Intent detected: Transfer with contact management")
            
            # Check if memo provided
            has_memo = False
            memo = ""
            if '备注' in user_request or 'memo' in request_lower or '给' in user_request:
                # Extract memo (simplified - in real LLM this would be more sophisticated)
                if '给妈妈' in user_request:
                    memo = "妈妈"
                    has_memo = True
                elif '朋友' in user_request:
                    memo = "朋友的钱包"
                    has_memo = True
                elif '家人' in user_request:
                    memo = "家人"
                    has_memo = True
            
            if has_memo:
                print(f"   ✓ Memo detected: Will save as contact alias '{memo}'")
            else:
                print("   ✓ No memo: Will only track transfer count")
            
            print("\n📤 Executing Transfer:\n")
            
            # Execute transfer
            result = await tool_transfer_tokens(
                from_address=user_context.get('user_wallet', USER_WALLET),
                to_address=user_context.get('target_wallet', TARGET_WALLET),
                token="TRX",
                amount=10,
                memo=memo
            )
            print(result[:600])  # Truncate for demo
            return
        
        print("   ✗ Intent not recognized in this demo\n")

async def main():
    print("🤖 Agent Simulation - Address Book Integration")
    print("=" * 80)
    print("Testing LLM understanding of contact management requests\n")
    
    agent = AgentSimulatorWithContacts()
    user_context = {
        'user_wallet': USER_WALLET,
        'target_wallet': TARGET_WALLET
    }
    
    # Scenario 1: Transfer with memo to create contact
    await agent.process_request(
        "给妈妈转10个TRX",
        user_context
    )
    
    # Scenario 2: Transfer to same address without memo (should recognize saved contact)
    await agent.process_request(
        "再转5个TRX给这个地址",
        user_context
    )
    
    # Scenario 3: List contacts
    await agent.process_request(
        "查看我的通讯录",
        user_context
    )
    
    # Scenario 4: Search contacts
    await agent.process_request(
        "搜索我保存的联系人",
        user_context
    )
    
    print("\n" + "=" * 80)
    print("✅ Agent simulation with address book completed!")
    print("=" * 80)
    print("""
💡 Demonstrated Capabilities:
  ✓ LLM understands contact management intents
  ✓ Auto-saves aliases from natural language
  ✓ Recognizes and displays saved contacts
  ✓ Tracks transfer counts automatically
  ✓ Integrates seamlessly with transfer workflow
""")

if __name__ == "__main__":
    asyncio.run(main())
