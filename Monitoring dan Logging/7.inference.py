from prometheus_client import start_http_server, Counter, Summary
import time, requests, random

# 5 Metrik Aplikasi
req_total = Counter('app_requests_total', 'Total Prediksi')
req_failed = Counter('app_requests_failed_total', 'Total Gagal')
latency = Summary('app_latency_seconds', 'Waktu Respon')
pred_positive = Counter('app_predictions_positive_total', 'Prediksi Terkena Jantung (1)')
pred_negative = Counter('app_predictions_negative_total', 'Prediksi Sehat (0)')

def simulate_traffic():
    url = "http://127.0.0.1:5001/invocations"
    headers = {"Content-Type": "application/json"}
    
    while True:
        # Data acak
        data = {
            "dataframe_split": {
                "columns": ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"],
                "data": [[random.uniform(29, 77), random.randint(0,1), random.randint(0,3), 
                          random.uniform(94, 200), random.uniform(126, 564), random.randint(0,1), 
                          random.randint(0,2), random.uniform(71, 202), random.randint(0,1), 
                          random.uniform(0, 6.2), random.randint(0,2), random.randint(0,4), random.randint(0,3)]]
            }
        }
        
        start_time = time.time()
        try:
            response = requests.post(url, json=data, headers=headers)
            latency.observe(time.time() - start_time)
            req_total.inc()
            
            if response.status_code == 200:
                result = response.json()['predictions'][0]
                if result == 1:
                    pred_positive.inc()
                else:
                    pred_negative.inc()
            else:
                req_failed.inc()
        except Exception as e:
            req_failed.inc()
            
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == '__main__':
    print("Memulai Inference & Exporter (Aplikasi) di port 8001...")
    start_http_server(8001)
    simulate_traffic()