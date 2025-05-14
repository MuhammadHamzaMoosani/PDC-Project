from math import ceil
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from joblib import Parallel, delayed

from main import scrape_kayak_flights

def process_chunk(chunk):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(lambda pair: scrape_kayak_flights(pair[0], pair[1]), chunk))

def chunkify(data, num_chunks):
    chunk_size = ceil(len(data) / num_chunks)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
def scrape_pair(pair):
        origin, destination = pair
        return scrape_kayak_flights(origin, destination)

if __name__ == "__main__":
    # origins = ["Karachi", "Lahore", "Islamabad"]
    origins = ["Karachi", "Islamabad"]
    # origins = ["Hyderabad", "Multan", "Rawalpindi"]
    pairs = [(o, d) for o in origins for d in origins if o != d]

    file_name = "output2.txt"
    start_time = time.time()
    results_seq = [scrape_kayak_flights(origin, destination) for origin, destination in pairs]
    print(f"Sequential Execution Time: {time.time() - start_time} seconds")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"Sequential Execution Time: {time.time() - start_time} seconds\n")

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        results_thread = list(executor.map(lambda pair: scrape_kayak_flights(pair[0], pair[1]), pairs))
    print(f"ThreadPoolExecutor Execution Time: {time.time() - start_time} seconds")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"ThreadPoolExecutor Execution Time: {time.time() - start_time} seconds\n")

        

    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results_process = list(executor.map(scrape_pair, pairs))
    print(f"ProcessPoolExecutor Execution Time: {time.time() - start_time:.2f} seconds")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"ProcessPoolExecutor Execution Time: {time.time() - start_time:.2f} seconds\n")

    # ========= Joblib Parallel =========
    start_time = time.time()
    results_joblib = Parallel(n_jobs=-1)(delayed(scrape_kayak_flights)(origin, destination) for origin, destination in pairs)
    print(f"Joblib Parallel Execution Time: {time.time() - start_time:.2f} seconds")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"Joblib Parallel Execution Time: {time.time() - start_time:.2f} seconds\n")

    # ========= Hybrid Execution (Process + Thread) =========
    start_time = time.time()
    # num_processes = 4
    num_processes = 8
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"Number of threads: {num_processes}\n")
    chunks = chunkify(pairs, num_processes)

    with ProcessPoolExecutor(max_workers=num_processes) as process_executor:
        nested_results = list(process_executor.map(process_chunk, chunks))

    # Flatten results
    results_hybrid = [item for sublist in nested_results for item in sublist]
    print(f"Hybrid Execution Time (Process + Thread): {time.time() - start_time:.2f} seconds")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"Hybrid Execution Time (Process + Thread): {time.time() - start_time:.2f} seconds\n")