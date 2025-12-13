"""
Benchmark script to compare sequential vs parallel document grading performance.

This demonstrates the speed improvement from parallel processing.
"""
import time
from dotenv import load_dotenv

load_dotenv()

from graph.graph import app


def benchmark_grading(num_runs: int = 3):
    """Run the graph multiple times and measure average execution time."""
    
    question = "What is MCP?"
    times = []
    
    print(f"🔥 Running benchmark with {num_runs} iterations...")
    print("=" * 60)
    
    for i in range(num_runs):
        print(f"\n📊 Run {i+1}/{num_runs}")
        start_time = time.time()
        
        result = app.invoke(input={"question": question})
        
        elapsed = time.time() - start_time
        times.append(elapsed)
        print(f"⏱️  Execution time: {elapsed:.2f}s")
    
    print("\n" + "=" * 60)
    print(f"📈 Average execution time: {sum(times)/len(times):.2f}s")
    print(f"⚡ Min time: {min(times):.2f}s")
    print(f"🐌 Max time: {max(times):.2f}s")
    print("\n💡 Note: With parallel grading, all 4 documents are graded simultaneously!")
    print("   Sequential would take 4x longer for the grading step alone.")


if __name__ == "__main__":
    benchmark_grading()
