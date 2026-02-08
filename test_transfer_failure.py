"""
后端测试：验证转账失败和 error-analysis skill 调用

测试转账失败场景（余额不足），验证：
1. transfer_tokens 返回错误
2. 前端接收到错误后调用 error-analysis API
3. error-analysis 返回分析结果
"""

import asyncio
import sys
from pathlib import Path
import httpx

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "transfer-tokens" / "scripts"))

from build_transfer import build_transfer_transaction


async def test_transfer_failure():
    """测试转账失败场景"""
    
    print("=" * 60)
    print("🧪 测试：转账失败 + error-analysis")
    print("=" * 60)
    
    # 测试参数 - 使用一个余额不足的地址
    from_address = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
    to_address = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"
    token = "TRX"
    amount = 1000000.0  # 极大金额，必然失败
    network = "nile"
    
    print(f"\n📋 测试参数（预期失败）：")
    print(f"   From: {from_address}")
    print(f"   To: {to_address}")
    print(f"   Token: {token}")
    print(f"   Amount: {amount} (故意设置超大金额)")
    print(f"   Network: {network}")
    print("\n" + "=" * 60)
    
    # === 第 1 步：调用 transfer ===
    print("\n🚀 步骤 1/2: 调用 build_transfer_transaction...\n")
    
    result = await build_transfer_transaction(
        from_address=from_address,
        to_address=to_address,
        token=token,
        amount=amount,
        memo="",
        network=network
    )
    
    print("\n" + "=" * 60)
    print("📊 Transfer 结果")
    print("=" * 60)
    
    # 检查是否包含交易
    has_transaction = 'transaction' in result
    
    if has_transaction:
        print(f"\n✅ Transaction 生成成功")
        print(f"   txID: {result['transaction'].get('txID', 'N/A')}")
        print("\n⚠️ 注意：交易已生成，但广播到链上时可能会失败（余额不足）")
        print("前端会在广播失败后调用 error-analysis")
    else:
        print(f"\n⚠️ 没有生成transaction（可能在构建阶段就检测到问题）")
    
    # === 第 2 步：模拟前端调用 error-analysis API ===
    print("\n\n" + "=" * 60)
    print("🚀 步骤 2/2: 模拟前端调用 error-analysis API")
    print("=" * 60)
    
    # 模拟一个典型的 TRON 错误消息（余额不足）
    error_hex = "436f6e74726163742076616c6964617465206572726f72203a2056616c6964617465205472616e73666572436f6e7472616374206572726f722c2062616c616e6365206973206e6f742073756666696369656e742e"
    
    print(f"\n📤 调用 POST /api/analyze-error")
    print(f"   Error: {error_hex[:60]}...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/api/analyze-error",
                json={"error_message": error_hex}  # 正确的参数名
            )
            
            if response.status_code == 200:
                analysis = response.json()
                print(f"\n✅ error-analysis API 响应成功")
                print(f"\n📋 分析结果：")
                print(f"{analysis.get('analysis', 'No analysis')}")
            else:
                print(f"\n❌ API 调用失败: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                
    except httpx.ConnectError:
        print(f"\n❌ 无法连接到 API (http://localhost:8000)")
        print(f"   请确保后端正在运行：uv run python src/server.py")
    except Exception as e:
        print(f"\n❌ API 调用异常: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 完整的转账失败流程")
    print("=" * 60)
    print("""
转账失败的完整 6-skill 调用链：

1. ✅ address-book - 记录转账尝试
2. ✅ malicious-address-detector - 检测黑名单
3. ✅ address-risk-checker - 风险评估
4. ⚠️ energy-rental - （TRX转账跳过）
5. ✅ transfer-build - 生成交易
   
   👉 用户尝试广播交易到链上
   👉 链上验证失败（余额不足）
   👉 返回错误消息
   
6. ✅ error-analysis - 前端自动调用，分析错误原因

前端流程：
- TransactionCard 组件
- 捕获 broadcast 错误
- 调用 /api/analyze-error
- 显示 LLM 分析结果
    """)


if __name__ == '__main__':
    asyncio.run(test_transfer_failure())
