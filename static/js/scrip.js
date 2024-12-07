// Fungsi logout sederhana
function logout() {
    alert("You have been logged out.");
    // Redirect ke halaman login
    window.location.href = "login.html"; // Ganti dengan lokasi halaman login
}

// Fungsi untuk memuat data pesanan aktif dari backend
function loadOrderSummary() {
    // Contoh data pesanan aktif
    const orders = [
        { id: 1, customer: "John Doe", status: "In Progress", estimatedTime: "2 hours" },
        { id: 2, customer: "Jane Smith", status: "Pending", estimatedTime: "1 hour" },
        // Tambahan data pesanan lainnya
    ];

    const orderList = document.getElementById("order-list");

    orders.forEach(order => {
        const listItem = document.createElement("li");
        listItem.textContent = `Order ID: ${order.id} - Customer: ${order.customer} - Status: ${order.status} - Estimated Time: ${order.estimatedTime}`;
        orderList.appendChild(listItem);
    });
}

// Fungsi untuk mengirim pesanan baru ke backend
function submitOrder(event) {
    event.preventDefault(); // Mencegah form untuk melakukan reload halaman

    // Ambil nilai input dari form
    const customerName = document.getElementById("customer-name").value;
    const orderDetails = document.getElementById("order-details").value;

    // Kirim data pesanan baru ke backend (contoh)
    console.log("Customer Name:", customerName);
    console.log("Order Details:", orderDetails);

    // Tambahkan logika untuk pengiriman pesanan ke backend sesuai kebutuhan aplikasi Anda
}

// Fungsi untuk memuat data status stok dari backend
function loadStockStatus() {
    // Contoh data status stok
    const stock = [
        { item: "Detergent", quantity: 50 },
        { item: "Softener", quantity: 30 },
        // Tambahan data stok lainnya
    ];

    const stockTableBody = document.querySelector("#stock-status tbody");

    stock.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${item.item}</td><td>${item.quantity}</td>`;
        stockTableBody.appendChild(row);
    });
}

// Fungsi untuk membuat grafik laporan keuangan
function createFinancialChart() {
    const ctx = document.getElementById('financial-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'Revenue',
                data: [1000, 2000, 1500, 2500, 1800, 2200],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

window.onload = function() {
    createFinancialChart();
    // Menambahkan event listener untuk tombol logout
    document.getElementById("logout-btn").addEventListener("click", logout);
};

function createFinancialChart() {
    const financialChartCanvas = document.getElementById('financial-chart');
    if (financialChartCanvas) {
        const ctx = financialChartCanvas.getContext('2d');
        if (ctx) {
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June'],
                    datasets: [{
                        label: 'Revenue',
                        data: [1000, 2000, 1500, 2500, 1800, 2200],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error("getContext() method is not supported.");
        }
    } else {
        console.error("Element with ID 'financial-chart' not found.");
    }
}

window.onload = function() {
    createFinancialChart();
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    } else {
        console.error("Element with ID 'logout-btn' not found.");
    }
};

function createFinancialChart() {
    const financialChartCanvas = document.getElementById('financial-chart');
    if (financialChartCanvas && financialChartCanvas.getContext) {
        const ctx = financialChartCanvas.getContext('2d');
        if (ctx) {
            // Kode untuk membuat grafik di sini
        } else {
            console.error("Unable to access 2D context for <canvas> element.");
        }
    } else {
        console.error("Element with ID 'financial-chart' not found or does not support getContext() method.");
    }
}


