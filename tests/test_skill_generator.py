"""
Test Skill Generator - Create a batch transfer skill
Simulates user request: "向10个地址批量转账"
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.skill_generator.scripts.generator import (
    analyze_requirement,
    generate_skill_plan,
    generate_skill_code,
    save_generated_skill,
    format_plan_for_review
)

async def test_skill_generator():
    """Test the skill generator workflow."""
    
    print("=" * 80)
    print("🧪 TESTING SKILL GENERATOR")
    print("=" * 80)
    print()
    
    # Simulate user request
    user_request = "向10个地址批量转账TRX或TRC20代币"
    
    print(f"📝 User Request: \"{user_request}\"")
    print()
    
    # List of existing skills
    existing_skills = [
        'token-price', 'wallet-balance', 'swap-tokens',
        'energy-rental', 'transfer-tokens', 'address-risk-checker',
        'address-book', 'address-profiling'
    ]
    
    # Step 1: Analyze requirement
    print("Step 1: Analyzing requirement...")
    print("-" * 80)
    analysis = await analyze_requirement(user_request, existing_skills)
    
    print(f"✓ Needs new skill: {analysis['needs_new_skill']}")
    print(f"✓ Reason: {analysis['reason']}")
    print(f"✓ Suggested name: {analysis['suggested_name']}")
    print(f"✓ Complexity: {analysis['complexity']}")
    print()
    
    # Step 2: Generate planning
    print("Step 2: Generating skill planning...")
    print("-" * 80)
    
    skill_name = "batch-transfer"  # Override with better name
    plan = await generate_skill_plan(user_request, skill_name, existing_skills)
    
    # Customize the plan for batch transfer
    plan['purpose'] = "Batch transfer TRX or TRC20 tokens to multiple addresses"
    plan['key_features'] = [
        "Support transferring to up to 100 addresses",
        "Validate all addresses before execution",
        "Calculate total amount and fees",
        "Return detailed results for each transfer",
        "Support both TRX and TRC20 tokens"
    ]
    plan['data_sources'] = [
        "TronGrid API (transaction building)",
        "Address validation utilities"
    ]
    
    # Show plan to user
    plan_text = format_plan_for_review(plan)
    print(plan_text)
    
    # Simulate user approval
    approval = input("\n👉 Approve this plan? (yes/no): ").strip().lower()
    
    if approval != 'yes':
        print("❌ Skill generation cancelled by user")
        return
    
    print()
    print("✅ Plan approved! Proceeding with code generation...")
    print()
    
    # Step 3: Generate code
    print("Step 3: Generating skill code...")
    print("-" * 80)
    
    generated = await generate_skill_code(plan, user_request)
    
    print("✅ Code generation complete!")
    print()
    
    # Show preview
    print("📄 SKILL.md Preview (first 500 chars):")
    print("-" * 80)
    print(generated['skill_md'][:500] + "...")
    print()
    
    print("🐍 Implementation Preview (first 500 chars):")
    print("-" * 80)
    print(generated['skill_py'][:500] + "...")
    print()
    
    # Ask to save
    save_approval = input("💾 Save this skill to personal-skills/? (yes/no): ").strip().lower()
    
    if save_approval != 'yes':
        print("❌ Skill not saved")
        return
    
    print()
    
    # Step 4: Save skill
    print("Step 4: Saving skill...")
    print("-" * 80)
    
    result = save_generated_skill(generated)
    
    if result['success']:
        print(f"✅ Skill '{result['skill_name']}' saved successfully!")
        print()
        print("Created files:")
        for file in result['created_files']:
            print(f"  ✓ {file}")
        print()
        print("🎉 Skill is ready to use!")
        print()
        print("Next steps:")
        print("  1. Add to src/tool_wrappers.py")
        print("  2. Register in src/main.py")
        print("  3. Test the skill")
    else:
        print("❌ Failed to save skill")
    
    print()
    print("=" * 80)
    print("Test Complete")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_skill_generator())
