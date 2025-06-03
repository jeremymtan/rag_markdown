#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from rag.rag_chain import RAGChain


def main():
    rag = RAGChain()
    chat_history = []
    
    print("rag chat (quit to exit, clear to reset)")
    
    while True:
        question = input("\n> ").strip()
        
        if question.lower() == 'quit':
            break
        
        if question.lower() == 'clear':
            chat_history = []
            print("cleared")
            continue
        
        if not question:
            continue
        
        try:
            # query rag and stream response
            result = rag.query(question, stream=True)
            
            print("\n", end="", flush=True)
            
            # stream answer chunks
            full_answer = ""
            for chunk in result['answer']:
                print(chunk, end="", flush=True)
                full_answer += chunk
            
            print("\n\nsources:")
            # display source documents
            for i, source in enumerate(result['sources']):
                metadata = source['metadata']
                print(f"  {i+1}. {metadata.get('source')} - {metadata.get('title', metadata.get('file_name'))} ({source['score']:.3f})")
            
            # add to history
            chat_history.append({
                "question": question,
                "answer": full_answer
            })
            
        except Exception as e:
            print(f"error: {e}")
    
    print("\nbye!")


if __name__ == "__main__":
    main()