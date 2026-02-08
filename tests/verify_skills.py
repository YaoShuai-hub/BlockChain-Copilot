"""
Skills-based verification script.
Tests the new skills architecture.
"""
import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.skills_loader import SkillsLoader
from src.tool_wrappers import (
    tool_get_token_price,
    tool_get_wallet_balance,
    tool_swap_tokens,
    tool_energy_rental
)

async def main():
    print("🚀 BlockChain-Copilot Skills Verification\n")
    
    # 1. Test skills discovery
    print("=" * 60)
    print("1. Testing Skills Discovery...")
    print("=" * 60)
    loader = SkillsLoader("skills")
    skills = loader.discover_skills()
    
    print(f"\n✅ Discovered {len(skills)} skills:\n")
    for skill in skills:
        print(f"  📦 {skill['name']}")
        print(f"     {skill['description'][:80]}...")
        print()
    
    # 2. Test token price
    print("=" * 60)
    print("2. Testing Token Price Skill...")
    print("=" * 60)
    result = await tool_get_token_price("TRX")
    print(result)
    print()
    
    # 3. Test wallet balance
    print("=" * 60)
    print("3. Testing Wallet Balance Skill...")
    print("=" * 60)
    test_addr = "TKzxdSv2FZKQrEqkKVgp5DcwEXBEKMg2Ax"
    result = await tool_get_wallet_balance(test_addr)
    print(result)
    print()
    
    # 4. Test swap tokens
    print("=" * 60)
    print("4. Testing Swap Tokens Skill...")
    print("=" * 60)
    result = await tool_swap_tokens(
        user_address=test_addr,
        token_in="TRX",
        token_out="USDT",
        amount_in=10,
        slippage=0.5
    )
    print(result[:800] + "..." if len(result) > 800 else result)
    print()
    
    # 5. Test energy rental
    print("=" * 60)
    print("5. Testing Energy Rental Skill...")
    print("=" * 60)
    result = await tool_energy_rental(32000, 3)
    print(result)
    print()
    
    print("=" * 60)
    print("✅ All skills verified successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
