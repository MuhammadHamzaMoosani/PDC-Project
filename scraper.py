import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from joblib import Parallel, delayed

# Assume scrape_kayak_flights is your scraping function
from main import scrape_kayak_flights

# List of origin airports
origins = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Multan",
           "Sialkot", "Faisalabad", "Quetta", "Sukkur", "Bahawalpur",
           "Dera Ghazi Khan", "Rahim Yar Khan", "Skardu", "Gilgit", "Chitral"]
pairs = [(o, d) for o in origins for d in origins if o != d]

# Sequential Execution
start_time = time.time()
results_seq = [scrape_kayak_flights(origin, destination) for origin, destination in pairs]
print(f"Sequential Execution Time: {time.time() - start_time} seconds")

# ThreadPoolExecutor
start_time = time.time()
with ThreadPoolExecutor() as executor:
    results_thread = list(executor.map(lambda pair: scrape_kayak_flights(pair[0], pair[1]), pairs))
print(f"ThreadPoolExecutor Execution Time: {time.time() - start_time} seconds")

# ProcessPoolExecutor
start_time = time.time()
with ProcessPoolExecutor() as executor:
    results_process = list(executor.map(lambda pair: scrape_kayak_flights(pair[0], pair[1]), pairs))
print(f"ProcessPoolExecutor Execution Time: {time.time() - start_time} seconds")

# Joblib Parallel
start_time = time.time()
results_joblib = Parallel(n_jobs=-1)(delayed(scrape_kayak_flights)(origin, destination) for origin, destination in pairs)
print(f"Joblib Parallel Execution Time: {time.time() - start_time} seconds")