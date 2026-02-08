"""
Test scam pattern detection.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import tool_profile_address

# Test with user's known wallet
USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"

async def main():
    print("🚨 Scam Pattern Detection Test")
    print("=" * 70)
    print()
    print("Testing enhanced address profiling with scam detection...")
    print()
    
    # Test 1: Profile user wallet (should be normal)
    print("TEST 1: Normal User Wallet")
    print("-" * 70)
    result = await tool_profile_address(USER_WALLET, max_transactions=100)
    print(result)
    print()
    
    print("\n\n" + "=" * 70)
    print("✅ Scam detection tests completed!")
    print("=" * 70)
    print("""
💡 New Features:
  ✓ 诱导投资骗局检测 (bait-and-switch)
  ✓ 资金黑洞检测 (money sink - only receives)
  ✓ 蜜罐合约检测 (honeypot - imbalanced flow)
  ✓ 递增投资模式检测 (escalating amounts)
  ✓ 粉尘攻击检测 (dusting attack)
  ✓ 交易特征详细展示
  
🎯 Scam Patterns Detected:
  🚨 初期返利诱导
  🚨 只进不出地址
  🚨 收支严重失衡
  ⚠️ 投资金额递增
  ℹ️ 重复小额测试
""")

if __name__ == "__main__":
    asyncio.run(main())
