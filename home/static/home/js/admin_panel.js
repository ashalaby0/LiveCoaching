

// client chart
let clientCtart = document.getElementById("clientChart").getContext('2d');
let clientChartObject = new Chart(clientCtart, {
      type: 'line',
      data: {
          labels: ["Jan", "Feb", "March", "April", "May", "June"],
          datasets: [{
              label: '# of Clients',
              data: [3, 6, 7, 25, 12, 19],
              backgroundColor: '#ffb703',
              borderColor: '#023047',
              borderWidth: 1
          }]
      },
      options: {
        legend: {
            display:false,
            labels: {
                fontColor: "white",
            }
        },
          scales: {
              yAxes: [{
                  ticks: {
                    fontColor:"black",
                      beginAtZero:true
                  }
              }],
              xAxes: [{
                ticks: {
                    fontColor:"black"
                }
              }]
          }
      }
  });


  // coach chart
let coachCtart = document.getElementById("coachChart").getContext('2d');
let coachChartObject = new Chart(coachCtart, {
      type: 'bar',
      data: {
          labels: ["Jan", "Feb", "March", "April", "May", "June"],
          datasets: [{
              label: '# of Coaches',
              data: [3, 6, 7, 25, 12, 19],
              backgroundColor: '#023047',
              borderColor: '#ffb703',
              borderWidth: 1
          }]
      },
      options: {
        legend: {
            display:false,
            labels: {
                fontColor: "white",
            }
        },
          scales: {
              yAxes: [{
                  ticks: {
                    fontColor:"black",
                      beginAtZero:true
                  }
              }],
              xAxes: [{
                ticks: {
                    fontColor:"black"
                }
              }]
          }
      }
  });

// session chart
  let sessionCtart = document.getElementById("sessionChart").getContext('2d');
  let sessionChartObject = new Chart(sessionCtart, {
        type: 'bar',
        data: {
            labels: ["Jan", "Feb", "March", "April", "May", "June"],
            datasets: [{
                label: '# of Sessions',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: '#023047',
                borderColor: '#ffb703',
                borderWidth: 1
            }]
        },
        options: {
            legend: {
            display:false,
            labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                      fontColor:"black",
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                  ticks: {
                      fontColor:"black"
                  }
                }]
            }
      }
    });
  

// client chart
let sessionPerCoachCtart = document.getElementById("sessionPerCoachChart").getContext('2d');
let sessionPerCoachChartObject = new Chart(sessionPerCoachCtart, {
      type: 'doughnut',
      data: {
          labels: ["Jan", "Feb", "March", "April", "May", "June"],
          datasets: [{
              label: '# Session Per Coach',
              data: [3, 6, 7, 25, 12, 19],
              backgroundColor: [
                '#ffb703',
                '#023047',
                '#ffb703',
                '#023047',
                '#ffb703',
                '#023047'
            ],
              borderColor: [
                '#023047',
                '#ffb703',
                '#023047',
                '#ffb703',
                '#023047',
                '#ffb703'
            ],
              borderWidth: 1
          }]
      },
      options: {
        legend: {
            display:false,
            labels: {
                fontColor: "white",
            }
        },
         
      }
  });


  // coach chart
let sessionPerClientCtart = document.getElementById("sessionPerClientChart").getContext('2d');
let sessionPerClientChartObject = new Chart(sessionPerClientCtart, {
    type: 'doughnut',
    data: {
        labels: ["Jan", "Feb", "March", "April", "May", "June"],
        datasets: [{
            label: '# Session Per Client',
            data: [3, 6, 7, 25, 12, 19],
            backgroundColor: [
              '#ffb703',
              '#023047',
              '#ffb703',
              '#023047',
              '#ffb703',
              '#023047'
          ],
            borderColor: [
              '#023047',
              '#ffb703',
              '#023047',
              '#ffb703',
              '#023047',
              '#ffb703'
          ],
            borderWidth: 1
        }]
    },
    options: {
      legend: {
          display:false,
          labels: {
              fontColor: "white",
          }
      },
       
    }
});
