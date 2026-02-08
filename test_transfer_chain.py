"""
后端测试：验证转账 Skill 链式调用

测试 transfer_tokens 是否正确调用所有 6 个 sub-skills：
1. address-book
2. malicious-address-detector
3. address-risk-checker
4. energy-rental (for TRC20)
5. build transaction
6. error-analysis (on failure)
"""

import asyncio
import sys
from pathlib import Path

# Add project root and skills to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "transfer-tokens" / "scripts"))

# Now import build_transfer
from build_transfer import build_transfer_transaction


async def test_transfer_skill_chain():
    """测试转账 skill 链式调用"""
    
    print("=" * 60)
    print("🧪 测试：转账 Skill 链式调用")
    print("=" * 60)
    
    # 测试参数
    from_address = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
    to_address = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"
    token = "USDT"
    amount = 10.0
    network = "nile"
    
    print(f"\n📋 测试参数：")
    print(f"   From: {from_address}")
    print(f"   To: {to_address}")
    print(f"   Token: {token}")
    print(f"   Amount: {amount}")
    print(f"   Network: {network}")
    print("\n" + "=" * 60)
    
    # 调用 transfer
    print("\n🚀 开始调用 build_transfer_transaction...\n")
    
    result = await build_transfer_transaction(
        from_address=from_address,
        to_address=to_address,
        token=token,
        amount=amount,
        memo="",
        network=network
    )
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    
    if 'error' in result:
        print(f"\n❌ 失败：{result['error']}")
    elif 'transaction' in result:
        print("\n✅ 成功：生成了交易")
        print(f"   Transaction ID: {result['transaction'].get('txID', 'N/A')}")
        print(f"   Metadata: {result.get('metadata', {}).get('type', 'N/A')}")
    else:
        print(f"\n⚠️ 未知结果：{result}")
    
    print("\n" + "=" * 60)
    print("🔍 预期看到的 Skill 调用日志：")
    print("=" * 60)
    print("""
应该包含以下 skills 的执行日志：

1. ✅ [SKILL ORCHESTRATION] transfer-tokens
   - 显示参数

2. ✅ [SKILL] address-book: Recording transfer...
   - 查询别名
   - 记录转账，次数+1
   - 显示 "Transfer #X"

3. ✅ [SKILL] malicious-address-detector: Checking TronScan blacklist...
   - 调用 TronScan API
   - 检测黑名单标签
   - 显示结果（SAFE/WARNING/DANGER）

4. ✅ [SKILL] address-risk-checker: Running security assessment...
   - 检查链上风险
   - 显示风险等级

5. ✅ [SKILL] energy-rental: Calculating energy requirements...
   - 计算能量需求（仅TRC20）
   - 显示租赁建议

6. ✅ [SKILL] Building transaction...
   - 构建交易JSON
    """)
    
    print("\n如果交易失败，前端会自动调用 error-analysis skill\n")
    

if __name__ == '__main__':
    asyncio.run(test_transfer_skill_chain())
