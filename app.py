from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi untuk menghitung metrik antrian
def calculate_queue_metrics(interarrival_time, service_time):
    lambda_rate = 1 / interarrival_time
    mu = 1 / service_time
    rho = lambda_rate / (2 * mu)

    # Log debugging
    print(f"[DEBUG] Laju Kedatangan (λ): {lambda_rate}")
    print(f"[DEBUG] Laju Pelayanan (μ): {mu}")
    print(f"[DEBUG] Pemanfaatan Pelayan (ρ): {rho}")

    steps = []
    steps.append(f"Laju kedatangan (λ) = 1 / {interarrival_time} = {lambda_rate}")
    steps.append(f"Laju pelayanan (μ) = 1 / {service_time} = {mu}")
    steps.append(f"Pemanfaatan pelayan (ρ) = λ / (2 * μ) = {lambda_rate} / (2 * {mu}) = {rho}")

    if rho < 1:
        wq = rho / (2 * mu * (1 - rho))
        w = wq + (1 / mu)
        steps.append(f"Waktu rata-rata dalam antrian (Wq) = {wq}")
        steps.append(f"Waktu rata-rata dalam sistem (W) = {w}")
        print(f"[DEBUG] Waktu rata-rata dalam antrian (Wq): {wq}")
        print(f"[DEBUG] Waktu rata-rata dalam sistem (W): {w}")
    else:
        wq = "Tak Terhingga"
        w = "Tak Terhingga"
        steps.append("Waktu rata-rata tidak terdefinisi karena ρ ≥ 1.")
        print("[DEBUG] Waktu rata-rata tidak terdefinisi karena ρ ≥ 1.")

    return {
        "lambda_rate": lambda_rate,
        "mu": mu,
        "rho": rho,
        "wq": wq,
        "w": w,
        "steps": steps,
    }

# Route untuk halaman input
@app.route('/')
def input_page():
    print("[DEBUG] Halaman input diakses.")  # Debug log
    return render_template('input.html')

# Route untuk halaman hasil
@app.route('/result', methods=['POST'])
def result_page():
    print("[DEBUG] Halaman hasil dipanggil.")  # Debug log
    try:
        # Mengambil input dari form
        interarrival_time = float(request.form['interarrival_time'])
        service_time = float(request.form['service_time'])
        print(f"[DEBUG] Input Waktu Antar Kedatangan: {interarrival_time}")
        print(f"[DEBUG] Input Waktu Pelayanan: {service_time}")

        # Validasi input
        if interarrival_time <= 0 or service_time <= 0:
            print("[DEBUG] Input tidak valid: nilai harus positif.")
            return render_template('input.html', error="Input harus positif.")

        # Perhitungan metrik
        metrics = calculate_queue_metrics(interarrival_time, service_time)
        print(f"[DEBUG] Metrik hasil perhitungan: {metrics}")
        return render_template('result.html', metrics=metrics)

    except ValueError:
        print("[DEBUG] Input tidak valid: masukkan angka yang benar.")  # Debug log
        return render_template('input.html', error="Masukkan angka yang valid.")

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    print("[DEBUG] Aplikasi Flask dijalankan.")  # Debug log
    app.run(debug=True)