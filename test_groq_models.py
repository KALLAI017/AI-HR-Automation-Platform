"""
Test script to verify Groq LLaMA models are working
Tests both llama-3.1-8b-instant and llama-3.3-70b-versatile
"""
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def test_groq_models():
    """Test both Groq models with sample prompts"""
    
    print("=" * 80)
    print("🧪 TESTING GROQ LLAMA MODELS")
    print("=" * 80)
    
    # Initialize Groq client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file!")
        return
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    client = Groq(api_key=api_key)
    
    # Test 1: LLaMA 3.1 8B Instant (Fast Chat Model)
    print("\n" + "=" * 80)
    print("📨 TEST 1: LLaMA 3.1 8B Instant (Fast Chat)")
    print("=" * 80)
    
    test_prompt_1 = """You are a friendly technical interviewer. 
A candidate asks: "Can I use a hash map for the Two Sum problem?"

Give a brief, encouraging response (2-3 sentences)."""
    
    print("\n📝 Prompt:")
    print(test_prompt_1)
    print("\n⏱️ Calling model: llama-3.1-8b-instant...")
    
    start_time = time.time()
    try:
        response_1 = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful technical interviewer."},
                {"role": "user", "content": test_prompt_1}
            ],
            temperature=0.7,
            max_tokens=200
        )
        elapsed_1 = time.time() - start_time
        
        print(f"\n✅ SUCCESS! Response time: {elapsed_1:.3f}s ({elapsed_1*1000:.0f}ms)")
        print("\n🤖 AI Response:")
        print("-" * 80)
        print(response_1.choices[0].message.content)
        print("-" * 80)
        
        # Check if within expected time
        if elapsed_1 < 1.5:
            print(f"⚡ FAST: Response received in {elapsed_1*1000:.0f}ms (Expected: <1500ms)")
        else:
            print(f"⚠️ SLOW: Response took {elapsed_1:.2f}s (Expected: <1.5s)")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: LLaMA 3.3 70B Versatile (Powerful Analysis Model)
    print("\n" + "=" * 80)
    print("🔬 TEST 2: LLaMA 3.3 70B Versatile (Deep Analysis)")
    print("=" * 80)
    
    test_prompt_2 = """Analyze this Python code for the Two Sum problem:

```python
def twoSum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

Provide a JSON analysis with:
{
  "time_complexity": "O(?)",
  "space_complexity": "O(?)",
  "quality_score": 0-100,
  "strengths": ["point1", "point2"],
  "improvements": ["suggestion1"]
}"""
    
    print("\n📝 Prompt:")
    print(test_prompt_2[:200] + "...")
    print("\n⏱️ Calling model: llama-3.3-70b-versatile...")
    
    start_time = time.time()
    try:
        response_2 = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert code analyzer. Always return valid JSON."},
                {"role": "user", "content": test_prompt_2}
            ],
            temperature=0.3,
            max_tokens=500
        )
        elapsed_2 = time.time() - start_time
        
        print(f"\n✅ SUCCESS! Response time: {elapsed_2:.3f}s ({elapsed_2*1000:.0f}ms)")
        print("\n🤖 AI Analysis:")
        print("-" * 80)
        print(response_2.choices[0].message.content)
        print("-" * 80)
        
        # Check if within expected time
        if elapsed_2 < 3.0:
            print(f"⚡ GOOD: Response received in {elapsed_2:.2f}s (Expected: <3s)")
        else:
            print(f"⚠️ SLOW: Response took {elapsed_2:.2f}s (Expected: <3s)")
            
        # Try to parse JSON
        try:
            import json
            response_text = response_2.choices[0].message.content
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            parsed = json.loads(response_text.strip())
            print("\n✅ JSON PARSING: Success!")
            print(f"   - Time Complexity: {parsed.get('time_complexity', 'N/A')}")
            print(f"   - Space Complexity: {parsed.get('space_complexity', 'N/A')}")
            print(f"   - Quality Score: {parsed.get('quality_score', 'N/A')}/100")
        except Exception as e:
            print(f"\n⚠️ JSON PARSING: Failed - {str(e)}")
            print("   (This is OK, model still works, just needs better prompting)")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Model 1 (llama-3.1-8b-instant):     {elapsed_1:.3f}s - {'PASS' if elapsed_1 < 1.5 else 'SLOW'}")
    print(f"✅ Model 2 (llama-3.3-70b-versatile): {elapsed_2:.3f}s - {'PASS' if elapsed_2 < 3.0 else 'SLOW'}")
    print("\n🎉 Both models are working correctly!")
    print("=" * 80)


if __name__ == "__main__":
    test_groq_models()
