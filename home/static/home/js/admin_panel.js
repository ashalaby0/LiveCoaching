
// client stats
async function get_client_stats(){
    const client_stats_res = await fetch(client_stats_url)
    let client_status_obj = await client_stats_res.json()

    let clientCtart = document.getElementById("clientChart").getContext('2d');
    new Chart(clientCtart, {
        type: 'line',
        data: {
            labels: Object.keys(client_status_obj),
            datasets: [{
                label: '# of Clients',
                data: Object.values(client_status_obj),
                backgroundColor: '#ffb703',
                borderColor: '#023047',
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            }
        }
    });
}
get_client_stats()

// coach_stats
async function get_coach_stats() {
    const coach_stats_res = await fetch(coach_stats_url)
    let coach_stats_obj = await coach_stats_res.json()
    
    // draw chart
    let coachCtart = document.getElementById("coachChart").getContext('2d');
    new Chart(coachCtart, {
        type: 'bar',
        data: {
            labels: Object.keys(coach_stats_obj),
            datasets: [{
                label: '# of Coaches',
                data: Object.values(coach_stats_obj),
                backgroundColor: '#023047',
    
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            }
        }
    });
}
get_coach_stats()

// session chart
async function get_session_stats() {
    const session_status_res = await fetch(session_stats_url)
    let session_status_obj = await session_status_res.json()

    let sessionCtart = document.getElementById("sessionChart").getContext('2d');
    new Chart(sessionCtart, {
        type: 'bar',
        data: {
            labels: Object.keys(session_status_obj),
            datasets: [{
                label: '# of Sessions',
                data: Object.values(session_status_obj),
                backgroundColor: '#023047',
    
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            }
        }
    });
}
get_session_stats()


// Sesions per Coach
async function get_sessions_per_coach_data() {

    const sessions_per_coach_res = await fetch(sessions_per_coach_url);
    let sessions_per_coach_obj = await sessions_per_coach_res.json();
    let sessionPerCoachCtart = document.getElementById("sessionPerCoachChart").getContext('2d');
    new Chart(sessionPerCoachCtart, {
        type: 'doughnut',
        data: {
            labels: Object.keys(sessions_per_coach_obj),
            datasets: [{
                label: '# Session Per Coach',
                data: Object.values(sessions_per_coach_obj),
                backgroundColor: [
                    '#ffb703',
                    '#023047',
                    '#ffb703',
                    '#023047',
                    '#ffb703',
                    '#023047'
                ],
    
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    fontColor: "#023047",
                    usePointStyle: true,
                },
                position: "right"
            },
    
        }
    });
}
get_sessions_per_coach_data()

// Sessions per Client
async function get_sessions_per_client_data() {

    const sessions_per_client_res = await fetch(sessions_per_client_url);
    let sessions_per_client_obj = await sessions_per_client_res.json()

    let sessionPerClientCtart = document.getElementById("sessionPerClientChart").getContext('2d');
    new Chart(sessionPerClientCtart, {
        type: 'doughnut',
        data: {
            labels: Object.keys(sessions_per_client_obj),
            datasets: [{
                label: '# Session Per Client',
                data: Object.values(sessions_per_client_obj),
                backgroundColor: [
                    '#ffb703',
                    '#023047',
                    '#ffb703',
                    '#023047',
                    '#ffb703',
                    '#023047'
                ],
    
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    fontColor: "#023047",
                    usePointStyle: true,
                },
                position: "right"
            },
    
        }
    });
}
get_sessions_per_client_data()
