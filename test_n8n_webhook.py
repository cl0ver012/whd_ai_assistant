#!/usr/bin/env python3
"""
Test script for n8n Marketing Analytics AI Assistant webhook
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/marketing-chat"  # Change this to your n8n webhook URL

# Test questions
TEST_QUESTIONS = [
    "What's our total Google Ads spend?",
    "Show me the top 5 campaigns by clicks",
    "What's the average CTR across all campaigns?",
    "Which campaigns have the best conversion rate?",
    "How many impressions did we get in November 2024?",
    "Compare Google Ads vs TikTok performance",
    "What's our cost per conversion?",
    "Show me campaigns with CTR above 2%",
]


def test_webhook(question: str, webhook_url: str = N8N_WEBHOOK_URL) -> dict:
    """
    Send a question to the n8n webhook and return the response
    """
    print(f"\n{'='*80}")
    print(f"🔍 Question: {question}")
    print(f"{'='*80}")
    
    try:
        response = requests.post(
            webhook_url,
            json={"question": question},
            headers={"Content-Type": "application/json"},
            timeout=60  # 60 second timeout
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"\n✅ Success!")
                print(f"\n📊 Answer:")
                print("-" * 80)
                
                # Extract answer (handle both string and object)
                answer = data.get('answer', '')
                if isinstance(answer, dict):
                    answer = json.dumps(answer, indent=2)
                
                print(answer)
                print("-" * 80)
                
                # Show metadata if available
                if 'metadata' in data:
                    metadata = data['metadata']
                    print(f"\n📈 Metadata:")
                    print(f"  • Rows analyzed: {metadata.get('rows_analyzed', 'N/A')}")
                    print(f"  • Timestamp: {metadata.get('timestamp', 'N/A')}")
                
                return data
            else:
                print(f"\n❌ Error: {data.get('error', 'Unknown error')}")
                return None
                
        else:
            print(f"\n❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️ Request timed out (>60s)")
        return None
    except requests.exceptions.ConnectionError:
        print(f"\n🔌 Connection Error: Cannot reach {webhook_url}")
        print(f"\nMake sure:")
        print(f"  • n8n is running")
        print(f"  • The workflow is activated")
        print(f"  • The webhook URL is correct")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def run_all_tests(webhook_url: str = N8N_WEBHOOK_URL):
    """
    Run all test questions
    """
    print("\n" + "="*80)
    print("🤖 TESTING N8N MARKETING ANALYTICS AI ASSISTANT")
    print("="*80)
    print(f"Webhook URL: {webhook_url}")
    print(f"Test Questions: {len(TEST_QUESTIONS)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n\n📝 Test {i}/{len(TEST_QUESTIONS)}")
        result = test_webhook(question, webhook_url)
        results.append({
            'question': question,
            'success': result is not None and result.get('success', False)
        })
    
    # Summary
    print("\n\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    
    if failed > 0:
        print(f"\n❌ Failed Questions:")
        for r in results:
            if not r['success']:
                print(f"  • {r['question']}")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


def interactive_mode(webhook_url: str = N8N_WEBHOOK_URL):
    """
    Interactive mode - ask questions one by one
    """
    print("\n" + "="*80)
    print("🤖 INTERACTIVE MODE - Marketing Analytics AI Assistant")
    print("="*80)
    print(f"Webhook URL: {webhook_url}")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            question = input("💬 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not question:
                continue
            
            test_webhook(question, webhook_url)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test n8n Marketing Analytics AI Assistant')
    parser.add_argument(
        '--url',
        default=N8N_WEBHOOK_URL,
        help='n8n webhook URL (default: http://localhost:5678/webhook/marketing-chat)'
    )
    parser.add_argument(
        '--mode',
        choices=['all', 'interactive', 'single'],
        default='interactive',
        help='Test mode: all (run all tests), interactive (ask questions), single (ask one question)'
    )
    parser.add_argument(
        '--question',
        help='Single question to ask (only with --mode single)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'all':
        run_all_tests(args.url)
    elif args.mode == 'interactive':
        interactive_mode(args.url)
    elif args.mode == 'single':
        if not args.question:
            print("❌ Error: --question is required with --mode single")
            sys.exit(1)
        test_webhook(args.question, args.url)
    
    sys.exit(0)

